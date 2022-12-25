#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

monkey_regex = re.compile("""Monkey ([0-9]):
  Starting items: ([0-9, ]+)
  Operation: new = ([^ ]+ . [^ ]+)
  Test: divisible by ([0-9]+)
    If true: throw to monkey ([0-9])
    If false: throw to monkey ([0-9])""")

class Operation:
  def __init__(self, operation) -> None:
    x1, self.operant, x2 = operation.split(' ')
    self.values = [x1 if x1 == 'old' else int(x1), x2 if x2 == 'old' else int(x2)]

  def process(self, value: int) -> int:
    value = self.__process(value)
    return value

  def __process(self, value: int) -> int:
    values = [(value if x == 'old' else x) for x in self.values]
    if self.operant == '+':
      return values[0] + values[1]
    if self.operant == '*':
      return values[0] * values[1]
    raise Exception(f'Invalid operant: {self.operant}')

  def __str__(self) -> str:
    return f'Operation({self.values[0]} {self.operant} {self.values[1]})'

class Test:
  def __init__(self, divider, on_true, on_false) -> None:
    self.divider = divider
    self.on_true = on_true
    self.on_false = on_false

  def next_id(self, value):
    return self.on_true if value % self.divider == 0 else self.on_false

  def __str__(self) -> str:
    return f'Test({self.divider} ? {self.on_true} : {self.on_false})'

class Monkey:
  def __init__(self, id, items, operation, test) -> None:
    self.id = id
    self.items = items
    self.operation = operation
    self.test = test
    self.inspected_items = 0

  def has_items(self) -> bool:
    return len(self.items) > 0

  def process_next_item(self, worry_reduction):
    self.inspected_items = self.inspected_items + 1
    new_worry_level = self.operation.process(self.items[0])
    new_worry_level = worry_reduction(new_worry_level)

    self.items = self.items[1:]
    next_id = self.test.next_id(new_worry_level)

    return [next_id, new_worry_level]

  def __str__(self) -> str:
    return f'Monkey({self.id} - {self.items} - {self.operation} - {self.test})'

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def parse_monkey(data):
  id, items, operation, divider, on_true, on_false = monkey_regex.match(data).groups()
  items = [int(x) for x in items.split(', ')]

  test = Test(int(divider), int(on_true), int(on_false))
  return Monkey(id, items, Operation(operation), test)

if __name__ == '__main__':
  data = [x for x in read_input().split('\n\n') if x != '']

  monkeys = [parse_monkey(x) for x in data]

  for i in range(20):
    for m in monkeys:
      while m.has_items():
        next_id, item = m.process_next_item(lambda x : x // 3)
        monkeys[next_id].items.append(item)

  activity = list(reversed(sorted([m.inspected_items for m in monkeys])))
  print(f'Monkey business after 20 rounds: {activity[0] * activity[1]}')

  monkeys = [parse_monkey(x) for x in data]

  common_divider = 1
  for m in monkeys:
    common_divider = common_divider * m.test.divider

  for i in range(10000):
    for m in monkeys:
      while m.has_items():
        next_id, item = m.process_next_item(lambda x : x % common_divider)
        monkeys[next_id].items.append(item)

  activity = list(reversed(sorted([m.inspected_items for m in monkeys])))
  print(f'New monkey business after 10000 rounds: {activity[0] * activity[1]}')
