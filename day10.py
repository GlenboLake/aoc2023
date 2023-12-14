from collections import deque
from itertools import chain, zip_longest


def parse_input(filename):
    with open(filename) as f:
        return f.read().splitlines()


def connected(r, c, grid):
    # We have it on good authority that it's a complete
    # loop, so don't bother checking the other tile
    if grid[r][c] in 'J7-':
        yield r, c - 1
    if grid[r][c] in 'FL-':
        yield r, c + 1
    if grid[r][c] in 'LJ|':
        yield r - 1, c
    if grid[r][c] in 'F7|':
        yield r + 1, c


def find_loop(grid):
    start_r, start_c = [(r, line.index('S')) for r, line in enumerate(grid) if 'S' in line].pop()
    connected_neighbors = [
        (r, c) for r, c in [
            (start_r + 1, start_c), (start_r - 1, start_c),
            (start_r, start_c + 1), (start_r, start_c - 1),
        ]
        if (start_r, start_c) in connected(r, c, grid)
    ]
    distances = {
        (start_r, start_c): 0,
        **{
            (r, c): 1 for r, c in connected_neighbors
        }
    }
    to_check = connected_neighbors
    while to_check:
        to_check = [
            neighbor
            for r, c in to_check
            for neighbor in connected(r, c, grid)
            if neighbor not in distances
        ]
        distances.update({
            n: max(distances.values()) + 1
            for n in to_check
        })
    return distances


def print_grid(grid):
    mapping = str.maketrans(dict(zip('SF7LJ-|.', '╬┌┐└┘─│.')))
    for row in grid:
        print(row.translate(mapping))


def part1(filename):
    tiles = parse_input(filename)
    return max(find_loop(tiles).values())


def interleave(a, b):
    return list(chain(*zip_longest(a, b)))[:len(a) + len(b)]


def expand(grid):
    def expand_line(line):
        between = [
            '-' if left in 'SFL-' and right in 'S7J-' else '.'
            for left, right in zip(line, line[1:])
        ]
        return '.' + ''.join(interleave(line, between)) + '.'

    def inserted_line(above, below):
        connections = {i for i, ch in enumerate(above) if ch in 'SF7|'} & {i for i, ch in enumerate(below) if ch in 'SLJ|'}
        return ''.join('|' if i in connections else '.' for i in range(len(above)))

    expanded_lines = [expand_line(l) for l in grid]
    extra_lines = [inserted_line(a, b) for a, b in zip(expanded_lines, expanded_lines[1:])]
    top_bottom = '.' * len(expanded_lines[0])
    return [top_bottom, *interleave(expanded_lines, extra_lines), top_bottom]


def part2(filename):
    grid = parse_input(filename)
    # print('Before filter:')
    # print_grid(grid)
    loop = find_loop(grid)
    filtered = [
        ''.join(
            ch if (r, c) in loop else '.'
            for c, ch in enumerate(line))
        for r, line in enumerate(grid)
    ]
    # print('After filter:')
    # print_grid(filtered)
    # Expand the grid
    expanded = expand(filtered)
    # print('Expanded:')
    # print_grid(expanded)
    # Use BFS to find all "outside" points
    seen = {(0, 0)}
    queue = deque([(0, 0)])
    while queue:
        row, col = queue.popleft()
        for adj in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1), ]:
            r, c = adj
            if adj in seen or r < 0 or c < 0:
                continue
            try:
                if expanded[r][c] == '.':
                    seen.add(adj)
                    queue.append(adj)
            except IndexError:
                continue
    return len([
        1
        for r, line in list(enumerate(expanded))[1::2]
        for c, ch in list(enumerate(line))[1::2]
        if ch == '.' and (r, c) not in seen
    ])


if __name__ == '__main__':
    assert part1('inputs/sample10_1.txt') == 8
    print('Part 1:', part1('inputs/day10.txt'))
    assert part2('inputs/sample10_2.txt') == 10
    print('Part 2:', part2('inputs/day10.txt'))
