#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time

def measure(task):
  start_time = time.time()
  measures = []

  def format_duration(d):
    if d < 1:
      d *= 1000
      return f'{d:.2f}ms'
    return f'{d:.3f}s'

  def add_measure(message, result):
    last_completion = measures[-1][1] if len(measures) > 0 else 0
    duration = time.time() - start_time - last_completion
    measures.append((result, duration))

    print(f'[{format_duration(duration)}] {message} {result}')

  task(add_measure)

  with open('results.md', 'w') as f:
    f.write(f"""# Results

| Part | Result | Time |
| --- | --- | --- |
""" + ''.join([f'| {i+1} | {m[0]} | {format_duration(m[1])} |\n' for i, m in enumerate(measures)]))
