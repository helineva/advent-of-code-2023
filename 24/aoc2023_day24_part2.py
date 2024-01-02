""" Advent of Code 2023 (https://adventofcode.com/)
    Day 24 Part 2. """
from math import isqrt
from math import inf
from fractions import Fraction


def determinant_3x3(c1, c2, c3):
    """computes the determinant of a 3x3 matrix, given its columns"""
    return (
        c1[0] * (c2[1] * c3[2] - c3[1] * c2[2])
        - c2[0] * (c1[1] * c3[2] - c3[1] * c1[2])
        + c3[0] * (c1[1] * c2[2] - c2[1] * c1[2])
    )


def coplanar(u1, v1, u2, v2):
    """tests if the lines { ui + t*vi : t in R }, i = 1,2, lie on the same plane"""
    u = tuple((x - y for x, y in zip(u2, u1)))
    return determinant_3x3(v1, v2, u) == 0


def cross_product(v, w):
    """computes the cross product of two vectors"""
    return (
        v[1] * w[2] - w[1] * v[2],
        w[0] * v[2] - v[0] * w[2],
        v[0] * w[1] - w[0] * v[1],
    )


def intersection(v1, u1, v2, u2):
    """computes the number of intersection points of two lines"""
    u = tuple((x - y for x, y in zip(u2, u1)))
    if not coplanar(u1, v1, u2, v2):
        return 0
    if cross_product(v1, v2) != (0, 0, 0):
        return 1
    if cross_product(v1, u) != (0, 0, 0):
        return 0
    else:
        return inf


def invert_3x3(c1, c2, c3):
    """inverts a 3x3 matrix, given its columns"""
    a, d, g, b, e, h, c, f, i = *c1, *c2, *c3
    i11 = e * i - f * h
    i21 = f * g - d * i
    i31 = d * h - e * g
    i12 = c * h - b * i
    i22 = a * i - c * g
    i32 = b * g - a * h
    i13 = b * f - c * e
    i23 = c * d - a * f
    i33 = a * e - b * d
    det = a * i11 + b * i21 + c * i31
    return (
        (i11 / det, i21 / det, i31 / det),
        (i12 / det, i22 / det, i32 / det),
        (i13 / det, i23 / det, i33 / det),
    )


def linear_map(c1, c2, c3, v):
    """applies a linear map (such that ei -> ci) to a vector v"""
    w1 = c1[0] * v[0] + c2[0] * v[1] + c3[0] * v[2]
    w2 = c1[1] * v[0] + c2[1] * v[1] + c3[1] * v[2]
    w3 = c1[2] * v[0] + c2[2] * v[1] + c3[2] * v[2]
    return (w1, w2, w3)


