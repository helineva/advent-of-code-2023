""" Advent of Code 2023 (https://adventofcode.com/)
    Day 7 Part 2. """
from functools import cmp_to_key


def find_hand_type(hand):
    """Returns hand type
    7: Five of a kind
    6: Four of a kind
    5: Full house
    4: Three of a kind
    3: Two pair
    2: One pair
    1: High card"""
    labels = {}
    jokers = 0
    for card in hand:
        if card == 'J':
            jokers += 1
        else:
            labels[card] = labels.get(card, 0) + 1

    if labels:
        max_label = max(labels, key=labels.get)
        labels[max_label] += jokers
    else:
        labels['A'] = 5

    hand_type = sorted(list(labels.values()))
    if hand_type == [1, 1, 1, 1, 1]:
        return 1
    if hand_type == [1, 1, 1, 2]:
        return 2
    if hand_type == [1, 2, 2]:
        return 3
    if hand_type == [1, 1, 3]:
        return 4
    if hand_type == [2, 3]:
        return 5
    if hand_type == [1, 4]:
        return 6
    if hand_type == [5]:
        return 7


def compare_cards(c1, c2):
    """Comparator for two cards"""
    labels = "J23456789TQKA"
    return labels.index(c1) - labels.index(c2)


def compare_hands(h1, h2):
    """Comparator for two hands"""
    t1 = find_hand_type(h1)
    t2 = find_hand_type(h2)
    if t1 != t2:
        return t1 - t2

    for i in range(5):
        comparison = compare_cards(h1[i], h2[i])
        if comparison != 0:
            return comparison
    return 0


def solve_day7_part2():
    """Solve the problem"""

    data = []

    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            hand, bid = line.strip().split()
            data.append((hand, int(bid)))

    data.sort(key=cmp_to_key(lambda d1, d2: compare_hands(d1[0], d2[0])))

    winnings = 0

    for count, d in enumerate(data):
        winnings += (count + 1) * d[1]

    print(winnings)


if __name__ == "__main__":
    solve_day7_part2()
