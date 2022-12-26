#!/usr/bin/python3
# -*- coding: utf-8 -*-

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def sum_data(data: str) -> int:
  elf_data = [int(x) for x in data.rstrip().split('\n')]
  return sum(elf_data)

def main(report_result):
  data = read_input()
  elfes_sorted = sorted([sum_data(x) for x in data.split('\n\n')])
  report_result('Elf with highest:', elfes_sorted[-1])

  report_result(f'Elfes with highest: {elfes_sorted[-3:]} - sum:', sum(elfes_sorted[-3:]))

if __name__ == '__main__':
  main(print)
