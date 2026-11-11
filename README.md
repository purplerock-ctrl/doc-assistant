# Tax Guide Assistant

Ask questions about U.S. federal income tax in plain English and get short answers drawn only from IRS Publication 17 (2025), with page citations. When the publication doesn't cover a question, it says so instead of guessing.

**[Live demo](https://doc-assistant-ndzfkpqgdqrqimbupdw4vk.streamlit.app/)** (password protected to control API costs)

![Screenshot of the app](screenshot.png)

> Not tax advice. Answers come only from the 2025 edition of Publication 17.

## How it works

1. **Ingest (once):** the PDF is split into 250-word chunks with 50 words of overlap. Each chunk is stored in a Chroma vector database with its page number and an embedding of its meaning.
2. **Retrieve (every question):** hybrid search ranks chunks two ways, by meaning (embeddings) and by keywords (BM25, with stopwords removed), then merges the rankings with reciprocal rank fusion and keeps the top 5.
3. **Answer:** Claude (`claude-sonnet-5-5`) gets the question plus the 5 numbered chunks, with instructions to answer only from them, cite each claim by source number, and reply with a fixed decline sentence if the answer isn't there.
4. **Log:** every question, answer, cited pages, decline flag, token count and response time is recorded.

## Results

Measured against a hand-reviewed question set built from the publication: 38 answerable questions with known answers and pages, plus 10 questions it should decline. Answers were graded by a separate Claude call acting as judge, spot-checked by hand.

| Measure | Result |
| --- | --- |
| Retrieval: right page in the top 5 | 35/38 (92%) |
| Answers fully correct | 29/38 (76%) |
| Wrong answers | 0/38 |
| Made-up answers to questions it should decline | 0/10 |
| **Held-back set** (8 questions never used for tuning): fully correct | **6/8 (75%), 0 wrong** |

The held-back score matches the main set, so the setup generalises rather than being fitted to the test questions.

### Retrieval experiments

All runs use the 38 answerable questions, top 5 results unless noted. Full log: [results/retrieval.md](results/retrieval.md).

| Setup | Right page in top 5 |
| --- | --- |
| 500-word chunks, meaning only | 30/38 |
| 250-word chunks, hybrid (naive keyword splitting) | 31/38 |
| 120-word chunks, meaning only | 32/38 |
| 120-word chunks, hybrid (improved keywords) | 32/38 |
| 250-word chunks, meaning only, top 10 | 33/38 |
| **250-word chunks, hybrid (improved keywords)** | **35/38** |

### Answer experiments

| Change | Correct | Wrong | Made up | Kept? |
| --- | --- | --- | --- | --- |
| Top 8 chunks | 29/38 | 0 | 0 | No: same accuracy at higher cost |
| **Top 5 chunks** | **29/38** | **0** | **0** | **Yes** |
| Top 5 + "include all conditions" instruction | 28/38 | 0 | 0 | No: no improvement |

## What I learned

- **Check the answer key before blaming the system.** Three retrieval "misses" were labels listing only one of several pages that contain the answer.
- **Small details in search code matter.** Keyword search went from the worst option to the best after stripping punctuation and filler words: 31/38 to 35/38.
- **"Right page" isn't "right chunk".** Page-level retrieval scores overstate success. On the standard deduction question, page 97 was retrieved but the chunk with the table wasn't, so the answer hedged.
- **Prompts can't fix missing context.** An instruction to include all conditions didn't help, because the sentences with those conditions weren't among the retrieved chunks.
- **Safe failures are a feature.** When retrieval missed, the assistant declined rather than inventing an answer, including on a question where a similar-sounding but wrong rule was retrieved.
- **Spending more isn't always better.** Sending 8 chunks instead of 5 cost more and didn't improve accuracy.
- **Judges need checking too.** The grading model once questioned a figure printed in the publication itself, using outside arithmetic.

## Limitations

- Tax-table lookups (e.g. "tax on $34,720 as head of household") fail: tables don't suit search. They'd need a dedicated lookup.
- Each question is answered on its own, so follow-ups like "what if I'm over 50?" lose context.
- One document, one tax year (2025).
- The question set is small (48 questions plus 8 held back), so a single question moves scores by 2 to 12 points.
- Answer quality is judged by a model, spot-checked by hand rather than fully hand-graded.

## Project structure

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit chat app; builds the database on first load and logs every question |
| `ask.py` | Retrieval (meaning, keyword and hybrid) and answer generation |
| `ingest.py` | Splits the PDF into chunks and stores them in Chroma |
| `eval_retrieval.py` | Measures how often the right page is retrieved, and logs each run |
| `eval_answers.py` | Generates answers for every test question and grades them with a judge model |
| `make_questions.py` | Drafts test questions from random pages for human review |

## Run it yourself

```
pip install -r requirements.txt
```

Add `ANTHROPIC_API_KEY` and `APP_PASSWORD` to `.streamlit/secrets.toml`, then:

```
python ingest.py p17-v1
streamlit run app.py
```
