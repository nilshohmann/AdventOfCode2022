#!/usr/bin/python3
# -*- coding: utf-8 -*-

class mapdict(dict[tuple,bool]):
  def __getitem__(self, __key):
    if __key in self:
      return super().__getitem__(__key)
    return False

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def move(p, o):
  return (p[0]+o[0], p[1]+o[1])

def possible_moves_for(p, elfes_map, i: int):
  local_map = [[elfes_map[(p[0]+x,p[1]+y)] for x in [-1,0,1]] for y in [-1,0,1]]
  possible_moves = [
    (( 0,-1), 0 == len([x for x in range(3) if local_map[0][x]])), # north
    (( 0, 1), 0 == len([x for x in range(3) if local_map[2][x]])), # south
    ((-1, 0), 0 == len([y for y in range(3) if local_map[y][0]])), # west
    (( 1, 0), 0 == len([y for y in range(3) if local_map[y][2]])), # east
  ]
  possible_moves = possible_moves[(i%4):] + possible_moves[:(i%4)]
  return [m for m, p in possible_moves if p]

def move_elfes(elfes_map, count, start = 0) -> bool:
  i = start
  has_moves = True

  while has_moves and i < count:
    target_positions = {}
    has_moves = False

    for p in elfes_map:
      possible_moves = possible_moves_for(p, elfes_map, i)
      if 0 == len(possible_moves) or 4 == len(possible_moves):
        continue

      t = move(p, possible_moves[0])
      if t in target_positions:
        del target_positions[t]
      else:
        target_positions[t] = p

    for t, c in target_positions.items():
      del elfes_map[c]
      elfes_map[t] = True
      has_moves = True

    if not has_moves:
      return i
    i += 1

def get_bounds(elfes_map):
  start = list(list(elfes_map.keys())[0])
  end = list(start)

  for p in elfes_map:
    if p[0] < start[0]:
      start[0] = p[0]
    if p[0] > end[0]:
      end[0] = p[0]
    if p[1] < start[1]:
      start[1] = p[1]
    if p[1] > end[1]:
      end[1] = p[1]

  return (start, end)

def print_map(elfes_map):
  start, end = get_bounds(elfes_map)
  w = end[0] - start[0] + 1
  h = end[1] - start[1] + 1

  for y in range(h):
    print(''.join([('#' if elfes_map[(x + start[0], y + start[1])] else '.') for x in range(w)]))

def count_empty_tiles(elfes_map):
  start, end = get_bounds(elfes_map)
  w = end[0] - start[0] + 1
  h = end[1] - start[1] + 1

  return sum([sum([(0 if elfes_map[(x + start[0], y + start[1])] else 1) for x in range(w)]) for y in range(h)])

def main(report_result):
  data = [x for x in read_input().split('\n') if x != '']

  elfes_map = mapdict()
  for y in range(len(data)):
    for x in range(len(data[y])):
      if data[y][x] == '#':
        elfes_map[(x,y)] = True

  move_elfes(elfes_map, 10)
  report_result('Empty tiles after 10 rounds:', count_empty_tiles(elfes_map))

  total_moves = move_elfes(elfes_map, 10e5, 10)
  report_result('First moves without changes:', total_moves + 1)

if __name__ == '__main__':
  main(print)
