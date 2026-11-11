# Retrieval eval log


## 2026-11-11 10:28 | p17-v1 | hybrid | k=5

- Note: hybrid
- Questions: `data/questions.csv` (38 answerable)
- hit@1: 15/38 = 39%
- hit@5: 31/38 = 82%

| Miss | Wanted | Got | Question |
| --- | --- | --- | --- |
| q07 | [33] | [37, 26, 9, 37, 37] | How do I figure out whether I paid for more than half of a relative's living costs so I can claim them as a dependent? |
| q09 | [42, 43] | [44, 39, 44, 39, 98] | I get a regular paycheck and don't want to make quarterly estimated tax payments. Is there a way to avoid them? |
| q14 | [78] | [49, 131, 55, 14, 50] | If my employer pays me back for travel costs when I go to a job interview, do I have to report that as income? |
| q18 | [109] | [13, 14, 18, 13, 131] | If I file my return on time, can the IRS work out how much tax I owe, and what happens if I end up owing more? |
| q20 | [123] | [113, 126, 60, 125, 60] | My taxable income is about $90,020 and I'm filing as head of household. How much tax does the table say I owe? |
| q23 | [142] | [18, 18, 8, 5, 13] | I live in Ohio and I'm mailing in my paper tax return with a check for what I owe. Where do I send it? |
| q37 | [5, 13] | [129, 20, 19, 17, 21] | I never filed a return and was owed a refund - how long do I have to claim it? |

## 2026-11-11 10:29 | p17-v1 | semantic | k=10

- Note: top 10
- Questions: `data/questions.csv` (38 answerable)
- hit@1: 21/38 = 55%
- hit@10: 33/38 = 87%

| Miss | Wanted | Got | Question |
| --- | --- | --- | --- |
| q07 | [33] | [26, 37, 27, 37, 29, 37, 38, 38, 38, 36] | How do I figure out whether I paid for more than half of a relative's living costs so I can claim them as a dependent? |
| q14 | [78] | [49, 55, 50, 49, 75, 107, 41, 41, 39, 73] | If my employer pays me back for travel costs when I go to a job interview, do I have to report that as income? |
| q18 | [109] | [13, 13, 21, 21, 12, 14, 22, 5, 13, 17] | If I file my return on time, can the IRS work out how much tax I owe, and what happens if I end up owing more? |
| q20 | [123] | [126, 125, 124, 119, 120, 124, 68, 117, 125, 67] | My taxable income is about $90,020 and I'm filing as head of household. How much tax does the table say I owe? |
| q35 | [3] | [41, 103, 105, 95, 49, 78, 73, 102, 94, 75] | How much overtime pay can I deduct? |

## 2026-11-11 10:31 | p17-v2 | semantic | k=5

- Note: small chunks
- Questions: `data/questions.csv` (38 answerable)
- hit@1: 21/38 = 55%
- hit@5: 32/38 = 84%

| Miss | Wanted | Got | Question |
| --- | --- | --- | --- |
| q07 | [33] | [27, 37, 37, 37, 27] | How do I figure out whether I paid for more than half of a relative's living costs so I can claim them as a dependent? |
| q14 | [78] | [49, 99, 49, 73, 55] | If my employer pays me back for travel costs when I go to a job interview, do I have to report that as income? |
| q18 | [109] | [21, 12, 13, 17, 13] | If I file my return on time, can the IRS work out how much tax I owe, and what happens if I end up owing more? |
| q19 | [117] | [43, 125, 126, 113, 125] | If I'm filing as head of household and my taxable income is $34,720, how much tax do I owe according to the 2025 tax table? |
| q20 | [123] | [125, 126, 125, 47, 113] | My taxable income is about $90,020 and I'm filing as head of household. How much tax does the table say I owe? |
| q37 | [5, 13] | [21, 21, 21, 17, 129] | I never filed a return and was owed a refund - how long do I have to claim it? |

## 2026-11-11 10:31 | p17-v2 | hybrid | k=5

- Note: small chunks + hybrid
- Questions: `data/questions.csv` (38 answerable)
- hit@1: 25/38 = 66%
- hit@5: 31/38 = 82%

| Miss | Wanted | Got | Question |
| --- | --- | --- | --- |
| q07 | [33] | [37, 36, 27, 26, 37] | How do I figure out whether I paid for more than half of a relative's living costs so I can claim them as a dependent? |
| q09 | [42, 43] | [44, 45, 39, 98, 44] | I get a regular paycheck and don't want to make quarterly estimated tax payments. Is there a way to avoid them? |
| q18 | [109] | [21, 18, 12, 14, 13] | If I file my return on time, can the IRS work out how much tax I owe, and what happens if I end up owing more? |
| q19 | [117] | [43, 14, 125, 27, 126] | If I'm filing as head of household and my taxable income is $34,720, how much tax do I owe according to the 2025 tax table? |
| q20 | [123] | [126, 113, 125, 65, 65] | My taxable income is about $90,020 and I'm filing as head of household. How much tax does the table say I owe? |
| q23 | [142] | [18, 5, 131, 18, 131] | I live in Ohio and I'm mailing in my paper tax return with a check for what I owe. Where do I send it? |
| q37 | [5, 13] | [21, 21, 56, 129, 20] | I never filed a return and was owed a refund - how long do I have to claim it? |

