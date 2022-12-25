#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Grid(list):
  __sand_start = [500, 0]
  __possible_moves = [[0,1], [-1,1], [1,1]]

  def __init__(self, rocks, has_floor = False):
    self.start, self.end = Grid.__find_dimensions(rocks)
    if has_floor:
      height = self.end[1] - self.start[1] + 2
      self.start = [500 - height, 0]
      self.end = [500 + height, height]

    width = self.end[0] - self.start[0] + 1
    self.grid = [['.' for x in range(width)] for y in range(self.end[1] + 1)]

    for r in rocks:
      p = r[0]

      for c in r[1:]:
        for point in line(p, c):
          self[point] = '#'
        p = c

    if has_floor:
        for point in line([self.start[0], self.end[1]], self.end):
          self[point] = '#'

    self[Grid.__sand_start] = '+'

  def is_in_grid(self, p):
    return p[0] >= self.start[0] and p[0] <= self.end[0] and p[1] <= self.end[1]

  def next_sand(self):
    p = list(Grid.__sand_start)
    if self[p] == 'o':
      return False

    while True:
      can_move = False

      for m in Grid.__possible_moves:
        t = move(p, m)
        if not self.is_in_grid(t):
          return False

        if self[t] == '.':
          p = t
          can_move = True
          break

      if not can_move:
        self[p] = 'o'
        return True

  def __getitem__(self, p):
    return self.grid[p[1]][p[0] - self.start[0]]

  def __setitem__(self, p, v):
    self.grid[p[1]][p[0] - self.start[0]] = v

  @staticmethod
  def __find_dimensions(rocks):
    start = list(Grid.__sand_start)
    end = list(Grid.__sand_start)

    for r in rocks:
      for x,y in r:
        if x < start[0]:
          start[0] = x
        if x > end[0]:
          end[0] = x
        if y < start[1]:
          start[1] = y
        if y > end[1]:
          end[1] = y

    return [start, end]

  def __str__(self):
    return '\n'.join([''.join(x) for x in self.grid])

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def parse(data):
  return [[int(x) for x in pair.split(',')] for pair in data.split(' -> ')]

def move(p, o):
  return [p[0] + o[0], p[1] + o[1]]

def line(start, end):
  offset = [0,0]
  if end[0] > start[0]:
    offset[0] = 1
  if end[0] < start[0]:
    offset[0] = -1
  if end[1] > start[1]:
    offset[1] = 1
  if end[1] < start[1]:
    offset[1] = -1

  points = []
  p = start
  while p != end:
    points.append(p)
    p = move(p, offset)
  points.append(p)

  return points

if __name__ == '__main__':
  rocks = [parse(x) for x in read_input().split('\n') if x != '']

  grid = Grid(rocks)

  number_of_sand_grains = 0
  while grid.next_sand():
    number_of_sand_grains = number_of_sand_grains + 1
  print(f'Number of sand grains: {number_of_sand_grains}')

  grid = Grid(rocks, True)

  number_of_sand_grains = 0
  while grid.next_sand():
    number_of_sand_grains = number_of_sand_grains + 1
  print(f'Number of sand grains with floor: {number_of_sand_grains}')
