#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

class Blueprint:
  __regex = re.compile('^Blueprint ([0-9]+): Each ore robot costs ([0-9]+) ore. Each clay robot costs ([0-9]+) ore. Each obsidian robot costs ([0-9]+) ore and ([0-9]+) clay. Each geode robot costs ([0-9]+) ore and ([0-9]+) obsidian.$')

  def __init__(self, data) -> None:
    self.id, ore, clay, obs1, obs2, geo1, geo2 = [int(x) for x in Blueprint.__regex.match(data).groups()]
    self.robots = {
      (1,0,0,0): (-ore, 0, 0, 0),
      (0,1,0,0): (-clay, 0, 0, 0),
      (0,0,1,0): (-obs1, -obs2, 0, 0),
      (0,0,0,1): (-geo1, 0, -geo2, 0),
    }

  def buyable_robots(self, budget):
    return [x for x in self.robots.items() if Blueprint.can_afford(x[1], budget)]

  @staticmethod
  def can_afford(costs, budget):
    return 0 == len([i for i in range(len(costs)) if budget[i] < -costs[i]])

  def affordable_robots(self, budget, gain):
    result = []
    for robot, costs in self.robots.items():
      time = Blueprint.time_to_be_affordable(costs, budget, gain)
      if time >= 0:
        result.append((time, robot, costs))
    return result

  @staticmethod
  def time_to_be_affordable(costs, budget, gain):
    min_rounds = -1

    for i in range(len(costs)):
      if (costs[i] == 0): continue
      if gain[i] == 0: return -1
      min_rounds = max(min_rounds, (budget[i] + costs[i] - gain[i] + 1) // -gain[i])
    return min_rounds

  def __str__(self) -> str:
    return f'Blueprint({self.id}, {self.robots})'

def add(t1, t2):
  if len(t1) != len(t2):
    raise Exception(f'Invalid addition: {t1} + {t2}')
  return tuple([t1[i] + t2[i] for i in range(len(t1))])

def read_input() -> str:
  """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"""
  with open('input.txt') as file:
    return file.read()

def find_maximum_geodes(blueprint: Blueprint, total_time):
  initial_robots = (1,0,0,0)
  empty = (0,0,0,0)

  states = [(initial_robots, empty, 0)]
  weights = [pow(100, i) for i in range(4)]

  for remaining_time in reversed(range(total_time)):
    new_states = []

    for robots, budget, score in states:
      for robot, costs in [(empty, empty)] + blueprint.buyable_robots(budget):
        b = add(add(budget, robots), costs)
        r = add(robots, robot)
        score = sum([weights[i] * (b[i] + r[i] * remaining_time) for i in range(len(budget))])
        new_states.append((r, b, score))

    states = sorted(new_states, key = lambda x : x[2], reverse = True)[:1337]

  best_state = sorted(states, key = lambda x : x[1][-1])[-1]
  return best_state[1][-1]

if __name__ == '__main__':
  blueprints = [Blueprint(x) for x in read_input().split('\n') if x != '']

  total_quality_level = sum([b.id * find_maximum_geodes(b, 24) for b in blueprints])
  print(f'Total quality level in 24 minutes: {total_quality_level}')

  max_geodes = [find_maximum_geodes(b, 32) for b in blueprints[:3]]
  print(f'Product for max geodes in 32 minutes: {max_geodes[0] * max_geodes[1] * max_geodes[2]}')
