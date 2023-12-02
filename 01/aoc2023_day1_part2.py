""" Advent of Code 2023 (https://adventofcode.com/)
    Day 1 Part 2. """
import re


def solve_day1_part2():
    """Solve the problem"""
    digits_in_letters = [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]
    digits_in_letters_rev = [s[::-1] for s in digits_in_letters]
    prog = re.compile("[1-9]|" + "|".join(digits_in_letters))
    prog_rev = re.compile("[1-9]|" + "|".join(digits_in_letters_rev))

    sum_cv = 0

    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            first = re.search(prog, line).group(0)
            if first.isdecimal():
                first = int(first)
            else:
                first = digits_in_letters.index(first) + 1

            second = re.search(prog_rev, line[::-1]).group(0)
            if second.isdecimal():
                second = int(second)
            else:
                second = digits_in_letters_rev.index(second) + 1
            sum_cv += 10 * first + second

    print(sum_cv)


if __name__ == "__main__":
    solve_day1_part2()
