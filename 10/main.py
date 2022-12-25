#!/usr/bin/python3
# -*- coding: utf-8 -*-

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def parse_command(data):
  if data == 'noop':
    return [0] # One cycle without changes
  if data.startswith('addx '):
    return [0, int(data[5:])] # Two cylces with changes in the second
  raise Exception(f'Unknown command: {data}')

def split_into_groups(data, group_size):
  if len(data) % group_size != 0:
    raise Exception('Invalid number of items')

  return [data[i:i + group_size] for i in range(0, len(data), group_size)]

if __name__ == '__main__':
  data = [x for x in read_input().split('\n') if x != '']
  # print(input)
  relevant_cycles = [20, 60, 100, 140, 180, 220]
  crt_width = 40

  cycle = 0
  register = 1

  signal_history = []
  crt_output = []

  for x in data:
    for c in parse_command(x):
      cycle = cycle + 1

      if cycle in relevant_cycles:
        signal_history.append(register)

      crt_output.append('#' if ((cycle - 1) % crt_width + 1) in range(register, register + 3) else '.')

      register = register + c

  print(f'Sum of signal strengths: {sum([relevant_cycles[i] * signal_history[i] for i in range(len(relevant_cycles))])}')

  print('CRT output:')
  for line in split_into_groups(crt_output, crt_width):
    print(''.join(line))
