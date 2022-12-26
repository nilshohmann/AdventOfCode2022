#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys
from utils import measure

def execute(day):
  main = __import__(f'{day}.main').main.main
  os.chdir(day)
  measure(main)

def list_available_days():
  dirs = sorted([dir for dir in os.listdir(base_dir) if os.path.isdir(dir) and dir.isnumeric()])
  print('Available days:')
  i = 0
  while len(dirs) > i:
    print('\t'.join(dirs[i:i+5]))
    i += 5

if __name__ == '__main__':
  base_dir = os.path.realpath(os.path.dirname(__file__))
  os.chdir(base_dir)

  if len(sys.argv) >= 2 and sys.argv[-2] == '--day':
    execute(sys.argv[-1])
  else:
    list_available_days()
    day = input('> ')
    execute(day)
