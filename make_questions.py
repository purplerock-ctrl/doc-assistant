import csv
import random

import anthropic
from dotenv import load_dotenv
from pypdf import PdfReader

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-sonnet-5-5"
PDF = "data/p17.pdf"

reader = PdfReader(PDF)
pages = [(i, p.extract_text() or "") for i, p in enumerate(reader.pages, start=1)]
pages = [(i, t) for i, t in pages if len(t.split()) > 200]   # skip near-empty pages
random.seed(1)
picked = random.sample(pages, 30)

rows = []
for n, (page_num, text) in enumerate(sorted(picked), start=1):
    response = client.messages.create(
        model=MODEL, max_tokens=300,
        messages=[{"role": "user", "content":
            "Write one question a taxpayer might ask that this page answers "
            "clearly, and the short correct answer. Use plain everyday wording, "
            "not the page's exact phrasing. Reply in exactly two lines:\n"
            "Q: ...\nA: ...\n\nPage text:\n" + text}])
    lines = response.content[0].text.strip().splitlines()
    q = next((l[2:].strip() for l in lines if l.startswith("Q:")), "")
    a = next((l[2:].strip() for l in lines if l.startswith("A:")), "")
    rows.append([f"q{n:02d}", q, a, page_num, "yes"])
    print(f"q{n:02d} p{page_num}: {q}")

with open("data/questions.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "question", "answer", "pages", "answerable"])
    writer.writerows(rows)