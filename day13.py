import sys


def parse_input(filename):
    with open(filename) as f:
        return [chunk.splitlines() for chunk in f.read().split('\n\n')]


def detect_vertical_symmetry(pattern):
    return detect_horizontal_symmetry(list(zip(*pattern)))


def detect_horizontal_symmetry(pattern):
    symmetry_lines = [
        i+1
        for i in range(len(pattern)-1)
        if all(l == r for l, r in zip(
            pattern[i::-1],
            pattern[i + 1:]
        ))
    ]
    if not symmetry_lines:
        return None, sys.maxsize
    symmetry_scores = {
        i: abs(i - len(pattern)/2)
        for i in symmetry_lines
    }

    return min(symmetry_scores.items(), key=lambda x: x[1])


def score_symmetry(pattern):
    v, vs = detect_vertical_symmetry(pattern)
    h, hs = detect_horizontal_symmetry(pattern)
    if vs < hs:
        return v
    else:
        return h * 100


def part1(filename):
    patterns = parse_input(filename)
    return sum(score_symmetry(pattern) for pattern in patterns)


if __name__ == '__main__':
    assert part1('inputs/sample13.txt') == 405
    print('Part 1:', part1('inputs/day13.txt'))
