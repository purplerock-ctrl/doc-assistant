import csv
import sys

import anthropic
from dotenv import load_dotenv

from ask import answer

load_dotenv()
client = anthropic.Anthropic()
JUDGE_MODEL = "claude-sonnet-5-5"
DECLINE = "I can't find that in these documents"

collection_name = sys.argv[1]
note = sys.argv[2] if len(sys.argv) > 2 else ""
questions_file = sys.argv[3] if len(sys.argv) > 3 else "data/questions.csv"


def judge(question, reference, candidate):
    response = client.messages.create(
        model=JUDGE_MODEL, max_tokens=1000,
        messages=[{"role": "user", "content":
            "You are grading an answer against a reference answer.\n"
            f"Question: {question}\nReference: {reference}\nCandidate: {candidate}\n\n"
            "Is the candidate correct? Wording may differ; facts and numbers must match. "
            "Extra correct detail is fine. Reply with one word on the first line: "
            "CORRECT, PARTIAL or WRONG. Then one sentence explaining why."}])
    text = "".join(b.text for b in response.content if b.type == "text").strip()
    if not text:
        return "WRONG", "(judge returned no verdict)"
    return text.split()[0].strip(".:*").upper(), text


with open(questions_file, newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

counts = {"correct": 0, "partial": 0, "wrong": 0, "wrongly_declined": 0,
          "correctly_declined": 0, "made_up": 0}
review = []

for r in rows:
    text, chunks, usage = answer(r["question"], collection_name)
    declined = DECLINE.lower() in text.lower()

    if r["answerable"] == "no":
        outcome = "correctly_declined" if declined else "made_up"
        reason = ""
    elif declined:
        outcome, reason = "wrongly_declined", ""
    else:
        verdict, reason = judge(r["question"], r["answer"], text)
        outcome = {"CORRECT": "correct", "PARTIAL": "partial"}.get(verdict, "wrong")

    counts[outcome] += 1
    review.append([r["id"], r["question"], r["answer"], text, outcome, reason])
    print(f"{r['id']}: {outcome}")

answerable = sum(1 for r in rows if r["answerable"] == "yes")
unanswerable = len(rows) - answerable
print(f"\nCorrect:            {counts['correct']}/{answerable}")
print(f"Partial:            {counts['partial']}/{answerable}")
print(f"Wrong:              {counts['wrong']}/{answerable}")
print(f"Wrongly declined:   {counts['wrongly_declined']}/{answerable}")
print(f"Correctly declined: {counts['correctly_declined']}/{unanswerable}")
print(f"Made up an answer:  {counts['made_up']}/{unanswerable}   <- the most dangerous number")

with open("answer_review.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "question", "reference", "answer", "outcome", "judge_reason"])
    writer.writerows(review)