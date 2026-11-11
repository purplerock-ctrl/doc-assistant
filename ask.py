import sys

import anthropic
import chromadb
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-sonnet-5-5"
TOP_K = 5

SYSTEM = (
    "You answer questions using only the numbered sources provided. "
    "After each claim, cite the source number in square brackets, like [2]. "
    "If the sources do not contain the answer, reply exactly: "
    "\"I can't find that in these documents.\" "
    "Do not use outside knowledge. Keep answers short."
)


def retrieve(question, collection_name, k=TOP_K):
    collection = chromadb.PersistentClient(path="chroma_db").get_collection(collection_name)
    results = collection.query(query_texts=[question], n_results=k)
    return list(zip(results["documents"][0], results["metadatas"][0]))


def answer(question, collection_name, model=MODEL):
    chunks = retrieve(question, collection_name)
    sources = "\n\n".join(
        f"[{i}] ({meta['source']}, page {meta['page']})\n{text}"
        for i, (text, meta) in enumerate(chunks, start=1))

    response = client.messages.create(
        model=model,
        max_tokens=600,
        system=SYSTEM,
        messages=[{"role": "user",
                   "content": f"Sources:\n\n{sources}\n\nQuestion: {question}"}],
    )
    return response.content[0].text, chunks, response.usage


if __name__ == "__main__":
    text, chunks, usage = answer(sys.argv[2], sys.argv[1])
    print(text, "\n")
    for i, (_, meta) in enumerate(chunks, start=1):
        print(f"[{i}] {meta['source']} page {meta['page']}")
    print(f"\n{usage.input_tokens} input tokens, {usage.output_tokens} output tokens")