""" Advent of Code 2023 (https://adventofcode.com/)
    Day 3 Part 1. """
import re


def check_for_symbols(s):
    """Check if a string contains any symbols"""
    nonsymbols = ".0123456789"
    for c in s:
        if c not in nonsymbols:
            return True
    return False


def solve_day3_part1():
    """Solve the problem"""

    sum_part_numbers = 0

    with open("input.txt", "r", encoding="utf-8") as f:
        schematic = [line.strip() for line in f]

    prog = re.compile(r"\d+")
    for i, line in enumerate(schematic):
        for match in prog.finditer(line):
            neighborhood = ""
            if i > 0:
                neighborhood += schematic[i - 1][
                    max(0, match.start() - 1) : min(
                        len(schematic[i - 1]), match.end() + 1
                    )
                ]
            if i < len(schematic) - 1:
                neighborhood += schematic[i + 1][
                    max(0, match.start() - 1) : min(
                        len(schematic[i - 1]), match.end() + 1
                    )
                ]
            if match.start() > 0:
                neighborhood += schematic[i][match.start() - 1]
            if match.end() < len(schematic[i]) - 1:
                neighborhood += schematic[i][match.end()]
            if check_for_symbols(neighborhood):
                sum_part_numbers += int(match.group())
    print(sum_part_numbers)


if __name__ == "__main__":
    solve_day3_part1()
