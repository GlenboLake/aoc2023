def shoelace(instructions):
    """
    Get the area with the Shoelace Formula

    However, we have to account for the border; each vertex is the
    center of a square meter. To account for this:
    - Every straight edge adds 0.5 to area
    - Every convex corner adds 0.75 to area
    - Every concave corner adds 0.25 to area

    Most concave corners are matched by a convex corner, so the
    0.75/0.25 cancels out and most corners can be considered as adding 0.5
    To get back to the start, there must be 4 extra convex corners,
    where we should add 0.75 instead of 0.5. This is an extra 0.25 for
    each of 4 units, for an additional 1 square meter.

    So to get the total area, we must calculate all vertices as well as the
    length of the perimeter. The total area is:

        shoelace_area + (perimeter_blocks / 2) + 1
    """
    x, y = 0, 0
    vertices = [(x, y)]
    perimeter = 0
    for d, steps in instructions:
        match d:
            case 'L':
                dx, dy = -steps, 0
            case 'R':
                dx, dy = steps, 0
            case 'U':
                dx, dy = 0, steps
            case 'D':
                dx, dy = 0, -steps
            case _:
                raise ValueError('Invalid direction')
        x += dx
        y += dy
        vertices.append((x, y))
        perimeter += steps / 2
    vertices.reverse()
    area = abs(sum(
        x1 * y2 - y1 * x2
        for (x1, y1), (x2, y2) in zip(vertices, vertices[1:])
    ) / 2)
    return int(area + perimeter + 1)


def part1_path(filename):
    with open(filename) as f:
        for line in f:
            direction, steps, *_ = line.split()
            yield direction, int(steps)


def part2_path(filename):
    directions = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            direction = directions[line[-2]]
            steps = int(line[-7:-2], 16)
            yield direction, steps


if __name__ == '__main__':
    assert shoelace(part1_path('inputs/sample18.txt')) == 62
    print('Part 1:', shoelace(part1_path('inputs/day18.txt')))
    assert shoelace(part2_path('inputs/sample18.txt')) == 952408144115
    print('Part 2:', shoelace(part2_path('inputs/day18.txt')))
