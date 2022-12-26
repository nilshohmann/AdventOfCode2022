#!/usr/bin/python3
# -*- coding: utf-8 -*-

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def snafu_to_decimal(data: str):
  mapping = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2,
  }

  result = 0
  for i, x in enumerate(reversed(data)):
    result += mapping[x] * pow(5, i)
  return result

def decimal_to_snafu(value: int) -> str:
  mapping = {
    -2: '=',
    -1: '-',
    0: '0',
    1: '1',
    2: '2',
  }

  result = []

  i = 0
  while value > 0:
    if len(result) <= i:
      result.append(0)

    v = result[i] + value % 5
    value //= 5

    if 0 <= v < 3:
      result[i] = v
    else:
      result[i] = v - 5
      result.append(1)
    i += 1

  return ''.join(reversed([mapping[x] for x in result]))

def main(report_result):
  data = [x for x in read_input().split('\n') if x != '']

  needed_fuel = sum([snafu_to_decimal(d) for d in data])
  report_result('Needed fuel in snafu:', decimal_to_snafu(needed_fuel))

if __name__ == '__main__':
  main(print)
