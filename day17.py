import heapq
import sys
import time
from collections import defaultdict
from contextlib import contextmanager
from datetime import timedelta
from typing import Tuple


class Point:
    def __init__(self, *items):
        self.items = items

    def __iter__(self):
        return iter(self.items)

    def __hash__(self):
        return hash(self.items)

    def __eq__(self, other):
        return self.items == other.items

    def __lt__(self, other):
        # assert isinstance(other, Point)
        return self.items < other.items

    def __abs__(self):
        return Point(*(abs(i) for i in self.items))

    def __add__(self, other):
        # assert isinstance(other, Point)
        return Point(*(a + b for a, b in zip(self, other)))

    def __sub__(self, other):
        return self + (-1 * other)

    def __mul__(self, other):
        # assert isinstance(other, typing.SupportsFloat)
        return Point(*(a * other for a in self))

    def __rmul__(self, other):
        return self * other

    def __repr__(self):
        items_str = ', '.join(repr(item) for item in self.items)
        return f'{self.__class__.__name__}({items_str})'


def parse_input(filename):
    with open(filename) as f:
        return {
            Point(r, c): int(ch)
            for r, line in enumerate(f)
            for c, ch in enumerate(line)
            if not ch.isspace()
        }


State = Tuple[int, Point, Point]


def solve(grid, min_movement, max_movement):
    start_pos = min(grid)
    goal = max(grid)

    def dist_to_goal(pos: Point):
        return sum(goal - pos)

    queue = [
        (dist_to_goal(start_pos), 0, start_pos, Point(0, 1)),
        (dist_to_goal(start_pos), 0, start_pos, Point(1, 0)),
    ]
    scores = defaultdict(lambda: sys.maxsize)
    while queue:
        heuristic, heat_loss, pos, direction = heapq.heappop(queue)
        if heuristic > scores[pos, direction]:
            continue
        if dist_to_goal(pos) == 0:
            return heat_loss
        dx, dy = direction
        for new_dir in [Point(dy, dx), Point(-dy, -dx)]:
            added_heat_loss = 0
            for dist in range(1, max_movement + 1):
                new_pos = pos + dist * new_dir
                try:
                    added_heat_loss += grid[new_pos]
                except KeyError:
                    break
                if dist < min_movement:
                    continue
                new_heat_loss = heat_loss + added_heat_loss
                new_heuristic = dist_to_goal(new_pos) + new_heat_loss
                new_state = new_heuristic, new_heat_loss, new_pos, abs(new_dir)
                if new_state in queue or new_heuristic > scores[new_pos, abs(new_dir)]:
                    continue
                scores[new_pos, abs(new_dir)] = new_heuristic
                heapq.heappush(queue, new_state)


def part1(filename):
    grid = parse_input(filename)
    return solve(grid, 1, 3)


def part2(filename):
    grid = parse_input(filename)
    return solve(grid, 4, 10)


@contextmanager
def timed():
    start = time.time()
    yield
    end = time.time()
    print(f'Took {timedelta(seconds=end - start)}')


if __name__ == '__main__':
    assert part1('inputs/sample17.txt') == 102
    with timed():
        print('Part 1:', part1('inputs/day17.txt'))
    assert part2('inputs/sample17.txt') == 94
    assert part2('inputs/sample17_2.txt') == 71
    with timed():
        print('Part 2:', part2('inputs/day17.txt'))
