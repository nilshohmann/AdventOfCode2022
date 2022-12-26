#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

dirs = [
  ( 1,  0), # right, intial
  ( 0,  1), # down
  (-1,  0), # left
  ( 0, -1), # up
]

class Map:
  def __init__(self, data: str):
    self.cube_map = None

    data = data.split('\n')
    l = max([len(d) for d in data])
    self.__data = [d.ljust(l) for d in data]
    self.reset_position()

    self.size = max([len(self.__data), l]) // 4

  def iscube(self):
    return not self.cube_map is None

  def build_cube_map(self):
    sides_map = [(x,y) for y in range(len(self.__data) // self.size) \
      for x in range(len(self.__data[0]) // self.size) \
        if self.__data[y * self.size][x * self.size] != ' ']

    # Initial cube map
    self.cube_map = {s: {} for s in sides_map}

    # Add direct neighbors
    while len(sides_map) > 0:
      s = sides_map.pop()
      for i, d in enumerate(dirs):
        t = move(s, d)
        if t in sides_map:
          self.cube_map[s][i] = (t, 0)
          self.cube_map[t][(i+2)%4] = (s, 0)

    # Some magic to determine other neighbors on the cube via adjencent neighbors
    # until all neighbors are available
    while sum([4-len(m) for _,m in self.cube_map.items()]) != 0:
      for direction_mappings in [m for _,m in self.cube_map.items() if len(m) != 4]:
        for d, t in list(direction_mappings.items()):
          if not (d+1)%4 in direction_mappings and (t[1]+d+1)%4 in self.cube_map[t[0]]:
            x = self.cube_map[t[0]][(t[1]+d+1)%4]
            direction_mappings[(d+1)%4] = (x[0], (t[1]+x[1]-1)%4)

  def reset_position(self):
    self.position = (self.__data[0].index('.'), 0, 0)

  def process_instructions(self, instructions: list):
    for i in instructions:
      if i == 'R':
        self.position = (self.position[0], self.position[1], (self.position[2] + 1) % len(dirs))
      elif i == 'L':
        self.position = (self.position[0], self.position[1], (self.position[2] - 1) % len(dirs))
      else:
        self.__move(int(i))

  def __itemat(self, p) -> str:
    return self.__data[p[1]][p[0]]

  def __moveone_flat(self, p):
    # Left or right
    if p[2] % 2 == 0:
      r = (p[0] + dirs[p[2]][0]) % len(self.__data[p[1]])
      return (r, p[1], p[2])

    # Up or down
    c = (p[1] + dirs[p[2]][1]) % len(self.__data)
    return (p[0], c, p[2])

  def __moveone_cube(self, p):
    o = dirs[p[2]]
    n = (p[0] + o[0], p[1] + o[1], p[2])
    if 0 <= n[0] < len(self.__data[0]) and 0 <= n[1] < len(self.__data) and self.__itemat(n) != ' ':
      return n

    t, r = self.cube_map[(p[0] // self.size, p[1] // self.size)][p[2]]
    np = (n[0] % self.size, n[1] % self.size)
    for _ in range(r):
      np = (self.size - np[1] - 1, np[0])

    return (t[0] * self.size + np[0], t[1] * self.size + np[1], (n[2] + r) % 4)

  def __move(self, l):
    n = self.position

    for _ in range(l):
      if self.iscube():
        n = self.__moveone_cube(n)
      else:
        n = self.__moveone_flat(n)
        while self.__itemat(n) == ' ':
          n = self.__moveone_flat(n)

      if self.__itemat(n) == '#':
        break

      self.position = n

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def move(p, o, c = 1):
  return (p[0] + o[0] * c, p[1] + o[1] * c)

def find_password_for_map(map: Map, instructions: list):
  map.process_instructions(instructions)

  column, row, direction = map.position
  return 1000 * (row + 1) + 4 * (column + 1) + direction

def main(report_result):
  map, instructions = [x for x in read_input().split('\n\n') if x != '']
  map = Map(map)
  instructions = re.findall("[0-9]+|[LR]", instructions)

  report_result('Final password:', find_password_for_map(map, instructions))

  map.build_cube_map()
  map.reset_position()
  report_result('Final password with cube:', find_password_for_map(map, instructions))

if __name__ == '__main__':
  main(print)
