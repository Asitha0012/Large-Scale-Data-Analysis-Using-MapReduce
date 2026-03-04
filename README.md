Large-Scale Data Analysis Using MapReduce
Overview

This project analyses Amazon Fine Food Reviews to extract the most frequent words per star rating (1–5). Using Hadoop Streaming and Python 3, the MapReduce workflow tokenises review text, filters stopwords, counts word frequencies, and ranks the top 20 words per rating. This provides insight into customer sentiment patterns across thousands of reviews.

Dataset

Source: Amazon Fine Food Reviews (568,454 reviews, 1999–2012)

Content: Each review contains Score (1–5) and Text fields.

Note: The dataset is not included in this repo due to size, but you can download it from Kaggle or other sources.

Project Structure
sentiment_mapreduce/
│
├── code/
│   ├── mapper.py          # MapReduce mapper script
│   ├── reducer.py         # MapReduce reducer script
│   └── analyse.py         # Post-processing: ranks top words per rating
│
├── data/                  # Place Reviews.csv here if running locally
├── input_sample.log       # Sample input for testing
├── output_sample.log      # Sample MapReduce output
├── results.txt            # Full MapReduce output
├── top_words_per_star.txt # Top-20 words per rating
└── .gitignore
Setup & Execution
1. Environment

WSL Ubuntu or Linux terminal

Python 3

Hadoop 3.3.6 (pseudo-distributed mode)

2. Run MapReduce
# Start Hadoop daemons
start-dfs.sh
start-yarn.sh

# Submit Hadoop streaming job
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.4.2.jar \
  -input /user/<username>/sentiment/input/Reviews.csv \
  -output /user/<username>/sentiment/output \
  -mapper "python3 code/mapper.py" \
  -reducer "python3 code/reducer.py" \
  -file code/mapper.py \
  -file code/reducer.py
3. Post-process results
python3 code/analyse.py results.txt top_words_per_star.txt

Generates top_words_per_star.txt containing the top 20 words per star rating.

4. Sample Logs
# Input sample
head -50 /user/<username>/sentiment/input/Reviews.csv > input_sample.log

# Output sample
hdfs dfs -cat /user/<username>/sentiment/output/part-00000 | head -50 > output_sample.log
Results & Insights

1–2 stars: Words like terrible, awful, disappointed indicate negative sentiment.

3 stars: Mixed terms; both positive and negative appear, showing ambiguous opinions.

4–5 stars: Words like love, delicious, great reflect positive sentiment.

Food descriptors such as taste, flavor, smell appear in all ratings.




The dataset is excluded from the repository. Place Reviews.csv in data/ or HDFS input folder.

Stopwords are filtered in the mapper script.

All Python scripts are compatible with Python 3 and Hadoop Streaming.
