def part1(filename):
    with open(filename) as f:
        # Transpose the grid so we can push them to the left with str.replace
        grid = '\n'.join(''.join(row) for row in zip(*f.read().splitlines()))
    while '.O' in grid:
        grid = grid.replace('.O', 'O.')
    # Transpose again to make enumerating easier
    grid = list(zip(*grid.splitlines()))[::-1]
    return sum(i * row.count('O') for i, row in enumerate(grid, start=1))


def part2(filename):
    pass


if __name__ == '__main__':
    assert part1('inputs/sample14.txt') == 136
    print('Part 1:', part1('inputs/day14.txt'))
    assert part2('inputs/sample14.txt') == 0
    print('Part 2:', part2('inputs/day14.txt'))
