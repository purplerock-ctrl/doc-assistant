import argparse
from pathlib import Path

import chromadb
from pypdf import PdfReader


def chunk_text(text, size, overlap):
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
    parser = argparse.ArgumentParser(description="Chunk the PDFs in data/ into a collection.")
    parser.add_argument("name", help="Collection name, at least 3 characters, e.g. p17-v2")
    parser.add_argument("--size", type=int, default=250, help="Words per chunk (default 250)")
    parser.add_argument("--overlap", type=int, default=50, help="Words shared between chunks (default 50)")
    args = parser.parse_args()

    client = chromadb.PersistentClient(path="chroma_db")
    try:
        client.delete_collection(args.name)              # rebuild from scratch
    except Exception:
        pass
    collection = client.create_collection(args.name)

    ids, docs, metas = [], [], []
    for pdf in sorted(Path("data").glob("*.pdf")):
        reader = PdfReader(pdf)
        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            for i, chunk in enumerate(chunk_text(text, args.size, args.overlap)):
                ids.append(f"{pdf.name}-p{page_num}-c{i}")
                docs.append(chunk)
                metas.append({"source": pdf.name, "page": page_num})

    for start in range(0, len(ids), 200):                # add in batches
        collection.add(ids=ids[start:start + 200],
                       documents=docs[start:start + 200],
                       metadatas=metas[start:start + 200])
    print(f"Stored {len(ids)} chunks in collection '{args.name}' "
          f"({args.size} words, {args.overlap} overlap)")


if __name__ == "__main__":
    main()