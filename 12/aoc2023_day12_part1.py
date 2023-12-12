""" Advent of Code 2023 (https://adventofcode.com/)
    Day 12 Part 1. (naive brute force, very slow) """
from itertools import product


def fill_row(r, s):
    """replaces ?'s in a row r by characters in s"""
    output = []
    i = 0
    for c in r:
        if c == "?":
            output.append(s[i])
            i += 1
        else:
            output.append(c)
    return "".join(output)


def compute_groups(r):
    """computes group arrangement for a given filled (without ?'s) row"""
    arr = []
    i = 0
    b = False
    l = 0
    while i < len(r):
        if r[i] == "#":
            if b:
                l += 1
            else:
                b = True
                l = 1
        else:
            if b:
                arr.append(l)
                b = False
        i += 1

    if b:
        arr.append(l)

    return arr


def solve_day12_part1():
    """Solve the problem"""

    count = 0
    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            row, groups = line.strip().split()
            groups = [int(n) for n in groups.split(",")]
            for p in product(".#", repeat=row.count("?")):
                if compute_groups(fill_row(row, p)) == groups:
                    count += 1

    print(count)


if __name__ == "__main__":
    solve_day12_part1()
