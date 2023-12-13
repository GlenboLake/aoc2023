def parse_input(filename):
    with open(filename) as f:
        return {
            (r, c): ch
            for r, line in enumerate(f)
            for c, ch in enumerate(line.strip())
        }


def connected(r, c, tile):
    # We have it on good authority that it's a complete
    # loop, so don't bother checking the other tile
    if tile in 'J7-':
        yield r, c - 1
    if tile in 'FL-':
        yield r, c + 1
    if tile in 'LJ|':
        yield r - 1, c
    if tile in 'F7|':
        yield r + 1, c


def part1(filename):
    tiles = parse_input(filename)
    start_x, start_y = [k for k, v in tiles.items() if v == 'S'].pop()
    connected_neighbors = [
        (r, c) for r, c in [
            (start_x + 1, start_y), (start_x - 1, start_y),
            (start_x, start_y + 1), (start_x, start_y - 1),
        ]
        if (start_x, start_y) in connected(r, c, tiles.get((r, c), '...'))
    ]
    distances = {
        (start_x, start_y): 0,
        **{
            (r, c): 1 for r, c in connected_neighbors
        }
    }
    to_check = connected_neighbors
    while to_check:
        to_check = [
            neighbor
            for r, c in to_check
            for neighbor in connected(r, c, tiles[r, c])
            if neighbor not in distances
        ]
        distances.update({
            n: max(distances.values()) + 1
            for n in to_check
        })
    return max(distances.values())


if __name__ == '__main__':
    assert part1('inputs/sample10.txt') == 8
    print('Part 1:', part1('inputs/day10.txt'))
