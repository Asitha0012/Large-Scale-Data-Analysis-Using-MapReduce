#!/usr/bin/env python3
import sys
import csv
import re

STOP_WORDS = {
    'the','a','an','and','or','but','in','on','at','to','for','of','with',
    'is','are','was','were','be','been','being','have','has','had','do',
    'does','did','will','would','could','should','may','might','shall',
    'it','its','this','that','these','those','i','you','he','she','we',
    'they','me','him','her','us','them','my','your','his','our','their',
    'not','no','so','as','if','by','from','up','about','than','then',
    'just','more','also','very','really','get','got','one','all','can',
    'br','amp','quot','http','com','www',
}

MIN_WORD_LEN = 3
MAX_WORD_LEN = 25

def clean_word(word):
    return re.sub(r'[^a-z]', '', word.lower())

def is_valid(word):
    return (MIN_WORD_LEN <= len(word) <= MAX_WORD_LEN
            and word not in STOP_WORDS
            and word.isalpha())

reader = csv.reader(sys.stdin)
header = next(reader, None)

for row in reader:
    try:
        if len(row) < 10:
            continue
        score = row[6].strip()
        text  = row[9].strip()
        if score not in {'1','2','3','4','5'}:
            continue
        if not text:
            continue
        for raw_word in text.split():
            word = clean_word(raw_word)
            if is_valid(word):
                print(f'{score}_{word}\t1')
    except Exception:
        continue
