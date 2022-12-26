#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Sprite:
  def __init__(self, data: str) -> None:
    self.data = list(reversed(data.split('\n')))
    self.height = len(self.data)
    self.width = len(self.data[0])

  def can_place_at(self, line, x, y):
    sprite_line = self.data[y]
    for i in range(self.width):
      if sprite_line[i] == '#' and line[x + i] != '.':
        return False
    return True

  def place_at(self, line, x, y):
    line = [x for x in line]
    for i, d in enumerate(self.data[y]):
      if d == '#':
        line[x + i] = '#'

    return ''.join(line)

  def __str__(self) -> str:
    return f'Sprite({self.width}x{self.height} - {self.data})'

  def __repr__(self) -> str:
    return self.__str__()

empty_line = '.......'
sprites = [Sprite(x) for x in """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##""".split('\n\n')]

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def process_wind(w: int, sprite: Sprite, x: int) -> int:
  if x + w < 0 or x + w + sprite.width > 7:
    return x
  return x + w

def can_move_down(sprite: Sprite, x: int, y: int, field: list[str]) -> bool:
  for i in range(sprite.height):
    if len(field) < y + i:
      continue
    if not sprite.can_place_at(field[y + i - 1], x, i):
      return False

  return True

def can_move_sideways(w: int, sprite: Sprite, x: int, y: int, field: list[str]) -> bool:
  if x + w < 0 or x + w + sprite.width > 7:
    return False

  for i in range(sprite.height):
    if len(field) < y + i + 1:
      continue
    if not sprite.can_place_at(field[y + i], x + w, i):
      return False

  # TODO
  return True

def place_sprite(sprite: Sprite, field: list[str], x: int, y: int) -> list[str]:
  while len(field) < y + sprite.height:
    field.append(empty_line)

  for i in range(sprite.height):
    field[y + i] = sprite.place_at(field[y + i], x, i)
  return field

def has_repeating_pattern(matches):
  return find_repeating_pattern(matches) is not None

def find_repeating_pattern(matches):
  diff = set([(matches[i+1][1] - matches[i][1], matches[i+1][2] - matches[i][2]) for i in range(len(matches) - 1)])
  if len(diff) != 1:
    return None

  diff = list(diff)[0]
  return {
    'stone_start': matches[0][1],
    'height_start': matches[0][2],
    'stone_diff': diff[0],
    'height_diff': diff[1],
  }

def process_stones(winds, count):
  field = ['-------']

  current_stone = 0
  current_wind = 0

  patterns = {}
  found_pattern = None

  necessary_count = count
  while current_stone < necessary_count:
    if found_pattern is None:
      key = (current_stone % len(sprites), current_wind)
      current_value = (field[-1], current_stone, len(field))
      if key in patterns:
        patterns[key].append(current_value)
        matches = [p for p in patterns[key] if p[0] == field[-1]]
        if len(matches) >= 3:
          found_pattern = find_repeating_pattern(matches)
          if found_pattern is not None:
            necessary_count = current_stone + ((count - found_pattern['stone_start']) % found_pattern['stone_diff'])
            continue

      else:
        patterns[key] = [current_value]

    current_x = 2
    sprite = sprites[current_stone % len(sprites)]
    for _ in range(4):
      current_x = process_wind(winds[current_wind], sprite, current_x)
      current_wind = (current_wind + 1) % len(winds)

    current_y = len(field)

    while can_move_down(sprite, current_x, current_y, field):
      current_y -= 1
      if can_move_sideways(winds[current_wind], sprite, current_x, current_y, field):
        current_x = process_wind(winds[current_wind], sprite, current_x)
      current_wind = (current_wind + 1) % len(winds)

    # Place sprite
    field = place_sprite(sprite, field, current_x, current_y)

    current_stone += 1

  if found_pattern is None:
    return len(field) - 1

  height_start = found_pattern['height_start']
  height_end = (len(field) - height_start) % found_pattern['height_diff']
  height_repetition = ((count - found_pattern['stone_start']) // found_pattern['stone_diff']) * found_pattern['height_diff']

  return height_start + height_repetition + height_end - 1

def main(report_result):
  winds = [({'>': 1, '<': -1}[x]) for x in read_input().strip()]

  height = process_stones(winds, 2022)
  report_result('Field height after 2022 stones:', height)

  height = process_stones(winds, 1000000000000)
  report_result('Field height after 1000000000000 stones:', height)

if __name__ == '__main__':
  main(print)
