#!/usr/bin/env python3
import re
from pprint import pprint
from typing import NamedTuple

class Number(NamedTuple):
	row: int
	col: int
	value: int

	@property
	def length(self):
		return len(str(self.value))

	@property
	def adjacent_area(self):
		return {
			(r,c)
			for r in range(self.row-1, self.row+2)
			for c in range(self.col-1, self.col+self.length+1)
		}

def parse_input(filename):
	nums = []
	symbols = set()
	possible_gears = set()
	with open(filename) as f:
		for r, line in enumerate(f):
			# print(line.rstrip())
			nums.extend([
				Number(r, m.start(), int(m.group()))
				for m in re.finditer(r'\d+', line)
			])
			symbols.update([
				(r, m.start())
				for m in re.finditer(r'[^\d\s\.]', line)
			])
			possible_gears.update([
				(r, m.start())
				for m in re.finditer(r'\*', line)
			])
	return nums, symbols, possible_gears

def part1(filename):
	nums, symbols, _ = parse_input(filename)
	print(len(nums))
	pprint(nums[-5:])
	return sum(num.value for num in nums if bool(num.adjacent_area & symbols))

def part2(filename):
	nums, _, possible_gears = parse_input(filename)
	gears = [
		ns for g in possible_gears
		if len(ns := [n for n in nums if g in n.adjacent_area]) == 2
	]
	return sum(n1.value * n2.value for n1, n2 in gears)

if __name__ == '__main__':
	assert part1('inputs/sample03.txt') == 4361
	print('Part 1:', part1('inputs/day03.txt'))
	assert part2('inputs/sample03.txt') == 467835
	print('Part 2:', part2('inputs/day03.txt'))