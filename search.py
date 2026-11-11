import sys

import chromadb

name, question = sys.argv[1], sys.argv[2]
collection = chromadb.PersistentClient(path="chroma_db").get_collection(name)

results = collection.query(query_texts=[question], n_results=5)
for text, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(f"--- {meta['source']} page {meta['page']} ---")
    print(text[:300], "...\n")