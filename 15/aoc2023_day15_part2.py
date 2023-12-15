""" Advent of Code 2023 (https://adventofcode.com/)
    Day 15 Part 2. """
from functools import reduce
import re


def hash_character(initial, c):
    """HASH a single character given an initial value"""
    return (17 * (initial + ord(c))) % 256


def hash_string(s):
    """compute HASH of a string"""
    return reduce(hash_character, s, 0)


def solve_day15_part2():
    """Solve the problem"""

    boxes = [{} for _ in range(256)]

    prog = re.compile(r"([^-=]+)([-=])(\d*)")

    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            for step in line.strip().split(","):
                label, op, focal_length = prog.match(step).groups()
                box = hash_string(label)
                if op == "-":
                    boxes[box].pop(label, None)
                if op == "=":
                    boxes[box][label] = int(focal_length)

    sum_of_focusing_power = 0
    for i, box in enumerate(boxes):
        for j, label in enumerate(box):
            sum_of_focusing_power += (i + 1) * (j + 1) * box[label]

    print(sum_of_focusing_power)


if __name__ == "__main__":
    solve_day15_part2()
