#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

item_reges = re.compile('^\[([A-Z])\]$')
command_regex = re.compile('^move ([0-9]+) from ([1-9]) to ([1-9])$')

class Line:
  def __init__(self, name) -> None:
    self.name = name
    self.items = []

  def push(self, item):
    self.items.append(item)

  def pop(self):
    return self.items.pop() if len(self.items) > 0 else ''

  def __str__(self) -> str:
    return f'Line({self.name}, [{", ".join(self.items)}])'

  def __repr__(self) -> str:
    return self.__str__()


def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def split_into_groups(data):
  group_size = 4

  return [data[i:i + group_size] for i in range(0, len(data), group_size)]

def parse_lines(data):
  rows = [x for x in data.split('\n') if x != '']

  lines = [Line(x.strip()) for x in split_into_groups(rows.pop())]

  for line in reversed(rows):
    for c, item in enumerate([x.strip() for x in split_into_groups(line)]):
      if item != '':
        lines[c].push(item_reges.match(item).groups()[0])

  return lines

def main(report_result):
  initial_state, commands = [x for x in read_input().split('\n\n') if x != '']
  commands = [[int(i) for i in command_regex.match(x).groups()] for x in commands.split('\n') if x != '']

  lines = parse_lines(initial_state)
  for c, f, t in commands:
    poped_items = [lines[f -1].pop() for i in range(c)]
    for item in poped_items:
      lines[t - 1].push(item)

  identifier = ''.join([x.pop() for x in lines])
  report_result('Final crate identifier with CrateMover 9000:', identifier)

  lines = parse_lines(initial_state)
  for c, f, t in commands:
    poped_items = [lines[f -1].pop() for i in range(c)]
    for item in reversed(poped_items):
      lines[t - 1].push(item)

  identifier = ''.join([x.pop() for x in lines])
  report_result('Final crate identifier with CrateMover 9001:', identifier)

if __name__ == '__main__':
  main(print)
