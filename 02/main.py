#!/usr/bin/python3
# -*- coding: utf-8 -*-

point_map = {
  'A': 1, # Rock
  'B': 2, # Paper
  'C': 3, # Scissor
  'X': 1, # Rock
  'Y': 2, # Paper
  'Z': 3, # Scissor
}

win_loose_map = {
  'X': -1, # Loose
  'Y': 0, # Draw
  'Z': 1, # Win
}

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def determine_score_for_round_part_1(input) -> int:
  if len(input) != 2:
    raise Exception(f'Invalid input for round: {input}')

  opponent = point_map[input[0]]
  myself = point_map[input[1]]

  score = ((myself - opponent) + 4) % 3
  # print(f'{input[0]} - {input[1]} -> {score} ({myself - opponent})')

  return myself + score * 3

def determine_score_for_round_part_2(input) -> int:
  if len(input) != 2:
    raise Exception(f'Invalid input for round: {input}')

  opponent = point_map[input[0]]
  win_loose = win_loose_map[input[1]]

  myself = (opponent + win_loose + 2) % 3 + 1

  return myself + (win_loose + 1) * 3

if __name__ == '__main__':
  data = [x.rsplit() for x in read_input().split('\n') if x != '']

  total_score_1 = sum([determine_score_for_round_part_1(x) for x in data])
  print(f'Score for part 1: {total_score_1}')

  total_score_2 = sum([determine_score_for_round_part_2(x) for x in data])
  print(f'Score for part 2: {total_score_2}')
