""" Advent of Code 2023 (https://adventofcode.com/)
    Day 4 Part 2. """


def process_card(winning, candidates, i):
    """Process a scratchcard"""
    process_card.count += 1
    hits = 0
    for c in candidates[i]:
        if c in winning[i]:
            hits += 1
    for j in range(i + 1, min(len(winning), i + hits + 1)):
        process_card(winning, candidates, j)


process_card.count = 0


def solve_day4_part2():
    """Solve the problem"""

    winning = []
    candidates = []

    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            _, numbers = line.strip().split(":")
            w, c = numbers.split("|")
            winning.append(w.strip().split())
            candidates.append(c.strip().split())

    for i in range(len(winning)):
        process_card(winning, candidates, i)

    print(process_card.count)


if __name__ == "__main__":
    solve_day4_part2()
