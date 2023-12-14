""" Advent of Code 2023 (https://adventofcode.com/)
    Day 14 Part 2. """


def transpose(platform):
    """returns the transpose (rows to cols and vice versa) of platform"""
    tp = []
    h = len(platform)
    w = len(platform[0])

    for j in range(w):
        col = []
        for i in range(h):
            col.append(platform[i][j])
        tp.append("".join(col))

    return tp


def tilt(platform, direction):
    """returns a new platform resulting from tilting "platform"
    to the direction given by "direction" ("L" or "R")"""
    tilted = []
    for row in platform:
        new_row = []
        no_of_empty = 0
        no_of_rocks = 0
        for c in row:
            if c == "#":
                if direction == "L":
                    new_row += ["O"] * no_of_rocks + ["."] * no_of_empty + ["#"]
                else:
                    new_row += ["."] * no_of_empty + ["O"] * no_of_rocks + ["#"]
                no_of_empty = 0
                no_of_rocks = 0
            if c == ".":
                no_of_empty += 1
            if c == "O":
                no_of_rocks += 1
        if direction == "L":
            new_row += ["O"] * no_of_rocks + ["."] * no_of_empty
        else:
            new_row += ["."] * no_of_empty + ["O"] * no_of_rocks
        tilted.append("".join(new_row))
    return tilted


def tilt_left(platform):
    """returns a new platform tilted left (west)"""
    return tilt(platform, "L")


def tilt_right(platform):
    """returns a new platform tilted right (east)"""
    return tilt(platform, "R")


def tilt_up(platform):
    """returns a new platform tilted up (north)"""
    return transpose(tilt(transpose(platform), "L"))


def tilt_down(platform):
    """returns a new platform tilted down (south)"""
    return transpose(tilt(transpose(platform), "R"))


def cycle(platform):
    """returns a new platform tilted in turn up, left, down and right"""
    platform = tilt_up(platform)
    platform = tilt_left(platform)
    platform = tilt_down(platform)
    platform = tilt_right(platform)
    return platform


def compute_total_load(platform):
    """returns the total load of the given platform"""
    load = 0
    for i, row in enumerate(platform):
        load += (len(platform) - i) * row.count("O")
    return load


def solve_day14_part2():
    """Solve the problem"""

    platform = []
    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            platform.append(line.strip())

    # find a cycle using the "tortoise and hare" algorithm
    t = cycle(platform)
    h = cycle(t)
    while t != h:
        t = cycle(t)
        h = cycle(cycle(h))

    start = 0
    t = platform
    while t != h:
        t = cycle(t)
        h = cycle(h)
        start += 1

    cycle_length = 1
    h = cycle(h)
    while t != h:
        h = cycle(h)
        cycle_length += 1

    n = (1000000000 - start) % cycle_length
    count = 0
    while count < n:
        t = cycle(t)
        count += 1

    print(compute_total_load(t))


if __name__ == "__main__":
    solve_day14_part2()
