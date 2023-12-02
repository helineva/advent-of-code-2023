""" Advent of Code 2023 (https://adventofcode.com/)
    Day 1 Part 1. """


def solve_day1_part1():
    """Solve the problem"""

    sum_cv = 0

    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            for c in line:
                if c.isdecimal():
                    sum_cv += 10 * int(c)
                    break
            for c in line[::-1]:
                if c.isdecimal():
                    sum_cv += int(c)
                    break

    print(sum_cv)


if __name__ == "__main__":
    solve_day1_part1()
