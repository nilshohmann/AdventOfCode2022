#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

class Monkey:
  __regex = re.compile('^([a-z]+): (.*)$')
  __operations = {
    '+': lambda x,y: x+y,
    '-': lambda x,y: x-y,
    '*': lambda x,y: x*y,
    '/': lambda x,y: x//y,
  }

  def __init__(self, data: str) -> None:
    self.name, task = Monkey.__regex.match(data).groups()
    if task.isnumeric():
      self.result = int(task)
      self.input = []
      self.op = None
    else:
      task = task.split(' ')
      self.result = None
      self.input = [task[0], task[2]]
      self.op = task[1]

  def reset(self):
    if len(self.input) > 0:
      self.result = None

  def solve(self, data = None) -> int:
    if self.result is None:
      self.result = Monkey.__operations[self.op](data[0], data[1])
    return self.result

  def __str__(self) -> str:
    return f'Monkey({self.name}, {self.op}, {self.input}, {self.result})'

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def find_answer_for(name: str, all_monkeys: dict[str, Monkey]) -> int:
  monkey = all_monkeys[name]
  if len(monkey.input) == 0:
    return monkey.solve()

  return monkey.solve([find_answer_for(m, all_monkeys) for m in monkey.input])

def find_answer_for_root(monkeys: dict[str, Monkey], human_value: int = None) -> int:
  if not human_value is None:
    [m.reset() for _, m in monkeys.items()]
    monkeys['humn'].result = human_value

  return find_answer_for('root', monkeys)

def find_result_for_humn(monkeys: dict[str, Monkey]):
  root_monkey = monkeys['root']

  root_monkey.op = '-'
  reference = pow(2, 63)

  boundaries = [
    (-reference, find_answer_for_root(monkeys, -reference)),
    (0, find_answer_for_root(monkeys, reference)),
    (reference, find_answer_for_root(monkeys, reference)),
  ]

  for _ in range(1000):
    options = []
    for i in range(2):
      value = (boundaries[i][0] + boundaries[i+1][0]) // 2
      result = find_answer_for_root(monkeys, value)
      if result == 0:
        return [j for j in range(value-10, value+10) if find_answer_for_root(monkeys, j) == 0]

      options.append((value, result))

    if abs(options[0][1]) > abs(options[1][1]):
      boundaries = (boundaries[1], options[1], boundaries[2])
    else:
      boundaries = (boundaries[0], options[0], boundaries[1])

  for i in range(boundaries[0][0], boundaries[-1][0]):
    if 0 == find_answer_for_root(monkeys, i):
      return i
  return -1

def main(report_result):
  monkeys = [Monkey(x) for x in read_input().split('\n') if x != '']

  monkey_dict = {m.name: m for m in monkeys}
  report_result('Root yells:', find_answer_for_root(monkey_dict))

  result_for_humn = find_result_for_humn(monkey_dict)
  report_result('Result for humn:', result_for_humn)

if __name__ == '__main__':
  main(print)
