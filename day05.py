from typing import Iterable

from util import flatten


def range_overlap(r1: range, r2: range):
    left = max(r1.start, r2.start)
    right = min(r1.stop, r2.stop)
    return range(left, right)


def split_range(r: range, buckets: Iterable[range]):
    overlaps = {
        overlap.start: overlap
        for b in buckets
        if len(overlap := range_overlap(r, b)) > 0
    }
    if not overlaps:
        return [r]
    new_ranges = []
    i = r.start
    while i < r.stop:
        if i in overlaps:
            new_ranges.append(overlaps[i])
            i = new_ranges[-1].stop
        else:
            new_stop = min([k for k in overlaps if k > i] or [r.stop])
            new_ranges.append(range(i, new_stop))
            i = new_stop
    assert sum(len(nr) for nr in new_ranges) == len(r)
    return new_ranges


def merge_ranges(*ranges: range):
    def merge_two_ranges(r1: range, r2: range):
        if r1.stop == r2.start:
            return [range(r1.start, r2.stop)]
        else:
            return [r1, r2]
    new_ranges = [ranges[0]]
    for r in ranges[1:]:
        new_ranges[-1:] = merge_two_ranges(new_ranges[-1], r)
    return new_ranges


class Mapping:
    def __init__(self, *map_lines):
        self.segments = [self._parse_line(line) for line in map_lines]
        self.segments.sort(key=lambda rs: rs[0].start)

    def __str__(self):
        return ', '.join(
            f'{min(s)}..{max(s)}'
            for s, _ in self.segments
        )

    @staticmethod
    def _parse_line(line):
        dest, src, size = map(int, line.split())
        return range(src, src + size), range(dest, dest + size)

    def convert(self, value):
        for in_range, out_range in self.segments:
            if value in in_range:
                return out_range[in_range.index(value)]
        return value

    def convert_range(self, r):
        pass
        new_ranges = split_range(r, [src for src, dest in self.segments])
        return [
            range(self.convert(r.start), self.convert(r.stop-1)+1)
            for r in new_ranges
        ]


class Almanac:
    def __init__(self, stages: list[Mapping]):
        self.stages = stages

    def add_stage(self, stage: Mapping):
        self.stages.append(stage)

    def get_location(self, seed):
        for stage in self.stages:
            seed = stage.convert(seed)
        return seed


def parse_input(filename):
    with open(filename) as f:
        seeds = [int(x) for x in f.readline().split()[1:]]
        f.readline()
        sections = f.read().split('\n\n')
    return seeds, Almanac([Mapping(*section.splitlines()[1:]) for section in sections])


def part1(filename):
    seeds, almanac = parse_input(filename)
    return min(almanac.get_location(seed) for seed in seeds)


def part2(filename):
    seed_ranges, almanac = parse_input(filename)
    starts = seed_ranges[0::2]
    sizes = seed_ranges[1::2]
    ranges = [range(start, start+size) for start, size in zip(starts, sizes)]
    ranges.sort(key=lambda r: r.start)
    for stage in almanac.stages:
        ranges = [stage.convert_range(r) for r in ranges]
        ranges = merge_ranges(*sorted(flatten(ranges), key=lambda r: r.start))
    return min(r.start for r in ranges)


if __name__ == '__main__':
    assert part1('inputs/sample05.txt') == 35
    print('Part 1:', part1('inputs/day05.txt'))
    assert part2('inputs/sample05.txt') == 46
    print('Part 2:', part2('inputs/day05.txt'))
