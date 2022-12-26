#!/usr/bin/python3
# -*- coding: utf-8 -*-

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def mix_list(data, count = 1):
  original_list = [[n, i] for i, n in enumerate(data)]
  mixed_list = list(original_list)

  for _ in range(count):
    for item in original_list:
      n, i = item
      if mixed_list[i][0] != n:
        raise Exception('Something is off')

      del mixed_list[i]

      new_i = (i + n) % (len(original_list) - 1)
      if new_i < i:
        for x in range(new_i, i):
          mixed_list[x][1] += 1
      else:
        for x in range(i, new_i):
          mixed_list[x][1] -= 1

      item[1] = new_i
      mixed_list.insert(new_i, item)

  return [n for n, _ in mixed_list]

def find_coordinates(data: list):
  start_index = data.index(0)
  return [data[(start_index + i) % len(data)] for i in [1000, 2000, 3000]]

def main(report_result):
  data = [int(x) for x in read_input().split('\n') if x != '']

  coordinates = find_coordinates(mix_list(data))
  report_result('Sum of coordinates:', sum(coordinates))

  decryption_key = 811589153
  data = [n * decryption_key for n in data]

  coordinates = find_coordinates(mix_list(data, 10))
  report_result('Sum of coordinates after 10 rounds:', sum(coordinates))

if __name__ == '__main__':
  main(print)
