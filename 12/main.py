#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Map:
  def __init__(self, data) -> None:
    self.start = Map.__find_position(data, 'S')
    self.end = Map.__find_position(data, 'E')
    self.map = Map.__convert_map(data)
    self.size = [len(self.map[0]), len(self.map)]

  def next_positions(self, c):
    value = self.value_at(c)

    possible_positions = []
    if c[0] > 0:
      n = move(c, [-1, 0])
      if self.value_at(n) <= value + 1:
        possible_positions.append(n)
    if c[0] < self.size[0] - 1:
      n = move(c, [1, 0])
      if self.value_at(n) <= value + 1:
        possible_positions.append(n)
    if c[1] > 0:
      n = move(c, [0, -1])
      if self.value_at(n) <= value + 1:
        possible_positions.append(n)
    if c[1] < self.size[1] - 1:
      n = move(c, [0, 1])
      if self.value_at(n) <= value + 1:
        possible_positions.append(n)
    return possible_positions

  def next_positions_reverse(self, c):
    value = self.value_at(c)

    possible_positions = []
    if c[0] > 0:
      n = move(c, [-1, 0])
      if self.value_at(n) >= value - 1:
        possible_positions.append(n)
    if c[0] < self.size[0] - 1:
      n = move(c, [1, 0])
      if self.value_at(n) >= value - 1:
        possible_positions.append(n)
    if c[1] > 0:
      n = move(c, [0, -1])
      if self.value_at(n) >= value - 1:
        possible_positions.append(n)
    if c[1] < self.size[1] - 1:
      n = move(c, [0, 1])
      if self.value_at(n) >= value - 1:
        possible_positions.append(n)
    return possible_positions

  def value_at(self, position):
    return self.map[position[1]][position[0]]

  def __str__(self) -> str:
    return f'Map({self.size[0]}x{self.size[1]} - {self.start} -> {self.end})'

  @staticmethod
  def __find_position(data, type):
    for y in range(len(data)):
      for x in range(len(data[y])):
        if data[y][x] == type:
          return [x, y]
    return None

  @staticmethod
  def __convert_position(data):
    if data == 'S':
      return Map.__convert_position('a')
    if data == 'E':
      return Map.__convert_position('z')

    if data < 'a' or data > 'z':
      raise Exception(f'Invalid data: {data}')

    return ord(data) - 96

  @staticmethod
  def __convert_map(map):
    size = len(map[0])
    for x in map[1:]:
      if len(x) != size:
        raise Exception(f'Invalid dimensions')

    return [[Map.__convert_position(x) for x in row] for row in map]

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def move(s, o):
  return [s[0] + o[0], s[1] + o[1]]

def find_shortest_route_length(map: Map):
  iteration = 0

  visited_positions = [map.start]

  positions_to_check = [map.start]
  next_positions = []

  while len(positions_to_check) > 0:
    for p in positions_to_check:
      visited_positions.append(p)
      if p == map.end:
        return iteration

      for n in map.next_positions(p):
        if not n in next_positions and not n in visited_positions:
          next_positions.append(n)

    positions_to_check = next_positions
    next_positions = []
    iteration = iteration + 1

  return -1

def find_shortest_route_length_reverse(map: Map):
  iteration = 0

  visited_positions = [map.end]

  positions_to_check = [map.end]
  next_positions = []

  while len(positions_to_check) > 0:
    # print(f'{iteration} - {positions_to_check}')

    for p in positions_to_check:
      visited_positions.append(p)
      if map.value_at(p) == 1:
        return iteration

      for n in map.next_positions_reverse(p):
        if not n in next_positions and not n in visited_positions:
          next_positions.append(n)

    positions_to_check = next_positions
    next_positions = []
    iteration = iteration + 1

  return -1

def main(report_result):
  data = [x for x in read_input().split('\n') if x != '']

  map = Map(data)
  report_result('Shortest route length:', find_shortest_route_length(map))
  report_result('Shortest reverse route length:', find_shortest_route_length_reverse(map))

if __name__ == '__main__':
  main(print)
