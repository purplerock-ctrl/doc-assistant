import argparse
import csv
from datetime import datetime
from pathlib import Path

from ask import find_chunks

parser = argparse.ArgumentParser(description="Measure how often retrieval finds the right page.")
parser.add_argument("collection", help="Collection name, e.g. p17-v1")
parser.add_argument("--method", choices=["semantic", "hybrid"], default="semantic")
parser.add_argument("--k", type=int, default=5, help="How many chunks to retrieve (default 5)")
parser.add_argument("--questions", default="data/questions.csv")
parser.add_argument("--note", default="", help="What changed in this run")
args = parser.parse_args()

with open(args.questions, newline="", encoding="utf-8-sig") as f:
    rows = [r for r in csv.DictReader(f) if r["answerable"] == "yes"]

hit1 = hitk = 0
misses = []
for r in rows:
    expected = {int(p) for p in r["pages"].split(";")}
    chunks = find_chunks(r["question"], args.collection, method=args.method, k=args.k)
    got = [meta["page"] for _, meta in chunks]
    if got and got[0] in expected:
        hit1 += 1
    if expected & set(got):
        hitk += 1
    else:
        print(f"MISS {r['id']}: wanted {sorted(expected)}, got {got} | {r['question']}")
        misses.append((r["id"], sorted(expected), got, r["question"]))

n = len(rows)
print(f"\nhit@1: {hit1}/{n} = {hit1 / n:.0%}   (right page ranked first)")
print(f"hit@{args.k}: {hitk}/{n} = {hitk / n:.0%}   (right page anywhere in the top {args.k})")

log_path = Path("results/retrieval.md")
log_path.parent.mkdir(exist_ok=True)
new_file = not log_path.exists() or log_path.stat().st_size == 0
lines = []
if new_file:
    lines.append("# Retrieval eval log\n")
lines += [
    f"\n## {datetime.now():%Y-%m-%d %H:%M} | {args.collection} | {args.method} | k={args.k}\n",
    f"- Note: {args.note or '-'}",
    f"- Questions: `{args.questions}` ({n} answerable)",
    f"- hit@1: {hit1}/{n} = {hit1 / n:.0%}",
    f"- hit@{args.k}: {hitk}/{n} = {hitk / n:.0%}",
]
if misses:
    lines += ["", "| Miss | Wanted | Got | Question |", "| --- | --- | --- | --- |"]
    for qid, wanted, got, question in misses:
        question = question.replace("|", "\\|")
        lines.append(f"| {qid} | {wanted} | {got} | {question} |")
with log_path.open("a", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print(f"Logged to {log_path}")