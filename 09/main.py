#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Positions:
  def __init__(self) -> None:
    self.positions = []

  def add(self, position):
    if not position in self.positions:
      self.positions.append(position)

  def __str__(self) -> str:
    return f'Positions({self.positions})'

  def __repr__(self) -> str:
    return self.__str__()

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def convert_command(data):
  d, c = data.split(' ')
  if d == 'U':
    return [[0,1] for i in range(int(c))]
  if d == 'D':
    return [[0,-1] for i in range(int(c))]
  if d == 'R':
    return [[1,0] for i in range(int(c))]
  if d == 'L':
    return [[-1,0] for i in range(int(c))]
  raise Exception(f'Invalid command: {data}')

def move(p, o):
  return [p[0] + o[0], p[1] + o[1]]

def adjust_tail(tail, head):
  dx = head[0] - tail[0]
  dy = head[1] - tail[1]
  if abs(dx) > 2 or abs(dy) > 2:
    raise Exception(f'Invalid state: {head} - {tail}')

  if abs(dx) > 1 or abs(dy) > 1:
    return [tail[0] + round(dx * 0.6), tail[1] + round(dy * 0.6)]

  return tail

if __name__ == '__main__':
  data = [x for x in read_input().split('\n') if x != '']
  # print(input)

  head = [0,0]
  tail = [0,0]
  positions = Positions()

  for x in data:
    for action in convert_command(x):
      head = move(head, action)
      tail = adjust_tail(tail, head)
      positions.add(tail)

  print(f'Number of fields visited by tail: {len(positions.positions)}')

  knots = [[0,0] for i in range(10)]
  positions = Positions()

  for x in data:
    for action in convert_command(x):
      #print(knots)
      #print(action)

      knots[0] = move(knots[0], action)
      for i in range(1, len(knots)):
        knots[i] = adjust_tail(knots[i], knots[i - 1])
        # print(knots[i])
      positions.add(knots[-1])

  print(f'Number of fields visited by last knot: {len(positions.positions)}')
