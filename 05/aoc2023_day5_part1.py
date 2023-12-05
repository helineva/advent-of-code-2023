""" Advent of Code 2023 (https://adventofcode.com/)
    Day 5 Part 1. """


def solve_day5_part1():
    """Solve the problem"""

    seeds = []
    mappings = []

    with open("input.txt", "r", encoding="utf-8") as f:
        line = f.readline()
        _, seeds = line.split(':')
        seeds = seeds.strip().split()
        seeds = [int(s) for s in seeds]
        for line in f:
            if "map" in line:
                mappings.append([])
                continue
            if not line.isspace():
                t = [int(s) for s in line.strip().split()]
                mappings[-1].append(t)

    locations = []
    for s in seeds:
        for mapping in mappings:
            for t in mapping:
                dest_start, source_start, length = t[0], t[1], t[2]
                if s >= source_start and s < source_start + length:
                    s = dest_start + s - source_start
                    break
        locations.append(s)

    print(min(locations))

if __name__ == "__main__":
    solve_day5_part1()
