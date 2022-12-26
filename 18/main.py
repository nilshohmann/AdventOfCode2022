#!/usr/bin/python3
# -*- coding: utf-8 -*-

dirs = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]

class CubeData(list):
  def __init__(self, data):
    super().__init__([parse(x) for x in data.split('\n') if x != ''])
    x, y, z = self[0]
    x = [x, x]
    y = [y, y]
    z = [z, z]

    for cx,cy,cz in self[1:]:
      if cx < x[0]: x[0] = cx
      elif cx > x[1]: x[1] = cx
      if cy < y[0]: y[0] = cy
      elif cy > y[1]: y[1] = cy
      if cz < z[0]: z[0] = cz
      elif cz > z[1]: z[1] = cz

    self.__dimensions = (x, y, z)

  def find_air_bubbles(self):
    dx, dy, dz = self.__dimensions
    remaining_cubes = []
    for x in range(dx[0]-1, dx[1]+2):
      for y in range(dy[0]-1, dy[1]+2):
        for z in range(dz[0]-1, dz[1]+2):
          c = (x,y,z)
          if not c in self:
            remaining_cubes.append(c)

    to_determine = [remaining_cubes.pop()]
    while len(to_determine) > 0:
      c = to_determine.pop()
      for t in [move(c, d) for d in dirs]:
        if t in remaining_cubes:
          remaining_cubes.remove(t)
          to_determine.append(t)

    return remaining_cubes

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def parse(data: str) -> tuple[str]:
  x, y, z = data.split(',')
  return (int(x), int(y), int(z))

def move(f, o):
  return (f[0]+o[0], f[1]+o[1], f[2]+o[2])

def find_air_bubbles(cubes: CubeData, candidates: list):
  bubbles = []

  current_bubble = set()
  current_candidates = []

  while len(candidates) > 0:
    current_bubble = set()
    current_candidates = [candidates.pop()]

    while len(current_candidates) > 0:
      c = current_candidates.pop()
      current_bubble.add(c)
      # print(c)

      for d in dirs:
        t = move(c, d)
        if t in cubes or t in current_bubble:
          continue

        if t in candidates:
          candidates.remove(t)
          continue

        if not cubes.is_in_area(t):
          # print(f'Found opening')
          current_bubble = set()
          current_candidates.clear()
          break
        current_candidates.append(t)

    if len(current_bubble) > 0:
      bubbles.append(sorted(current_bubble))

  return bubbles

def surface_of(cubes):
  remaining_cubes = {c: 6 for c in cubes}
  total_surface = 0

  while len(remaining_cubes) > 0:
    c, s = remaining_cubes.popitem()
    for d in dirs:
      t = move(c, d)
      if t in remaining_cubes:
        remaining_cubes[t] -= 1
        s -= 1

    total_surface += s

  return total_surface

def main(report_result):
  cubes = CubeData(read_input())

  total_surface = surface_of(cubes)
  report_result('Total surface:', total_surface)

  air_bubbles = cubes.find_air_bubbles()
  air_bubble_surface = surface_of(air_bubbles)

  report_result('Total surface without air bubbles:', total_surface - air_bubble_surface)

if __name__ == '__main__':
  main(print)
