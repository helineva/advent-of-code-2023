""" Advent of Code 2023 (https://adventofcode.com/)
    Day 2 Part 2. """

import re


def solve_day2_part2():
    """Solve the problem"""
    sum_power = 0
    prog_r = re.compile(r"(\d+) r")
    prog_g = re.compile(r"(\d+) g")
    prog_b = re.compile(r"(\d+) b")

    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            r_min = 0
            g_min = 0
            b_min = 0
            for grab in line.split(";"):
                match_r = re.search(prog_r, grab)
                match_g = re.search(prog_g, grab)
                match_b = re.search(prog_b, grab)
                if match_r:
                    r = int(match_r.group(1))
                    if r > r_min:
                        r_min = r
                if match_g:
                    g = int(match_g.group(1))
                    if g > g_min:
                        g_min = g
                if match_b:
                    b = int(match_b.group(1))
                    if b > b_min:
                        b_min = b
            sum_power += r_min * g_min * b_min

    print(sum_power)


if __name__ == "__main__":
    solve_day2_part2()
