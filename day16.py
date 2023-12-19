from enum import Enum
from functools import total_ordering


@total_ordering
class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def __lt__(self, other):
        ordering = [self.UP, self.DOWN, self.LEFT, self.RIGHT]
        return ordering.index(self) < ordering.index(other)

    def __str__(self):
        return str(self.value)


new_facing = {
    '/': {
        Direction.UP: [Direction.RIGHT],
        Direction.DOWN: [Direction.LEFT],
        Direction.LEFT: [Direction.DOWN],
        Direction.RIGHT: [Direction.UP],
    },
    '\\': {
        Direction.UP: [Direction.LEFT],
        Direction.DOWN: [Direction.RIGHT],
        Direction.LEFT: [Direction.UP],
        Direction.RIGHT: [Direction.DOWN],
    },
    '-': {
        Direction.UP: [Direction.LEFT, Direction.RIGHT],
        Direction.DOWN: [Direction.LEFT, Direction.RIGHT],
        Direction.LEFT: [Direction.LEFT],
        Direction.RIGHT: [Direction.RIGHT],
    },
    '|': {
        Direction.UP: [Direction.UP],
        Direction.DOWN: [Direction.DOWN],
        Direction.LEFT: [Direction.UP, Direction.DOWN],
        Direction.RIGHT: [Direction.UP, Direction.DOWN],
    },
    '.': {
        Direction.UP: [Direction.UP],
        Direction.DOWN: [Direction.DOWN],
        Direction.LEFT: [Direction.LEFT],
        Direction.RIGHT: [Direction.RIGHT],
    }
}


def add_points(a, b):
    return tuple(map(sum, zip(a, b)))


def count_energized_tiles(grid, start_point):
    seen = set()
    beams = {start_point}
    while beams:
        beam = beams.pop()
        if beam in seen:
            continue
        seen.add(beam)
        pos, direction = beam
        new_directions = new_facing[grid[pos]][direction]
        for d in new_directions:
            new_pos = add_points(pos, d.value)
            if new_pos in grid:
                beams.add((new_pos, d))
    return len({pos for pos, d in seen})


def part1(filename):
    with open(filename) as f:
        grid = {
            (r, c): ch
            for r, line in enumerate(f)
            for c, ch in enumerate(line)
            if not ch.isspace()
        }
    return count_energized_tiles(grid, ((0, 0), Direction.RIGHT))


def part2(filename):
    with open(filename) as f:
        grid = {
            (r, c): ch
            for r, line in enumerate(f)
            for c, ch in enumerate(line)
            if not ch.isspace()
        }
    r_max, c_max = max(grid)
    starts = [
        *[((r, 0), Direction.RIGHT) for r in range(r_max + 1)],
        *[((r, c_max), Direction.LEFT) for r in range(r_max + 1)],
        *[((0, c), Direction.DOWN) for c in range(c_max + 1)],
        *[((r_max, c), Direction.UP) for c in range(c_max + 1)],
    ]
    return max(count_energized_tiles(grid, start) for start in starts)


if __name__ == '__main__':
    assert part1('inputs/sample16.txt') == 46
    print('Part 1:', part1('inputs/day16.txt'))
    assert part2('inputs/sample16.txt') == 51
    print('Part 2:', part2('inputs/day16.txt'))
