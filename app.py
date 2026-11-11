import sqlite3
import subprocess
import sys
import time

import chromadb
import streamlit as st

from ask import answer

COLLECTION = "p17-v1"   # your best collection from Week 10
DECLINE = "I can't find that in these documents"

st.title("Tax guide assistant")
st.caption("Answers come only from IRS Publication 17, with page citations. Not tax advice.")

if st.text_input("Password", type="password") != st.secrets["APP_PASSWORD"]:
    st.stop()


@st.cache_resource(show_spinner="Preparing the documents (first run only)...")
def ensure_index():
    client = chromadb.PersistentClient(path="chroma_db")
    try:
        if client.get_collection(COLLECTION).count() > 0:
            return True
    except Exception:
        pass
    subprocess.run([sys.executable, "ingest.py", COLLECTION], check=True)
    return True


def log(question, text, chunks, usage, seconds):
    conn = sqlite3.connect("log.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS questions (
        asked_at TEXT DEFAULT CURRENT_TIMESTAMP, question TEXT, answer TEXT,
        pages TEXT, declined INTEGER, input_tokens INTEGER, output_tokens INTEGER,
        seconds REAL)""")
    conn.execute(
        "INSERT INTO questions (question, answer, pages, declined, input_tokens, "
        "output_tokens, seconds) VALUES (?,?,?,?,?,?,?)",
        (question, text, ", ".join(str(m["page"]) for _, m in chunks),
         int(DECLINE.lower() in text.lower()),
         usage.input_tokens, usage.output_tokens, seconds))
    conn.commit()


ensure_index()

if "history" not in st.session_state:
    st.session_state.history = []

for role, content in st.session_state.history:
    with st.chat_message(role):
        st.markdown(content)

question = st.chat_input("Ask about federal income tax")
if question:
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Searching the guide..."):
            start = time.time()
            text, chunks, usage = answer(question, COLLECTION)
            seconds = time.time() - start
        sources = "\n".join(f"[{i}] page {m['page']}" for i, (_, m) in enumerate(chunks, 1))
        reply = f"{text}\n\n**Sources**\n{sources}"
        st.markdown(reply)
    st.session_state.history += [("user", question), ("assistant", reply)]
    log(question, text, chunks, usage, seconds)