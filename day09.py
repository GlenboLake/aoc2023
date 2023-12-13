from functools import reduce


def parse_input(filename):
    with open(filename) as f:
        return [
            [int(x) for x in line.split()]
            for line in f
        ]


def extrapolate(history):
    diffs = [history]
    while set(diffs[-1]) != {0}:
        new_layer = [b - a for a, b in zip(diffs[-1], diffs[-1][1:])]
        diffs.append(new_layer)
    future = sum(layer[-1] for layer in diffs)
    past = reduce(lambda a, b: b - a, [layer[0] for layer in reversed(diffs)])
    return future, past


def solve(filename):
    histories = parse_input(filename)
    part1, part2 = list(zip(*[extrapolate(h) for h in histories]))
    return sum(part1), sum(part2)


if __name__ == '__main__':
    assert solve('inputs/sample09.txt') == (114, 2)
    answer1, answer2 = solve('inputs/day09.txt')
    print('Part 1:', answer1)
    print('Part 2:', answer2)
