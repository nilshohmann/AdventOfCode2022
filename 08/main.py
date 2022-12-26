#!/usr/bin/python3
# -*- coding: utf-8 -*-

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def is_visible(x, y, grid) -> bool:
  height = grid[y][x]

  hiding_trees = [
    len([i for i in range(0, y) if grid[i][x] >= height]),
    len([i for i in range(0, x) if grid[y][i] >= height]),
    len([i for i in range(x + 1, len(grid)) if grid[y][i] >= height]),
    len([i for i in range(y + 1, len(grid)) if grid[i][x] >= height]),
  ]

  return len([x for x in hiding_trees if x == 0]) > 0

def count_visible_trees(trees, height):
  count = 0

  for t in trees:
    count = count + 1
    if t >= height:
      break

  return count

def determine_scenic_score(x, y, grid) -> int:
  height = grid[y][x]

  scores = [
    count_visible_trees(reversed([grid[i][x] for i in range(0, y)]), height),
    count_visible_trees(reversed([grid[y][i] for i in range(0, x)]), height),
    count_visible_trees([grid[y][i] for i in range(x + 1, len(grid))], height),
    count_visible_trees([grid[i][x] for i in range(y + 1, len(grid))], height),
  ]

  return scores[0] * scores[1] * scores[2] * scores[3]

def main(report_result):
  grid = [x for x in read_input().split('\n') if x != '']

  number_of_visible_trees = sum([sum([is_visible(x, y, grid) for x in range(len(grid))]) for y in range(len(grid))])
  report_result('Number of visible trees:', number_of_visible_trees)

  scores = [[determine_scenic_score(x, y, grid) for x in range(len(grid))] for y in range(len(grid))]
  report_result('Highest score:', max([max(x) for x in scores]))

if __name__ == '__main__':
  main(print)
