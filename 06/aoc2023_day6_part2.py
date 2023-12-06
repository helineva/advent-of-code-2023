""" Advent of Code 2023 (https://adventofcode.com/)
    Day 6 Part 2. """
from math import floor, ceil, sqrt


def solve_day6_part2():
    """Solve the problem"""

    with open("input.txt", "r", encoding="utf-8") as f:
        _, time = f.readline().split(":")
        time = time.strip().split()
        time = int("".join(time))
        _, dist = f.readline().split(":")
        dist = dist.strip().split()
        dist = int("".join(dist))

    # quadratic equation in t: -t^2 + time*t - dist = 0
    root_big = (time + sqrt(time * time - 4 * dist)) / 2
    root_small = (time - sqrt(time * time - 4 * dist)) / 2
    difference = floor(root_big) - ceil(root_small) + 1
    print(difference)


if __name__ == "__main__":
    solve_day6_part2()
