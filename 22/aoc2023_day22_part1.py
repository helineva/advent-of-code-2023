""" Advent of Code 2023 (https://adventofcode.com/)
    Day 22 Part 1. """
from bisect import insort
from math import inf


def solve_day22_part1():
    """Solve the problem"""

    bricks = []

    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            start, end = line.strip().split("~")
            start = [int(c) for c in start.split(",")]
            end = [int(c) for c in end.split(",")]
            bricks.append([*start, *end])  # x0, y0, z0, x1, y1, z1

    bricks.sort(key=lambda b: b[2])  # sort by z0

    # refer to a brick by its index in the list "bricks"

    # keep record of end faces of already dropped bricks and heights of those
    # initialize with floor (with index -1)
    end_faces = [[0, -inf, inf, -inf, inf, -1]]  # height, x0, x1, y0, y1, brick

    # for each brick, keep record of which bricks (or floor) it is supported by
    supported_by = []

    # drop bricks
    for i, brick in enumerate(bricks):
        x0, y0, z0, x1, y1, z1 = brick
        current_supported_by = []

        # record the height of first collision
        # cannot break out from the loop immediately but need to consider
        # all the dropped bricks of the same end face height
        height_of_collision = None
        for h, a0, a1, b0, b1, j in reversed(end_faces):
            if height_of_collision is not None and h < height_of_collision:
                break
            # check whether there is a collision
            if x0 <= a1 and x1 >= a0 and y0 <= b1 and y1 >= b0:
                current_supported_by.append(j)
                height_of_collision = h
        supported_by.append(current_supported_by)
        # add the currect brick to "end_faces" keeping the list sorted by height
        insort(
            end_faces,
            [height_of_collision + 1 + z1 - z0, x0, x1, y0, y1, i],
            key=lambda x: x[0],
        )

    # find the bricks that support alone another brick
    supporting_alone = [False for _ in range(len(bricks))]
    for i, t in enumerate(supported_by):
        if len(t) == 1 and t[0] >= 0:
            supporting_alone[t[0]] = True

    # the rest of the bricks can be disintegrated safely
    print(len(bricks) - sum((1 for b in supporting_alone if b)))


if __name__ == "__main__":
    solve_day22_part1()
