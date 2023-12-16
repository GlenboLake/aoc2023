import re
import sys
from functools import lru_cache
from io import StringIO
from itertools import combinations

import pytest


def count_arrangements_naive(line, nums):
    unknowns = [i for i, ch in enumerate(line) if ch == '?']
    remaining_damaged = sum(nums) - line.count('#')
    positions = combinations(unknowns, remaining_damaged)
    chunks = [f'#{{{n}}}' for n in nums]
    regex = re.compile(r'\.*' + r'\.+'.join(chunks) + r'\.*')
    result = 0
    for combo in positions:
        new_str = ''.join(
            '#' if i in combo else '.' if i in unknowns else ch
            for i, ch in enumerate(line)
        )
        if regex.fullmatch(new_str):
            result += 1
    return result


@lru_cache
def count_arrangements(line, nums):
    if not nums:
        if '#' in line:
            return 0
        return 1
    # Rightmost option: Pack everything to the right
    packed_width = len('.'.join('#' * n for n in nums))
    right = len(line) - packed_width
    # But if there are any #s, we can't go any farther to the right than the first one
    if '#' in line:
        right = min(right, line.index('#'))
    # Find all places there and farther left where the first number will fit
    lefts = [
        i for i in range(right + 1)
        if re.match(r'[#\?]{{{n}}}(?!#)'.format(n=nums[0]), line[i:])
           and not line[0:i].endswith('#')
    ]
    if not lefts:
        return 0
    # Recursion point
    return sum(
        count_arrangements(line[left + nums[0] + 1:], nums[1:])
        for left in lefts
    )


@pytest.mark.parametrize('line, nums, expected', [
    ('???.###', (1, 1, 3), 1),
    ('.??..??...?##.', (1, 1, 3), 4),
    ('?#?#?#?#?#?#?#?', (1, 3, 1, 6), 1),
    ('????.#...#...', (4, 1, 1), 1),
    ('????.######..#####.', (1, 6, 5), 4),
    ('?###????????', (3, 2, 1), 10),
])
def test_count_arrangements(line, nums, expected):
    result = count_arrangements(line, nums)
    assert result == expected


def parse_input(filename):
    with open(filename) as f:
        for line in f:
            row, nums = line.split()
            nums = tuple([int(n) for n in nums.split(',')])
            yield row, nums


def part1(filename):
    return sum(count_arrangements(line, nums) for line, nums in parse_input(filename))


def test_part1():
    assert part1('inputs/sample12.txt') == 21


def unfold(line):
    return '?'.join(line for _ in range(5))


@pytest.mark.parametrize('line, expected', [
    ('.#', '.#?.#?.#?.#?.#'),
    ('???.###', '???.###????.###????.###????.###????.###'),
])
def test_unfold(line, expected):
    assert unfold(line) == expected


def part2(filename):
    return sum(
        count_arrangements(unfold(line), nums * 5)
        for line, nums in parse_input(filename)
    )


@pytest.mark.parametrize('line, expected', [
    ('???.### 1,1,3', 1),
    ('.??..??...?##. 1,1,3', 16384),
    ('?#?#?#?#?#?#?#? 1,3,1,6', 1),
    ('????.#...#... 4,1,1', 16),
    ('????.######..#####. 1,6,5', 2500),
    ('?###???????? 3,2,1', 506250),
    ('##.?? 2,1', 32)
])
def test_part2_per_line(mocker, line, expected):
    mocker.patch('builtins.open', return_value=StringIO(initial_value=line))
    assert part2('foo') == expected


def test_part2():
    assert part2('inputs/sample12.txt') == 525152


if __name__ == '__main__':
    print('Part 1:', part1('inputs/day12.txt'))
    print('Part 2:', part2('inputs/day12.txt'))
