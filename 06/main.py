#!/usr/bin/python3
# -*- coding: utf-8 -*-

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def index_for_first_marker(data, threshold) -> int:
  index = 0
  last_characters = []

  while True:
    last_characters.append(data[index])
    last_characters = last_characters[-threshold:]
    index = index + 1

    if len(last_characters) == len(set(last_characters)) == threshold:
      return index

if __name__ == '__main__':
  data = read_input()

  print(f'Start of packet: {index_for_first_marker(data, 4)}')
  print(f'Start of message: {index_for_first_marker(data, 14)}')
