from collections import Counter


def parse_input(filename):
    with open(filename) as f:
        for line in f:
            hand, bid = line.split()
            yield hand, int(bid)


def solve(filename, score_func):
    hands = list(parse_input(filename))
    hands.sort(key=score_func)
    return sum(i * bid for i, (_, bid) in enumerate(hands, start=1))


hand_type_ranks = {
    (5,): 7,  # Five of a kind
    (1, 4): 6,  # Four of a kind
    (2, 3): 5,  # Full house
    (1, 1, 3): 4,  # Three of a kind
    (1, 2, 2): 3,  # Two pair
    (1, 1, 1, 2): 2,  # Pair
    (1, 1, 1, 1, 1): 1,  # High card
}


def part1(filename):
    def score(hand_and_bid):
        card_values = '23456789TJQKA'
        hand, _ = hand_and_bid
        rank = hand_type_ranks[tuple(sorted(Counter(hand).values()))]
        return rank, *[card_values.index(card) for card in hand]

    return solve(filename, score)


def part2(filename):
    def score(hand_and_bid):
        card_values = 'J23456789TQKA'
        hand, _ = hand_and_bid
        num_jokers = hand.count('J')
        other_cards = [card for card in hand if card != 'J']
        counts = sorted(Counter(other_cards).values())
        if counts:
            adjusted_counts = counts[:-1] + [counts[-1] + num_jokers]
        else:
            # Avoid IndexError for JJJJJ hand
            adjusted_counts = [num_jokers]
        rank = hand_type_ranks[tuple(adjusted_counts)]
        return rank, *[card_values.index(card) for card in hand]

    return solve(filename, score)


if __name__ == '__main__':
    assert part1('inputs/sample07.txt') == 6440
    print('Part 1:', part1('inputs/day07.txt'))
    assert part2('inputs/sample07.txt') == 5905
    print('Part 2:', part2('inputs/day07.txt'))
