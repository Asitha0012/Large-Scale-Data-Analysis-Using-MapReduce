#!/usr/bin/env python3
from collections import defaultdict

TOP_N = 20
INPUT_FILE  = '/home/asitha/sentiment_mapreduce/output/results.txt'
OUTPUT_FILE = '/home/asitha/sentiment_mapreduce/output/top_words.txt'

word_counts = defaultdict(dict)

with open(INPUT_FILE, 'r') as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) != 2:
            continue
        key, count_str = parts
        if '_' not in key:
            continue
        star, word = key.split('_', 1)
        if star in {'1','2','3','4','5'}:
            try:
                word_counts[star][word] = int(count_str)
            except ValueError:
                pass

lines_out = []
star_labels = {
    '1':'⭐  (Negative)',
    '2':'⭐⭐  (Poor)',
    '3':'⭐⭐⭐  (Neutral)',
    '4':'⭐⭐⭐⭐  (Good)',
    '5':'⭐⭐⭐⭐⭐  (Excellent)'
}

for star in ['1','2','3','4','5']:
    label  = star_labels[star]
    ranked = sorted(word_counts[star].items(), key=lambda x: x[1], reverse=True)[:TOP_N]
    total  = sum(word_counts[star].values())
    lines_out.append(f'\n{"="*55}')
    lines_out.append(f'Star Rating {star} {label}')
    lines_out.append(f'Total word occurrences: {total:,}')
    lines_out.append(f'Top {TOP_N} words:')
    lines_out.append(f'{"─"*55}')
    for rank, (word, cnt) in enumerate(ranked, 1):
        pct = (cnt / total * 100) if total else 0
        lines_out.append(f'  {rank:2}. {word:<20}  {cnt:>8,}  ({pct:.2f}%)')

output_text = '\n'.join(lines_out)
print(output_text)
with open(OUTPUT_FILE, 'w') as f:
    f.write(output_text + '\n')
print(f'\n✅ Saved to {OUTPUT_FILE}')
