import sys
from pathlib import Path

import chromadb
from pypdf import PdfReader

CHUNK_WORDS = 250     # words per chunk
OVERLAP_WORDS = 50    # words shared between neighbouring chunks


def chunk_text(text, size=CHUNK_WORDS, overlap=OVERLAP_WORDS):
    words = text.split()
    chunks = []
    step = size - overlap
    for start in range(0, max(len(words), 1), step):
        piece = words[start:start + size]
        if piece:
            chunks.append(" ".join(piece))
        if start + size >= len(words):
            break
    return chunks


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "v1"   # one collection per version
    client = chromadb.PersistentClient(path="chroma_db")
    try:
        client.delete_collection(name)                   # rebuild from scratch
    except Exception:
        pass
    collection = client.create_collection(name)

    ids, docs, metas = [], [], []
    for pdf in sorted(Path("data").glob("*.pdf")):
        reader = PdfReader(pdf)
        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            for i, chunk in enumerate(chunk_text(text)):
                ids.append(f"{pdf.name}-p{page_num}-c{i}")
                docs.append(chunk)
                metas.append({"source": pdf.name, "page": page_num})

    for start in range(0, len(ids), 200):                # add in batches
        collection.add(ids=ids[start:start + 200],
                       documents=docs[start:start + 200],
                       metadatas=metas[start:start + 200])
    print(f"Stored {len(ids)} chunks in collection '{name}'")


if __name__ == "__main__":
    main()