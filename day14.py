def rotate_string_ccw(s):
    transposed = [''.join(row) for row in zip(*s.splitlines())]
    flipped = reversed(transposed)
    return '\n'.join(flipped)


def rotate_string_cw(s):
    flipped = reversed(s.splitlines())
    transposed = [''.join(row) for row in zip(*flipped)]
    return '\n'.join(transposed)


def part1(filename):
    with open(filename) as f:
        # Rotate input so north is to the left
        grid = rotate_string_ccw(f.read())
    while '.O' in grid:
        grid = grid.replace('.O', 'O.')
    # Rotate CCW once more so north is at the bottom to make enumerating easier
    grid = rotate_string_ccw(grid)
    return sum(i * row.count('O') for i, row in enumerate(grid.splitlines(), start=1))


def part2(filename):
    with open(filename) as f:
        grid = f.read()
    # Rotate 180 to prepare rotation
    grid = rotate_string_cw(rotate_string_cw(grid))
    history = {grid: 0}
    for i in range(1, 1_000_000_001):
        for _ in range(4):
            grid = rotate_string_cw(grid)
            while '.O' in grid:
                grid = grid.replace('.O', 'O.')
        if grid in history:
            break
        history[grid] = i
    cycle_start = history[grid]
    cycle_length = i - cycle_start
    result = 1_000_000_000 % cycle_length
    while result < cycle_start:
        result += cycle_length
    assert result in history.values()
    final_grid = {k for k, v in history.items() if v == result}.pop()
    return sum(i * row.count('O') for i, row in enumerate(final_grid.splitlines(), start=1))


if __name__ == '__main__':
    assert rotate_string_ccw('ab\ncd') == 'bd\nac'
    assert rotate_string_cw('ab\ncd') == 'ca\ndb'
    assert rotate_string_cw(rotate_string_ccw('ab\ncd')) == 'ab\ncd'
    assert part1('inputs/sample14.txt') == 136
    print('Part 1:', part1('inputs/day14.txt'))
    assert part2('inputs/sample14.txt') == 64
    print('Part 2:', part2('inputs/day14.txt'))
