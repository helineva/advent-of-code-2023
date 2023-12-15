""" Advent of Code 2023 (https://adventofcode.com/)
    Day 15 Part 1. """
from functools import reduce


def hash_character(initial, c):
    """HASH a single character given an initial value"""
    return (17 * (initial + ord(c))) % 256


def hash_string(s):
    """compute HASH of a string"""
    return reduce(hash_character, s, 0)


def solve_day15_part1():
    """Solve the problem"""

    sum_of_hashes = 0

    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            for step in line.strip().split(","):
                sum_of_hashes += hash_string(step)

    print(sum_of_hashes)


if __name__ == "__main__":
    solve_day15_part1()
