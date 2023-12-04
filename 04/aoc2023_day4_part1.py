""" Advent of Code 2023 (https://adventofcode.com/)
    Day 4 Part 1. """


def solve_day4_part1():
    """Solve the problem"""
    sum_points = 0

    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            _, numbers = line.strip().split(":")
            winning, candidates = numbers.split("|")
            winning = winning.strip().split()
            candidates = candidates.strip().split()
            hits = 0
            for c in candidates:
                if c in winning:
                    hits += 1
            if hits > 0:
                sum_points += 2 ** (hits - 1)

    print(sum_points)


if __name__ == "__main__":
    solve_day4_part1()
