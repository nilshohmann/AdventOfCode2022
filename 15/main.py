#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

class SensorData:
  __sensor_regex = re.compile('^Sensor at x=(-?[0-9]+), y=(-?[0-9]+): closest beacon is at x=(-?[0-9]+), y=(-?[0-9]+)$')

  def __init__(self, data) -> None:
    match = SensorData.__sensor_regex.match(data)
    if match is None:
      raise Exception(f'Invalid data: {data}')

    sx, sy, bx, by = [int(x) for x in match.groups()]
    self.sensor = [sx, sy]
    self.beacon = [bx, by]
    self.distance = abs(bx - sx) + abs(by - sy)

  def covered_range_at(self, y):
    d = abs(self.sensor[1] - y)
    if d > self.distance:
      return []

    w = self.distance - d
    return [self.sensor[0] - w, self.sensor[0] + w]

  def __str__(self) -> str:
    return f'SensorData({self.sensor} -> {self.beacon} - {self.distance})'

  def __repr__(self) -> str:
    return self.__str__()

def read_input() -> str:
  """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""
  """Sensor at x=2557568, y=3759110: closest beacon is at x=2594124, y=3746832
Sensor at x=2684200, y=1861612: closest beacon is at x=2816974, y=2000000
"""
  with open('input.txt') as file:
    return file.read()

def determine_covered_positions(data, y):
  covered = set()

  for x in data:
    r = x.covered_range_at(y)
    if len(r) > 0:
      covered.update(range(r[0], r[1] + 1))

  return covered

def positions_without_beacon_at(data, y):
  covered_positions = determine_covered_positions(data, y)
  beacons_at_row = set([x.beacon[0] for x in data if x.beacon[1] == y])
  return len(covered_positions) - len(beacons_at_row)

def find_tuning_frequency(data, m):
  possible_signals = []

  for y in range(m + 1):
    signal_ranges = list([x for x in [x.covered_range_at(y) for x in data] if len(x) > 0])
    signal_ranges.sort(key = lambda x : x[0])
    if len(signal_ranges) > 1:
      p = signal_ranges[0]
      for c in signal_ranges[1:]:
        if c[0] > p[1] + 1:
          gap = list(range(p[1] + 1, c[0]))
          if len(gap) == 1:
            possible_signals.append([gap[0], y])
          p = c
        else:
          p[1] = max(p[1], c[1])

  if len(possible_signals) != 1:
    raise Exception(f'Invalid number of possible signals: {possible_signals}')

  return possible_signals[0][0] * m + possible_signals[0][1]

if __name__ == '__main__':
  data = [SensorData(x) for x in read_input().split('\n') if x != '']

  target_y = 2000000
  positions_without_beacon = positions_without_beacon_at(data, target_y)
  print(f'Positions without beacon at {target_y}: {positions_without_beacon}')

  tuning_signal = find_tuning_frequency(data, 4000000)
  print(f'Tuning signal: {tuning_signal}')
