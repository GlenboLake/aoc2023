import sys
from math import lcm


def parse_input(filename):
    with open(filename) as f:
        turns = f.readline().strip()
        f.readline()

        def parse_line(line):
            label = line[:3]
            left = line[7:10]
            right = line[12:15]
            return label, (left, right)

        return turns, dict(parse_line(line) for line in f)


def part1(filename):
    turns, nodes = parse_input(filename)

    label = 'AAA'
    step_count = 0
    while label != 'ZZZ':
        step = turns[step_count % len(turns)]
        if step == 'L':
            label = nodes[label][0]
        else:
            label = nodes[label][1]
        step_count += 1
    return step_count


def find_cycles(turns, start, node_map):
    seen = {}
    label = start
    turn_index = 0
    t = 0
    first_z = sys.maxsize
    while (label, turn_index) not in seen:
        seen[label, turn_index] = t
        turn = turns[turn_index]
        if turn == 'L':
            label = node_map[label][0]
        else:
            label = node_map[label][1]
        t += 1
        turn_index = (turn_index + 1) % len(turns)
    cycle_length = t - seen[label, turn_index]
    return {first_seen for (node, _), first_seen in seen.items() if node.endswith('Z')}, cycle_length


def part2(filename):
    turns, nodes = parse_input(filename)
    labels = [node for node in nodes if node.endswith('A')]
    cycles = [
        find_cycles(turns, label, nodes)
        for label in labels
    ]
    # It happens to work out that the cycle length and the first time each Z is encountered matches up
    return lcm(*[t for _, t in cycles])


if __name__ == '__main__':
    assert part1('inputs/day08.txt') == 22199  # https://scratch.mit.edu/projects/938158474/
    assert part2('inputs/sample08.txt') == 6
    print('Part 2:', part2('inputs/day08.txt'))