## 2026-11-11 10:33 | p17-v3 | semantic | k=5

- Note: big chunks
- Questions: `data/questions.csv` (38 answerable)
- hit@1: 17/38 = 45%
- hit@5: 30/38 = 79%

| Miss | Wanted | Got | Question |
| --- | --- | --- | --- |
| q07 | [33] | [37, 37, 38, 38, 36] | How do I figure out whether I paid for more than half of a relative's living costs so I can claim them as a dependent? |
| q14 | [78] | [49, 55, 39, 73, 73] | If my employer pays me back for travel costs when I go to a job interview, do I have to report that as income? |
| q18 | [109] | [13, 21, 12, 22, 5] | If I file my return on time, can the IRS work out how much tax I owe, and what happens if I end up owing more? |
| q20 | [123] | [126, 124, 119, 120, 124] | My taxable income is about $90,020 and I'm filing as head of household. How much tax does the table say I owe? |
| q21 | [128] | [22, 16, 23, 11, 11] | If the IRS picks my tax return for an audit, does that mean they think I cheated? |
| q35 | [3] | [103, 105, 95, 78, 73] | How much overtime pay can I deduct? |
| q36 | [78] | [42, 42, 54, 39, 46] | Do I have to pay tax on jury duty pay? |
| q38 | [77] | [127, 69, 126, 100, 125] | At what amount should a client send me a 1099-NEC? |

## 2026-11-11 10:34 | p17-v1 | semantic | k=5

- Note: baseline
- Questions: `data/questions.csv` (38 answerable)
- hit@1: 21/38 = 55%
- hit@5: 32/38 = 84%

| Miss | Wanted | Got | Question |
| --- | --- | --- | --- |
| q07 | [33] | [26, 37, 27, 37, 29] | How do I figure out whether I paid for more than half of a relative's living costs so I can claim them as a dependent? |
| q09 | [42, 43] | [44, 45, 39, 39, 44] | I get a regular paycheck and don't want to make quarterly estimated tax payments. Is there a way to avoid them? |
| q14 | [78] | [49, 55, 50, 49, 75] | If my employer pays me back for travel costs when I go to a job interview, do I have to report that as income? |
| q18 | [109] | [13, 13, 21, 21, 12] | If I file my return on time, can the IRS work out how much tax I owe, and what happens if I end up owing more? |
| q20 | [123] | [126, 125, 124, 119, 120] | My taxable income is about $90,020 and I'm filing as head of household. How much tax does the table say I owe? |
| q35 | [3] | [41, 103, 105, 95, 49] | How much overtime pay can I deduct? |

## 2026-11-11 10:36 | p17-v1 | hybrid | k=5

- Note: hybrid, better tokenizing
- Questions: `data/questions.csv` (38 answerable)
- hit@1: 21/38 = 55%
- hit@5: 35/38 = 92%

| Miss | Wanted | Got | Question |
| --- | --- | --- | --- |
| q18 | [109] | [13, 13, 13, 17, 8] | If I file my return on time, can the IRS work out how much tax I owe, and what happens if I end up owing more? |
| q20 | [123] | [113, 126, 11, 125, 31] | My taxable income is about $90,020 and I'm filing as head of household. How much tax does the table say I owe? |
| q37 | [5, 13] | [20, 21, 21, 20, 21] | I never filed a return and was owed a refund - how long do I have to claim it? |

## 2026-11-11 10:36 | p17-v2 | hybrid | k=5

- Note: small chunks + hybrid, better tokenizing
- Questions: `data/questions.csv` (38 answerable)
- hit@1: 27/38 = 71%
- hit@5: 32/38 = 84%

| Miss | Wanted | Got | Question |
| --- | --- | --- | --- |
| q07 | [33] | [27, 37, 27, 37, 36] | How do I figure out whether I paid for more than half of a relative's living costs so I can claim them as a dependent? |
| q09 | [42, 43] | [44, 45, 45, 44, 39] | I get a regular paycheck and don't want to make quarterly estimated tax payments. Is there a way to avoid them? |
| q15 | [80] | [85, 86, 89, 87, 85] | I'm 72 and still working part-time. Can I still put money into my traditional IRA, or am I too old? |
| q18 | [109] | [17, 13, 13, 13, 13] | If I file my return on time, can the IRS work out how much tax I owe, and what happens if I end up owing more? |
| q20 | [123] | [43, 113, 124, 117, 125] | My taxable income is about $90,020 and I'm filing as head of household. How much tax does the table say I owe? |
| q37 | [5, 13] | [21, 21, 21, 21, 21] | I never filed a return and was owed a refund - how long do I have to claim it? |
