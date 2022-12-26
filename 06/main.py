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

def main(report_result):
  data = read_input()

  report_result('Start of packet:', index_for_first_marker(data, 4))
  report_result('Start of message:', index_for_first_marker(data, 14))

if __name__ == '__main__':
  main(print)
