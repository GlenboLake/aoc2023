from itertools import chain


class Mapping:
    def __init__(self, *map_lines):
        self.segments = [self._parse_line(line) for line in map_lines]
        self.segments.sort(key=lambda r: r.start)

    @staticmethod
    def _parse_line(line):
        dest, src, size = map(int, line.split())
        return range(src, src + size), range(dest, dest + size)

    def convert(self, value):
        for in_range, out_range in self.segments:
            if value in in_range:
                return out_range[in_range.index(value)]
        return value


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
    print(sum(sizes))
    seeds = chain.from_iterable([range(start, start+size) for start, size in zip(starts, sizes)])
    return min(almanac.get_location(seed) for seed in seeds)


if __name__ == '__main__':
    assert part1('inputs/sample05.txt') == 35
    print('Part 1:', part1('inputs/day05.txt'))
    assert part2('inputs/sample05.txt') == 46
    print('Part 2:', part2('inputs/day05.txt'))
