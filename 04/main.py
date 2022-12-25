#!/usr/bin/python3
# -*- coding: utf-8 -*-

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def parse_section(data):
  values = [int(x) for x in data.split('-')]
  if len(values) != 2:
    raise Exception(f'Invalid section: {data}')

  return values

def intersection(lst1, lst2):
    return [value for value in lst1 if value in lst2]

def has_complete_overlap(data):
  section_1, section_2 = [parse_section(x) for x in data.split(',')]

  section_1 = list(range(section_1[0], section_1[1] + 1))
  section_2 = list(range(section_2[0], section_2[1] + 1))
  common = intersection(section_1, section_2)

  is_overlapping = len(common) == len(section_1) or len(common) == len(section_2)

  return is_overlapping

def has_overlap(data):
  section_1, section_2 = [parse_section(x) for x in data.split(',')]

  section_1 = list(range(section_1[0], section_1[1] + 1))
  section_2 = list(range(section_2[0], section_2[1] + 1))
  common = intersection(section_1, section_2)

  is_overlapping = len(common) > 0

  return is_overlapping

if __name__ == '__main__':
  data = [x for x in read_input().split('\n') if x != '']

  print(f'Number of sections contained in the other: {len([x for x in data if has_complete_overlap(x)])}')
  print(f'Number of sections overlapping: {len([x for x in data if has_overlap(x)])}')
