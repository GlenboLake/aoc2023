def parse_input(filename):
    with open(filename) as f:
        return {
            (r, c)
            for r, line in enumerate(f)
            for c, char in enumerate(line)
            if char == '#'
        }


def solve(filename, expansion_rate=1):
    galaxies = parse_input(filename)
    total_distance = sum(
        abs(c2 - c1) + abs(r2 - r1)
        for r1, c1 in galaxies
        for r2, c2 in galaxies
    ) // 2
    rows = {r for r, c in galaxies}
    cols = {c for r, c in galaxies}

    def galaxies_above(row):
        return len([1 for r, c in galaxies if r < row])

    def galaxies_below(row):
        return len([1 for r, c in galaxies if r > row])

    def galaxies_left(col):
        return len([1 for r, c in galaxies if c < col])

    def galaxies_right(col):
        return len([1 for r, c in galaxies if c > col])

    for r in range(min(rows), max(rows)):
        if r not in rows:
            total_distance += galaxies_above(r) * galaxies_below(r) * (expansion_rate - 1)
    for c in range(min(cols), max(cols)):
        if c not in cols:
            total_distance += galaxies_left(c) * galaxies_right(c) * (expansion_rate - 1)
    return total_distance


def part1(filename):
    return solve(filename, expansion_rate=2)


def part2(filename, er):
    return solve(filename, expansion_rate=er)


if __name__ == '__main__':
    assert part1('inputs/sample11.txt') == 374
    print('Part 1:', part1('inputs/day11.txt'))
    assert part2('inputs/sample11.txt', 10) == 1030
    assert part2('inputs/sample11.txt', 100) == 8410
    print('Part 2:', part2('inputs/day11.txt', 1_000_000))
