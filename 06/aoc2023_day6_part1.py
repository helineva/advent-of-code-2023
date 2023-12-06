""" Advent of Code 2023 (https://adventofcode.com/)
    Day 6 Part 1. """
from math import floor, ceil, sqrt


def solve_day6_part1():
    """Solve the problem"""

    with open("input.txt", "r", encoding="utf-8") as f:
        _, times = f.readline().split(":")
        times = times.strip().split()
        times = [int(t) for t in times]
        _, distances = f.readline().split(":")
        distances = distances.strip().split()
        distances = [int(d) for d in distances]

    product_of_ways = 1
    for i, time in enumerate(times):
        dist = distances[i]
        # quadratic equation in t: -t^2 + time*t - dist = 0
        root_big = (time + sqrt(time * time - 4 * dist)) / 2
        root_small = (time - sqrt(time * time - 4 * dist)) / 2
        difference = floor(root_big) - ceil(root_small) + 1
        product_of_ways *= difference

    print(product_of_ways)


if __name__ == "__main__":
    solve_day6_part1()
