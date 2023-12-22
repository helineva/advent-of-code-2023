""" Advent of Code 2023 (https://adventofcode.com/)
    Day 22 Part 2. """
from bisect import insort
from math import inf
from queue import PriorityQueue


def solve_day22_part2():
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
        # compute the new z-coords of the currect brick and update it to "bricks"
        new_z0 = height_of_collision + 1
        new_z1 = new_z0 + z1 - z0
        bricks[i][2] = new_z0
        bricks[i][5] = new_z1
        # add the currect brick to "end_faces" keeping the list sorted by height
        insort(
            end_faces,
            [new_z1, x0, x1, y0, y1, i],
            key=lambda x: x[0],
        )

    # for each brick, find which bricks it's supporting
    supporting = [[] for _ in range(len(bricks))]
    for i in range(len(bricks)):
        for j in supported_by[i]:
            if j >= 0:
                supporting[j].append(i)

    number_of_falling_bricks = 0

    # for each brick, find which bricks would fall if that brick was taken away
    # move upwards according to the info given by "supported_by"
    # have to process the bricks in the order of increasing end face height
    # so something like a priority queue is needed
    # for example, using a normal queue
    # results in an easy-to-overlook error recording too few fallen bricks
    #
    # e.g. in the following, B1 is taken away
    # adding the bricks supported by B1 (that is B2 and B3) to the queue
    # and then processing B5 before B4, we fail to understand that B5 will fall
    #
    # |   B5   |
    # ----------
    # |   ||B4 |
    # |B2 |-----
    # |   |-----
    # |   ||B3 |
    # ----------
    # ----------
    # |   B1   |
    #

    for i, brick in enumerate(bricks):
        falling = set()
        queue = PriorityQueue()
        queue.put((brick[5], i))
        seen = set()

        while not queue.empty():
            z1, b = queue.get()
            if b == i or all((j in falling for j in supported_by[b])):
                falling.add(b)
                for j in supporting[b]:
                    if j not in seen:
                        seen.add(j)
                        queue.put((bricks[j][5], j))

        # don't count the current brick as fallen
        number_of_falling_bricks += len(falling) - 1

    print(number_of_falling_bricks)


if __name__ == "__main__":
    solve_day22_part2()
