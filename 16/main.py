#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

class Valve:
  __regex = re.compile('^Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z, ]+)$')

  def __init__(self, data):
    self.name, flow_rate, targets = Valve.__regex.match(data).groups()
    self.flow_rate = int(flow_rate)
    self.targets = targets.split(', ')

  def __str__(self) -> str:
    return f'Valve({self.name}, {self.flow_rate} -> {self.targets})'

  def __repr__(self) -> str:
    return self.__str__()

class Distances(list):
  def __init__(self, valves):
    self.__distances = dict()

    relevant_valves = [v for v in valves if valves[v].flow_rate > 0]
    for f in ['AA'] + relevant_valves:
      for t in relevant_valves:
        if f != t:
          self[[f, t]] = Distances.__determine_shortest_distance(valves, f, t)

  @staticmethod
  def __determine_shortest_distance(valves, f, t):
    next_valves = valves[f].targets
    pending_valves = []
    visited = [f]

    d = 1
    while len(next_valves) > 0:
      for n in next_valves:
        if n in visited:
          continue

        if n == t:
          return d

        visited.append(n)
        pending_valves += valves[n].targets

      next_valves = pending_valves
      pending_valves = []
      d += 1

    raise Exception(f'No route found from {f} to {t}')

  def __getitem__(self, w):
    return self.__distances[w[0]+w[1]]

  def __setitem__(self, w, v):
    self.__distances[w[0]+w[1]] = v

class Vulcano:
  def __init__(self, data):
    self.valves = { v.name : v for v in [Valve(x) for x in data] }
    self.relevant_valves = [v for v in self.valves if self.valves[v].flow_rate > 0]
    self.distances = Distances(self.valves)

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def find_max_release_alone(vulcano: Vulcano, open_valves: list[str] = [], current_valve = 'AA', remaining_time = 30) -> int:
  valve = vulcano.valves[current_valve]
  open_valves = open_valves + [current_valve]

  max_sub_release = 0

  for next_valve in vulcano.relevant_valves:
    if next_valve in open_valves:
      continue

    distance = vulcano.distances[[current_valve, next_valve]]
    if distance >= remaining_time - 1:
      continue

    release = find_max_release_alone(vulcano, open_valves, next_valve, remaining_time - distance - 1)
    if release > max_sub_release:
      max_sub_release = release

  return valve.flow_rate * remaining_time + max_sub_release

def find_max_release_together(vulcano: Vulcano, is_elefant = False, open_valves: list[str] = [], current_valve = 'AA', remaining_time = 26) -> int:
  valve = vulcano.valves[current_valve]
  open_valves = open_valves + [current_valve]

  max_sub_release = 0

  # If we determine our turn, first check what happens when we stay still
  # and let the elefant do the rest
  if not is_elefant:
    max_sub_release = find_max_release_together(vulcano, True, open_valves)

  # Go through the rest of the open valves and try to open the next
  for next_valve in vulcano.relevant_valves:
    # Valve is already open so there's no use to visit it again
    if next_valve in open_valves:
      continue

    distance = vulcano.distances[[current_valve, next_valve]]
    # We couldn't open the valve in time, so we don't even try
    if distance >= remaining_time - 1:
      continue

    # Determine how much pressure we can release if we go there and open the valve
    release = find_max_release_together(vulcano, is_elefant, open_valves, next_valve, remaining_time - distance - 1)
    if release > max_sub_release:
      max_sub_release = release

  return valve.flow_rate * remaining_time + max_sub_release

def main(report_result):
  data = [x for x in read_input().split('\n') if x != '']
  vulcano = Vulcano(data)

  max_release_alone = find_max_release_alone(vulcano)
  report_result('Maximum release alone:', max_release_alone)

  max_release_together = find_max_release_together(vulcano)
  report_result('Maximum release together:', max_release_together)

if __name__ == '__main__':
  main(print)
