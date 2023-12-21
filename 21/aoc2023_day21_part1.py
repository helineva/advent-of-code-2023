""" Advent of Code 2023 (https://adventofcode.com/)
    Day 21 Part 1. """


def solve_day21_part1():
    """Solve the problem"""

    garden = []
    start = (0, 0)
    steps = 64

    with open("input.txt", "r", encoding="utf-8") as f:
        for row, line in enumerate(f):
            line = line.strip()
            if "S" in line:
                start = (row, line.index("S"))
                line = line.replace("S", ".")
            garden.append(line)

    h = len(garden)
    w = len(garden[0])
    positions = set()
    positions.add(start)

    for _ in range(steps):
        new_positions = set()
        for y, x in positions:
            if y > 0 and garden[y - 1][x] == ".":
                new_positions.add((y - 1, x))
            if y < h - 1 and garden[y + 1][x] == ".":
                new_positions.add((y + 1, x))
            if x > 0 and garden[y][x - 1] == ".":
                new_positions.add((y, x - 1))
            if x < w - 1 and garden[y][x + 1] == ".":
                new_positions.add((y, x + 1))
        positions = new_positions

    print(len(positions))


if __name__ == "__main__":
    solve_day21_part1()
