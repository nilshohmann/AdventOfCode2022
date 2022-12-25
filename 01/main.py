#!/usr/bin/python3
# -*- coding: utf-8 -*-

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def sum_data(data: str) -> int:
  elf_data = [int(x) for x in data.rstrip().split('\n')]
  return sum(elf_data)

if __name__ == '__main__':
  data = read_input()
  elfes_sorted = sorted([sum_data(x) for x in data.split('\n\n')])
  print(f'Elf with highest: {elfes_sorted[-1]}')

  print(f'Elfes with highest: {elfes_sorted[-3:]} - sum: {sum(elfes_sorted[-3:])}')
