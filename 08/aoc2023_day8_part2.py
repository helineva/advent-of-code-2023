""" Advent of Code 2023 (https://adventofcode.com/)
    Day 8 Part 1. """
from math import lcm


def solve_day8_part2():
    """Solve the problem"""

    left = {}
    right = {}

    with open("input.txt", "r", encoding="utf-8") as f:
        instructions = f.readline().strip()
        for line in f:
            if line.isspace():
                continue
            node, leftright = line.strip().split("=")
            node = node.strip()
            l, r = leftright.strip(" ()").split(",")
            l = l.strip()
            r = r.strip()
            left[node] = l
            right[node] = r

    cycle_lengths = []
    length = len(instructions)

    for current in left:
        if not current.endswith("A"):
            continue
        count = 0
        while not current.endswith("Z"):
            instruction = instructions[count % length]
            if instruction == "L":
                current = left[current]
            else:
                current = right[current]
            count += 1
        cycle_lengths.append(count)

    print(lcm(*cycle_lengths))


if __name__ == "__main__":
    solve_day8_part2()
