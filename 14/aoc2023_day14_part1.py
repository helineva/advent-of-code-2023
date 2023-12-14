""" Advent of Code 2023 (https://adventofcode.com/)
    Day 14 Part 1. """


def solve_day14_part1():
    """Solve the problem"""

    platform = []
    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            platform.append(line.strip())

    total_load = 0
    for col in range(len(platform[0])):
        load = len(platform)
        for row in range(len(platform)):
            if platform[row][col] == "O":
                total_load += load
                load -= 1
            elif platform[row][col] == "#":
                load = len(platform) - row - 1

    print(total_load)


if __name__ == "__main__":
    solve_day14_part1()