def solve_day24_part2():
    """Solve the problem"""

    hailstones = []

    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            p, v = line.strip().split("@")
            p = p.strip().split(",")
            v = v.strip().split(",")
            hailstones.append([Fraction(n) for n in p + v])

    # the plan is to take any four hailstones and attempt to find a line intersecting
    # each of the four trajectory lines of these hailstones
    # I use the method described in the article
    # "Constructing a straight line intersecting four lines" by Huang, Li and Sze

    # take the first four hailstones; position vectors ui and velocity vectors vi
    # so trajectory lines are defined by Li = { ui + t*vi : t in R }
    u1, v1 = tuple(hailstones[0][:3]), tuple(hailstones[0][3:])
    u2, v2 = tuple(hailstones[1][:3]), tuple(hailstones[1][3:])
    u3, v3 = tuple(hailstones[2][:3]), tuple(hailstones[2][3:])
    u4, v4 = tuple(hailstones[3][:3]), tuple(hailstones[3][3:])

    # check that the lines are pairwise skew (i.e. not lying on the same plane)
    assert not coplanar(u1, v1, u2, v2)
    assert not coplanar(u1, v1, u3, v3)
    assert not coplanar(u1, v1, u4, v4)
    assert not coplanar(u2, v2, u3, v3)
    assert not coplanar(u2, v2, u4, v4)
    assert not coplanar(u3, v3, u4, v4)

    # as in the article, apply a translation followed by a linear map so that
    # we can assume u1 = 0, v1 = e1, u2 = e3, v2 = e2
    # the translation is the map x -> m - u1
    # the linear map is the inverse map of the linear map defined by
    # e1 -> v1, e2 -> v2, e3 -> u2-u1
    m1, m2, m3 = invert_3x3(v1, v2, tuple(a - b for a, b in zip(u2, u1)))
    v3 = linear_map(m1, m2, m3, v3)
    v4 = linear_map(m1, m2, m3, v4)
    u3 = linear_map(m1, m2, m3, tuple(a - b for a, b in zip(u3, u1)))
    u4 = linear_map(m1, m2, m3, tuple(a - b for a, b in zip(u4, u1)))

    # compute the cross products of v3,u3 and v4,u4
    # (a3, b3, c3) = v3 x u3; (a4, b4, c4) = v4 x u4
    (a3, b3, c3) = cross_product(v3, u3)
    (a4, b4, c4) = cross_product(v4, u4)

    # then the lines intersecting all the four transformed lines are of the form
    # L0 = { (-t1,0,0) + t*(t1,t2,1) : t in R } where
    # t1 is a root of the polynomial
    # p(x) = (v33*x + b3)*((a4-v42)*x + c4) - (v43*x + b4)((a3-v32)*x + c3)
    # such that v33*t1 + b3 != 0 != v43*t1 + b4
    # and t2 = -((a3-v32)*t1 + c3) / (v33*t1 + b3)
    # to find the roots, compute the coefficients and discrimimant of p
    coeff2 = v3[2] * (a4 - v4[1]) - v4[2] * (a3 - v3[1])
    coeff1 = v3[2] * c4 + b3 * (a4 - v4[1]) - v4[2] * c3 - b4 * (a3 - v3[1])
    coeff0 = b3 * c4 - b4 * c3
    disc = coeff1 * coeff1 - 4 * coeff2 * coeff0

    # in this case, the polynomial is of the second degree and the discriminant is positive
    assert coeff2 != 0
    assert disc > 0

    # then there are two solutions, both involving the square root of the discriminant,
    # which happens to be rational in this case
    sqroot_of_disc = Fraction(isqrt(disc.numerator), isqrt(disc.denominator))
    assert sqroot_of_disc**2 == disc
    t1s = [
        (-sqroot_of_disc - coeff1) / (2 * coeff2),
        (sqroot_of_disc - coeff1) / (2 * coeff2),
    ]

    # check the additional condition: v33*t1 + b3 != 0 != v43*t1 + b4
    assert v3[2] * t1s[0] + b3 != 0 and v4[2] * t1s[0] + b4 != 0
    assert v3[2] * t1s[1] + b3 != 0 and v4[2] * t1s[1] + b4 != 0

    # both solutions for t1 are valid,
    # choose and continue with the first one
    t1 = t1s[0]
    assert t1.denominator == 1
    t2 = -((a3 - v3[1]) * t1 + c3) / (v3[2] * t1 + b3)

    # now we know that the line { u0 + t*v0 : t in R } where
    # u0 = (-t1,0,0) and v0 = (t1,t2,1)
    # intersects the four transformed lines
    u0 = (-t1, 0, 0)
    v0 = (t1, t2, 1)

    # map this line by the above linear map and the translation x -> x + u1
    u0 = linear_map(v1, v2, tuple(a - b for a, b in zip(u2, u1)), u0)
    v0 = linear_map(v1, v2, tuple(a - b for a, b in zip(u2, u1)), v0)
    u0 = tuple(a + b for a, b in zip(u0, u1))

    # check that the found line intersects all the trajectories at exactly one point
    for hailstone in hailstones:
        u, v = tuple(hailstone[:3]), tuple(hailstone[3:])
        assert intersection(v0, u0, v, u) == 1

    # to find the correct starting position and velocity vector,
    # pick two hailstones and find the times of collision t1 and t2
    # use the first two hailstones
    d = v1[0] * v0[1] - v1[1] * v0[0]
    assert d != 0
    t1 = ((u0[0] - u1[0]) * v0[1] + (u1[1] - u0[1]) * v0[0]) / d

    d = v2[0] * v0[1] - v2[1] * v0[0]
    assert d != 0
    t2 = ((u0[0] - u2[0]) * v0[1] + (u2[1] - u0[1]) * v0[0]) / d

    # the correct velocity vector is now the difference of the two points
    # of collision divided by the time elapsed between the collisions
    poc1 = (u1[0] + t1 * v1[0], u1[1] + t1 * v1[1], u1[2] + t1 * v1[2])
    poc2 = (u2[0] + t2 * v2[0], u2[1] + t2 * v2[1], u2[2] + t2 * v2[2])
    v0 = tuple(((a - b) / (t2 - t1) for a, b in zip(poc2, poc1)))

    # the starting position can now be obtained by moving backwards from, say,
    # the first point of collision
    u0 = tuple((a - t1 * b for a, b in zip(poc1, v0)))

    # check that with this choice the trajectories meet at the correct time
    for hailstone in hailstones:
        u, v = tuple(hailstone[:3]), tuple(hailstone[3:])
        i = min((j for j, t in enumerate(zip(v, v0)) if t[0] != t[1]))
        t = (u0[i] - u[i]) / (v[i] - v0[i])
        assert (
            u0[0] + t * v0[0] == u[0] + t * v[0]
            and u0[1] + t * v0[1] == u[1] + t * v[1]
            and u0[2] + t * v0[2] == u[2] + t * v[2]
        )

    # print out the sum of the coordinates of the starting position
    print(sum(u0))


if __name__ == "__main__":
    solve_day24_part2()
