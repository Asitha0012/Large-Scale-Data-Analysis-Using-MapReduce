# Large-Scale Data Analysis Using MapReduce
### Sentiment Word Frequency Analysis — Amazon Fine Food Reviews


## Overview

This project analyses **Amazon Fine Food Reviews** to extract the most frequent words per star rating (1–5). Using **Hadoop Streaming** and **Python 3**, the MapReduce workflow tokenises review text, filters stopwords, counts word frequencies, and ranks the top 20 words per rating — revealing customer sentiment patterns at scale across 568,454 reviews.

| Component | Detail |
|---|---|
| Dataset | Amazon Fine Food Reviews — 568,454 rows |
| Task | Sentiment Word Frequency Analysis grouped by Star Rating |
| MapReduce Key | Composite key: `star_word` e.g. `5_delicious` |
| Language | Python 3 via Hadoop Streaming |
| Platform | Hadoop 3.4.2 — Pseudo-Distributed (WSL / Linux) |

---

## Dataset

- **Source:** [Amazon Fine Food Reviews — Kaggle](https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews)
- **Size:** 568,454 reviews collected between 1999–2012
- **Key columns used:** `Score` (1–5 star rating) and `Text` (review content)
- **Note:** The dataset is not included in this repository due to file size. Download `Reviews.csv` from Kaggle and place it in the `data/` folder.

---

## Project Structure

```
sentiment_mapreduce/
│
├── code/
│   ├── mapper.py               # MapReduce mapper — tokenises text, emits star_word TAB 1
│   ├── reducer.py              # MapReduce reducer — sums counts per composite key
│   └── analyse.py              # Post-processing — ranks top 20 words per star rating
│
├── data/                       # Place Reviews.csv here (not tracked in git)
├── output/
│   ├── results.txt             # Full MapReduce output from HDFS
│   ├── top_words_per_star.txt  # Top-20 words per rating level
│   ├── input_sample.log        # Sample input rows for submission evidence
│   └── output_sample.log       # Sample MapReduce output for submission evidence
│
└── README.md
```

---

## How It Works

```
INPUT (Reviews.csv)
       │
       ▼
  MAPPER.PY
  ─ Reads Score and Text fields
  ─ Lowercases and tokenises text
  ─ Filters 50+ English stopwords
  ─ Emits: star_word  TAB  1
  ─ Example: 5_delicious  1
       │
       ▼
  HADOOP SHUFFLE & SORT
  ─ Groups all pairs by key automatically
       │
       ▼
  REDUCER.PY
  ─ Sums counts per composite key
  ─ Emits: star_word  TAB  total_count
  ─ Example: 5_delicious  4231
       │
       ▼
  ANALYSE.PY
  ─ Reads results.txt
  ─ Ranks top 20 words per star rating
  ─ Outputs: top_words_per_star.txt
```

---

## Setup & Requirements

- WSL (Ubuntu) or any Linux terminal
- Python 3.7+
- Hadoop 3.4.2 in pseudo-distributed mode
- Java JDK 11

### Verify your environment
```bash
java -version       # Should show JDK 11
python3 --version   # Should show Python 3.7+
hadoop version      # Should show Hadoop 3.4.2
jps                 # Should show 5 daemons running
```

---

## Execution Guide

### Step 1 — Start Hadoop Daemons
```bash
start-dfs.sh
start-yarn.sh
jps   # Verify: NameNode, DataNode, SecondaryNameNode, ResourceManager, NodeManager
```

### Step 2 — Upload Dataset to HDFS
```bash
hdfs dfs -mkdir -p /user/<username>/sentiment/input
hdfs dfs -put data/Reviews.csv /user/<username>/sentiment/input/
hdfs dfs -ls /user/<username>/sentiment/input/
```

### Step 3 — Local Test (Optional but Recommended)
```bash
head -201 data/Reviews.csv | \
python3 code/mapper.py | \
sort | \
python3 code/reducer.py | \
head -20
```

### Step 4 — Run MapReduce Job
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.4.2.jar \
  -input  /user/<username>/sentiment/input/Reviews.csv \
  -output /user/<username>/sentiment/output \
  -mapper  "python3 code/mapper.py" \
  -reducer "python3 code/reducer.py" \
  -file code/mapper.py \
  -file code/reducer.py
```

### Step 5 — Retrieve Results
```bash
hdfs dfs -get /user/<username>/sentiment/output/part-00000 output/results.txt
hdfs dfs -cat /user/<username>/sentiment/output/part-00000 | head -50 > output/output_sample.log
head -11 data/Reviews.csv > output/input_sample.log
```

### Step 6 — Post-Process & Analyse
```bash
python3 code/analyse.py
```

Generates `output/top_words_per_star.txt` with the top 20 words per star rating.

---

## Results & Insights

| Star Rating | Top Words | Sentiment |
|---|---|---|
| ⭐ 1 star | terrible, awful, disappointed, waste, bad | Strong negative |
| ⭐⭐ 2 stars | poor, bland, expected, returned, hard | Mild negative |
| ⭐⭐⭐ 3 stars | okay, average, decent, mixed, expected | Ambiguous |
| ⭐⭐⭐⭐ 4 stars | good, great, nice, recommend, quality | Positive |
| ⭐⭐⭐⭐⭐ 5 stars | love, delicious, amazing, perfect, great | Strong positive |

**Key findings:**
- A clear linguistic divide exists between low and high-star reviews
- Food descriptors (`taste`, `flavor`, `smell`) appear across **all** rating levels
- 3-star reviews show the most ambiguous vocabulary — both positive and negative terms appear at similar frequencies
- The word `love` is among the most dominant in 5-star reviews; `disappointed` dominates 1-star

## License

This project is submitted as part of an academic assignment. Dataset copyright belongs to the original authors on Kaggle/SNAP.
