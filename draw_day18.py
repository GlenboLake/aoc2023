#!/usr/bin/env python3
import sys
import turtle as t


def part1_path(filename):
    headings = {'R': 0, 'L': 180, 'U': 90, 'D': 270}
    with open(filename) as f:
        for line in f:
            heading, distance, *_ = line.split()
            yield headings[heading], int(distance)


def part2_path(filename):
    headings = {'0': 0, '1': 270, '2': 180, '3': 90}
    with open(filename) as f:
        for line in f:
            distance = int(line.strip()[-7:-2], 16)
            heading = headings[line.strip()[-2]]
            yield heading, distance


def draw(path):
    scale, shift = get_scaling(path)
    t.penup()
    t.goto(shift)
    t.pendown()
    for i, (d, dist) in enumerate(path, start=1):
        # print(i)
        t.setheading(d)
        t.forward(dist / scale)


def get_scaling(path):
    left = right = top = bottom = 0
    x, y = 0, 0
    w, h = t.screensize()
    for d, dist in path:
        if d == 0:
            x += dist
            right = max(x, right)
        elif d == 180:
            x -= dist
            left = min(x, left)
        elif d == 90:
            y += dist
            top = max(y, top)
        else:  # d==270
            y -= dist
            bottom = min(y, bottom)
    v_scale = (top - bottom) / (h * 1.5)
    h_scale = (right - left) / (w * 1.5)
    v_offset = (top + bottom) / 2
    h_offset = (right + left) / 2
    scale = max(h_scale, v_scale)
    return scale, (-h_offset/scale, -v_offset/scale)


if __name__ == '__main__':
    match sys.argv[1]:
        case '1':
            path = list(part1_path(sys.argv[2]))
        case '2':
            path = list(part2_path(sys.argv[2]))
        case p:
            raise ValueError(f'Bad part: {p}')
    draw(path)
    t.mainloop()
