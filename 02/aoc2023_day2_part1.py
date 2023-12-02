""" Advent of Code 2023 (https://adventofcode.com/)
    Day 2 Part 1. """

import re

def solve_day2_part1():
    """ Solve the problem """

    sum_id = 0
    r_max = 12
    g_max = 13
    b_max = 14
    prog_r = re.compile(r"(\d+) r")
    prog_g = re.compile(r"(\d+) g")
    prog_b = re.compile(r"(\d+) b")


    with open("input.txt", "r", encoding="utf-8") as f:
        for count, line in enumerate(f, start=1):
            possible = True
            for grab in line.split(";"):
                match_r = re.search(prog_r, grab)
                match_g = re.search(prog_g, grab)
                match_b = re.search(prog_b, grab)
                if match_r and int(match_r.group(1)) > r_max:
                    possible = False
                    break
                if match_g and int(match_g.group(1)) > g_max:
                    possible = False
                    break
                if match_b and int(match_b.group(1)) > b_max:
                    possible = False
                    break
            if possible:
                sum_id += count

    print(sum_id)

if __name__ == "__main__":
    solve_day2_part1()
