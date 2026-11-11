import sys

import anthropic
import chromadb
from dotenv import load_dotenv
from rank_bm25 import BM25Okapi

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-sonnet-5-5"
RETRIEVAL = "hybrid"   # "semantic" or "hybrid": set to the Week 10 winner
TOP_K = 5                # how many chunks to send to the model

SYSTEM = (
    "You answer questions using only the numbered sources provided. "
    "After each claim, cite the source number in square brackets, like [2]. "
    "If the sources do not contain the answer, reply exactly: "
    "\"I can't find that in these documents.\" "
    "Do not use outside knowledge. Keep answers short."
)

_db = chromadb.PersistentClient(path="chroma_db")
_keyword_index = {}


def retrieve(question, collection_name, k=TOP_K):
    """Meaning-based search only."""
    collection = _db.get_collection(collection_name)
    results = collection.query(query_texts=[question], n_results=k)
    return list(zip(results["documents"][0], results["metadatas"][0]))

import re

STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "is", "are", "was",
    "do", "does", "did", "i", "my", "me", "you", "your", "it", "if", "can", "how",
    "what", "when", "where", "which", "who", "much", "many", "be", "have", "has",
    "that", "this", "with", "about", "from", "at", "by", "as", "so", "any", "still",
}

def tokenize(text):
    words = re.findall(r"[a-z0-9]+(?:[-,][a-z0-9]+)*", text.lower())
    return [w for w in words if w not in STOPWORDS]

def retrieve_hybrid(question, collection_name, k=TOP_K, fetch=20):
    """Meaning-based search plus keyword search, merged into one ranking."""
    collection = _db.get_collection(collection_name)

    # Build the keyword index once per collection
    if collection_name not in _keyword_index:
        everything = collection.get(include=["documents", "metadatas"])
        tokens = [tokenize(d) for d in everything["documents"]]
        _keyword_index[collection_name] = (BM25Okapi(tokens), everything)
    bm25, everything = _keyword_index[collection_name]

    # Ranking 1: by meaning
    by_meaning = collection.query(query_texts=[question], n_results=fetch)["ids"][0]

    # Ranking 2: by keywords
    scores = bm25.get_scores(tokenize(question))
    order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:fetch]
    by_keyword = [everything["ids"][i] for i in order]

    # Merge: a chunk ranked high in either list scores well
    combined = {}
    for ranking in (by_meaning, by_keyword):
        for rank, chunk_id in enumerate(ranking):
            combined[chunk_id] = combined.get(chunk_id, 0) + 1 / (60 + rank)
    best = sorted(combined, key=combined.get, reverse=True)[:k]

    lookup = dict(zip(everything["ids"], zip(everything["documents"], everything["metadatas"])))
    return [lookup[i] for i in best]


def find_chunks(question, collection_name, method=RETRIEVAL, k=TOP_K):
    """Pick the search method by name."""
    if method == "hybrid":
        return retrieve_hybrid(question, collection_name, k=k)
    return retrieve(question, collection_name, k=k)


def answer(question, collection_name, model=MODEL):
    chunks = find_chunks(question, collection_name)
    sources = "\n\n".join(
        f"[{i}] ({meta['source']}, page {meta['page']})\n{text}"
        for i, (text, meta) in enumerate(chunks, start=1))

    response = client.messages.create(
        model=model,
        max_tokens=1500,
        system=SYSTEM,
        messages=[{"role": "user",
                   "content": f"Sources:\n\n{sources}\n\nQuestion: {question}"}],
    )
    text = "".join(block.text for block in response.content if block.type == "text")
    return text, chunks, response.usage


if __name__ == "__main__":
    text, chunks, usage = answer(sys.argv[2], sys.argv[1])
    print(text, "\n")
    for i, (_, meta) in enumerate(chunks, start=1):
        print(f"[{i}] {meta['source']} page {meta['page']}")
    print(f"\n{usage.input_tokens} input tokens, {usage.output_tokens} output tokens")