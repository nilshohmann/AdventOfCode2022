#!/usr/bin/python3
# -*- coding: utf-8 -*-

dirs = {
  '>': ( 1, 0),
  'v': ( 0, 1),
  '<': (-1, 0),
  '^': ( 0,-1),
}

class mapdict(dict[tuple,bool]):
  def __getitem__(self, __key):
    if __key in self:
      return super().__getitem__(__key)
    return False

class Map:
  def __init__(self, data: list[str]):
    self.w = len(data[0]) - 2
    self.h = len(data) - 2

    self.blizzards = (
      [[] for _ in range(self.h)], # per row
      [[] for _ in range(self.w)], # per column
    )

    self.start = (data[0].index('.')-1, -1)
    self.target = (data[-1].index('.')-1, len(data)-2)

    for y in range(1, len(data)-1):
      for x in range(1, len(data[y])-1):
        if data[y][x] in dirs:
          self.blizzards[0][y-1].append((x-1, dirs[data[y][x]]))
          self.blizzards[1][x-1].append((y-1, dirs[data[y][x]]))

  def switch_start_and_target(self):
    self.start, self.target = (self.target, self.start)

  def distance_to_target(self, p):
    return abs(self.target[0] - p[0]) + abs(self.target[1] - p[1])

  def is_in_map(self, p):
    return 0 <= p[0] < self.w and 0 <= p[1] < self.h

  def move_blizzard(self, p, o, i):
    return ((p[0] + o[0] * i) % self.w, (p[1] + o[1] * i) % self.h)

  def collides_with_blizzard(self, p, i):
    for x, o in self.blizzards[0][p[1]]:
      t = self.move_blizzard((x, p[1]), o, i)
      if t == p:
        return True
    for y, o in self.blizzards[1][p[0]]:
      t = self.move_blizzard((p[0], y), o, i)
      if t == p:
        return True
    return False

  def possible_moves(self, p, i):
    targets = []

    # Wait
    if p == self.start or not self.collides_with_blizzard(p, i):
      targets.append(p)

    # Move
    for _, d in dirs.items():
      t = move(p, d)
      if t == self.target:
        return [t]

      if self.is_in_map(t) and not self.collides_with_blizzard(t, i):
        targets.append(t)

    return targets

  def __str__(self) -> str:
    return f'Map({self.w}x{self.h}, {self.start} -> {self.target})'

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def move(p, o):
  return (p[0]+o[0], p[1]+o[1])

def find_shortest_path(map: Map, i = 1):
  states = [(map.start, map.distance_to_target(map.start))]

  while len(states) > 0:
    new_states = set()
  
    for p, _ in states:
      for t in map.possible_moves(p, i):
        if t == map.target:
          return i
        new_states.add((t, map.distance_to_target(t)))

    states = sorted(new_states, key = lambda x : x[1])[:42]
    i += 1

def main(report_result):
  data = [x for x in read_input().split('\n') if x != '']
  map = Map(data)

  shortest_path = find_shortest_path(map)
  report_result('Shortest path one way:', shortest_path)

  map.switch_start_and_target()
  shortest_path = find_shortest_path(map, shortest_path)
  map.switch_start_and_target()
  shortest_path = find_shortest_path(map, shortest_path)
  report_result('Shortest path forth and back and forth:', shortest_path)

if __name__ == '__main__':
  main(print)
