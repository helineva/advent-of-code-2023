""" Advent of Code 2023 (https://adventofcode.com/)
    Day 24 Part 1. """
from itertools import combinations


def solve_day24_part1():
    """Solve the problem"""

    hailstones = []

    x_min = 200000000000000
    y_min = 200000000000000
    x_max = 400000000000000
    y_max = 400000000000000

    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            p, v = line.strip().split("@")
            p = p.strip().split(",")
            v = v.strip().split(",")
            hailstones.append([int(n) for n in p + v])

    # compute the intersection point of the traces of pairs of hailstones if it exists
    # we need to solve the pair of linear equations in unknowns t and u (time)
    #   px1 + vx1 * t = px2 + vx2 * u   (equation for x-coordinates)
    #   py1 + vy1 * t = py2 + vy2 * u   (equation for y-coordinates)
    # we assume that the traces are lines, in other words they don't degenerate to points:
    # (vx1 != 0 or vy1 != 0) and (vx2 != 0 or vy2 != 0)
    # the pair has a unique solution if and only if d = vx1 * vy2 - vy1 * vx2 != 0
    # the case d = 0: the traces are parallel lines
    #   then the traces are the same or disjoint
    #   if there is a solution (t, u) then
    #   0 = t*d = (px2 - px1) * vy2 + (py1 - py2) * vx2
    #   0 = u*d = (px2 - px1) * vy1 + (py1 - py2) * vx1
    #   so that if either of the two quantities on the RHS is not equal to zero
    #   then the traces are not the same, so disjoint
    #   on the other hand, if
    #   (px2 - px1) * vy2 + (py1 - py2) * vx2 = 0 = (px2 - px1) * vy1 + (py1 - py2) * vx1
    #   then depending on which of vx1, vx2, vy1, vy2 is nonzero, at least one of the following
    #   ((px2 - px1) / vx1, 0), ((py2 - py1) / vy1, 0),
    #   (0, (px1 - px2) / vx2), (0, (py1 - py2) / vy2)
    #   is a common point (t, u) so that the traces are the same
    # the case d != 0: the unique solution is
    #   t = [(px2 - px1) * vy2 + (py1 - py2) * vx2] / d
    #   u = [(px2 - px1) * vy1 + (py1 - py2) * vx1] / d
    #   and the intersection point (x, y) is then
    #   x = px1 + vx1 * t
    #   y = py1 + vy1 * t
    #   the solution (t, u) is valid iff
    #   t > 0, u > 0, x_min <= x <= x_max, y_min <= y <= y_max   (*)
    #   write
    #   t0 = (px2 - px1) * vy2 + (py1 - py2) * vx2
    #   u0 = (px2 - px1) * vy1 + (py1 - py2) * vx1
    #   when d > 0, the conditions (*) are equivalent to
    #   t0 > 0, u0 > 0,
    #   x_min * d <= px1 * d + vx1 * t0 <= x_max * d and
    #   y_min * d <= py1 * d + vy1 * t0 <= y_max * d
    #   and for d < 0, switch <'s to >'s and <='s to >='s

    crossings = 0

    for h1, h2 in combinations(hailstones, 2):
        px1, py1, _, vx1, vy1, _ = h1
        px2, py2, _, vx2, vy2, _ = h2
        d = vx1 * vy2 - vy1 * vx2
        assert vx1 != 0 or vy1 != 0
        assert vx2 != 0 or vy2 != 0
        t0 = (px2 - px1) * vy2 + (py1 - py2) * vx2
        u0 = (px2 - px1) * vy1 + (py1 - py2) * vx1

        if d == 0:
            assert t0 != 0 or u0 != 0
        elif (
            d > 0
            and t0 > 0
            and u0 > 0
            and x_min * d <= px1 * d + vx1 * t0 <= x_max * d
            and y_min * d <= py1 * d + vy1 * t0 <= y_max * d
        ):
            crossings += 1
        elif (
            d < 0
            and t0 < 0
            and u0 < 0
            and x_min * d >= px1 * d + vx1 * t0 >= x_max * d
            and y_min * d >= py1 * d + vy1 * t0 >= y_max * d
        ):
            crossings += 1

    print(crossings)


if __name__ == "__main__":
    solve_day24_part1()
