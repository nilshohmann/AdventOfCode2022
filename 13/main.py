#!/usr/bin/python3
# -*- coding: utf-8 -*-

digit_chars = [f'{i}' for i in range(10)]

def read_input() -> str:
  with open('input.txt') as file:
    return file.read()

def determine_order(left, right):
  if not isinstance(left, list) and not isinstance(right, list):
    if left == right:
      return 0
    if left < right:
      return 1
    if left > right:
      return -1

  if isinstance(left, list) and not isinstance(right, list):
    return determine_order(left, [right])
  if not isinstance(left, list) and isinstance(right, list):
    return determine_order([left], right)

  if len(left) == 0:
    if (len(right) == 0):
      return 0
    return 1
  if len(right) == 0:
    return -1

  r = determine_order(left[0], right[0])
  if r == 0:
    return determine_order(left[1:], right[1:])
  if r == 1:
    return 1
  return -1

def is_in_correct_order(left, right):
  return determine_order(left, right) >= 0

def parse(data):
  i = 0

  if data[0] == '[':
    result = []
    i = i + 1

    while i < len(data):
      if data[i] == ']':
        return [i + 1, result]

      c, r = parse(data[i:])
      result.append(r)
      i = i + c

      if data[i] == ',':
        i = i + 1

    raise Exception('Closing parenthises not found')

  value = ''
  while data[len(value)] in digit_chars:
    value = value + data[len(value)]
  return [len(value), int(value)]

def parse_pair(data):
  data = [parse(x)[1] for x in data.split('\n') if x != '']
  return data

def bubble_sort(array: list, comparator):
	new_array = [e for e in array]

	while True:
		swapped = False
		for i in range(0, len(new_array) - 1):
			if comparator(new_array[i+1], new_array[i]):
				new_array[i], new_array[i+1] = new_array[i+1], new_array[i] # Swap elements that are out of order
				swapped = True

		if not swapped:
			break

	return new_array

def join_lists(lists):
  result = []
  for x in lists:
    result = result + x
  return result

if __name__ == '__main__':
  data = [parse_pair(x) for x in read_input().split('\n\n') if x != '']

  relevant_indices = [(i + 1 if is_in_correct_order(x[0], x[1]) else 0) for i, x in enumerate(data)]
  print(f'Sum of indices: {sum(relevant_indices)}')

  divider_packets = [
    [[2]],
    [[6]]
  ]
  data = join_lists(data) + divider_packets
  ordered_packets = bubble_sort(data, lambda left, right : is_in_correct_order(left, right))

  dividers = [i + 1 for i, x in enumerate(ordered_packets) if x in divider_packets]
  print(f'Decoder key: {dividers[0] * dividers[1]}')
