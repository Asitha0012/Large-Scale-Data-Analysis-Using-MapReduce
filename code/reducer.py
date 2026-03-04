#!/usr/bin/env python3
import sys

current_key   = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split('\t')
    if len(parts) != 2:
        continue
    key, count_str = parts[0], parts[1]
    try:
        count = int(count_str)
    except ValueError:
        continue
    if key == current_key:
        current_count += count
    else:
        if current_key is not None:
            print(f'{current_key}\t{current_count}')
        current_key   = key
        current_count = count

if current_key is not None:
    print(f'{current_key}\t{current_count}')
