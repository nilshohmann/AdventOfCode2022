#!/usr/bin/python3
# -*- coding: utf-8 -*-

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def split_in_half(data):
  if len(data) == 0 or len(data) % 2 != 0:
    print(f'Invalid input: {data}')

  half_size = len(data) // 2
  return [data[:half_size], data[half_size:]]

def split_into_groups(data):
  group_size = 3
  if len(data) % group_size != 0:
    raise Exception('Invalid number of items')

  return [data[i:i + group_size] for i in range(0, len(data), group_size)]

def priority_for_item(item):
  item_value = ord(item)

  if item_value >= ord('A') and item_value <= ord('Z'):
    return item_value - 38
  elif item_value >= ord('a') and item_value <= ord('z'):
    return item_value - 96
  else:
    raise Exception(f'Invalid item: {item[0]}')

def determine_priority_for_rucksack(data):
  common_items = set([x for x in data[0] if x in data[1]])
  if len(common_items) != 1:
    raise Exception(f'Invalid data: {data}')

  return priority_for_item(common_items.pop())

def determine_priority_for_group(data):
  common_items = set([x for x in data[0] if x in data[1] and x in data[2]])
  if len(common_items) != 1:
    raise Exception(f'Invalid data: {data}')

  return priority_for_item(common_items.pop())

def main(report_result):
  data = [x for x in read_input().split('\n') if x != '']

  priorities = sum([determine_priority_for_rucksack(split_in_half(x)) for x in data])
  report_result('Sum of priorities by rucksack:', priorities)

  priorities = sum([determine_priority_for_group(x) for x in split_into_groups(data)])
  report_result('Sum of priorities by group:', priorities)

if __name__ == '__main__':
  main(print)
