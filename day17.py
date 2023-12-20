import sys
from collections import deque
from typing import Tuple


def parse_input(filename):
    with open(filename) as f:
        return {
            (r, c): int(ch)
            for r, line in enumerate(f)
            for c, ch in enumerate(line)
            if not ch.isspace()
        }


def add_points(a: Tuple[int, int], b: Tuple[int, int]):
    return a[0]+b[0], a[1]+b[1]


State = Tuple[Tuple[int, int], Tuple[int, int], int]


def part1(filename):
    grid = parse_input(filename)
    # State: Position, direction facing, and how long we've gone straight
    start = (0, 0), (0, 1), 0
    target_pos = max(grid)
    history: dict[State, int] = {
        start: 0
    }
    queue = deque([start])
    while queue:
        print(len(queue))
        state = queue.popleft()
        score = history[state]
        pos, d, streak = state
        dx, dy = d
        next_states: list[State] = [
            (add_points(pos, new_dir), new_dir, 1)
            for new_dir in [(dy, dx), (-dy, -dx)]
        ]
        if streak < 3:
            next_states.append(
                (add_points(pos, d), d, streak + 1)
            )
        new_state: State
        for new_state in next_states:
            new_pos, new_d, new_streak = new_state
            if new_pos not in grid:
                continue
            new_score = score + grid[new_pos]
            if history.get(new_state, sys.maxsize) < new_score:
                continue
            history[new_state] = new_score
            if new_pos != target_pos:
                if new_state not in queue:
                    queue.append(new_state)
    return min(score for (pos, _, _), score in history.items() if pos == target_pos)


if __name__ == '__main__':
    assert part1('inputs/sample17.txt') == 102
    print('Part 1:', part1('inputs/day17.txt'))
