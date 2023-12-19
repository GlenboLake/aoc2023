# Part 1: https://scratch.mit.edu/projects/942011276/
import re


def hohohash(s):
    value = 0
    for char in s:
        value = (value + ord(char)) * 17 % 256
    return value


def part2(filename):
    class Box:
        def __init__(self):
            self.labels = []
            self.focal_lengths = []

        def __len__(self):
            return len(self.labels)

        def add(self, label, focal_length):
            if label in self.labels:
                index = self.labels.index(label)
                self.focal_lengths[index] = focal_length
            else:
                self.labels.append(label)
                self.focal_lengths.append(focal_length)

        def remove(self, label):
            if label in self.labels:
                index = self.labels.index(label)
                self.labels.pop(index)
                self.focal_lengths.pop(index)

        def __str__(self):
            if len(self) == 0:
                return '<EMPTY>'
            items = [f'[{label} {fl}]' for label, fl in zip(self.labels, self.focal_lengths)]
            return ' '.join(items)

        @property
        def focusing_power(self):
            return sum(i * length for i, length in enumerate(self.focal_lengths, start=1))

    def show_boxes():
        nonlocal boxes
        for i, box in enumerate(boxes):
            if len(box) > 0:
                print(f'Box {i}: {box}')

    with open(filename) as f:
        ops = f.read().strip().split(',')
    parse = re.compile(r'(?P<label>\w+)(?P<op>[=-])(?P<focal_length>\d+)?')
    boxes = [Box() for _ in range(256)]

    for op in ops:
        match = parse.fullmatch(op)
        box = boxes[hohohash(match['label'])]
        if match['op'] == '=':
            box.add(match['label'], int(match['focal_length']))
        else:
            box.remove(match['label'])
        # print(f'After "{op}":')
        # show_boxes()
        # print()

    return sum(
        i * box.focusing_power
        for i, box in enumerate(boxes, start=1)
    )


if __name__ == '__main__':
    assert part2('inputs/sample15.txt') == 145
    print('Part 2:', part2('inputs/day15.txt'))
