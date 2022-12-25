#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

file_reges = re.compile('^([0-9]+) +([^ ]+)$')

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

class Dir:
  def __init__(self, name) -> None:
    self.name = name
    self.content = []

  def add(self, item):
    self.content.append(item)

  def size(self) -> int:
    return sum([c.size() for c in self.content])

  def __repr__(self) -> str:
    return '\n'.join([f'- dir {self.name} ({self.size()})'] + [f'{x}' for x in self.content])

class File:
  def __init__(self, name, size) -> None:
    self.name = name
    self.__size__ = size

  def size(self) -> int:
    return self.__size__

  def __repr__(self) -> str:
    return f'- file {self.name} ({self.size()})'

def parse_line(data: str):
  if data.startswith('$ '):
    if data[2:] == 'ls':
      return None
    if data[2:].startswith('cd '):
      return Dir(data[5:])
    raise Exception(f'Unknown command: {data}')

  if data.startswith('dir '):
    return None # We handle these when we go into it

  match = file_reges.match(data)
  if match is not None:
    size, name = match.groups()
    return File(name, int(size))

  raise Exception(f'Invalid line: {data}')

def parse_structure(data):
  current_path = []

  for l in data:
    c = parse_line(l)
    if isinstance(c, Dir):
      if c.name == '..':
        current_path.pop()
        continue

      if len(current_path) > 0:
        current_path[-1].add(c)
      current_path.append(c)

    elif isinstance(c, File):
      current_path[-1].add(c)

    else:
      continue

  return current_path[0]

def find_relevant_dirs(dir: Dir, is_relevant: int):
  result = [dir] if is_relevant(dir.size()) else []

  for item in dir.content:
    if isinstance(item, Dir):
      result = result + find_relevant_dirs(item, is_relevant)

  return result

if __name__ == '__main__':
  data = [x for x in read_input().split('\n') if x != '']

  root = parse_structure(data)

  relevant_dirs = find_relevant_dirs(root, lambda x : x <= 100000)
  print(f'Size of relevant dirs with duplicates: {sum([d.size() for d in relevant_dirs])}')

  maximium_allowed_space = 70000000 - 30000000
  minimum_size_to_be_removed = root.size() - maximium_allowed_space
  print(minimum_size_to_be_removed)

  relevant_dirs = find_relevant_dirs(root, lambda x : x >= minimum_size_to_be_removed)
  size_of_relevant_dir_with_smallest_size = sorted([d.size() for d in relevant_dirs])[0]
  print(f'Size of smallest dir to be removed: {size_of_relevant_dir_with_smallest_size}')
