""" Advent of Code 2023 (https://adventofcode.com/)
    Day 13 Part 1. """


def transpose(pattern):
    """returns the transpose (rows to cols and vice versa) of pattern"""
    tp = []
    h = len(pattern)
    w = len(pattern[0])

    for j in range(w):
        col = []
        for i in range(h):
            col.append(pattern[i][j])
        tp.append("".join(col))

    return tp


def find_reflections(pattern):
    """finds all the horizontal reflections (number of lines above the symmetry axis)"""

    reflections = []
    n = len(pattern)
    for i in range(n - 1):
        b = True
        for j in range(min(i + 1, n - i - 1)):
            if pattern[i - j] != pattern[i + j + 1]:
                b = False
                break
        if b:
            reflections.append(i + 1)
    return reflections


def summarize(pattern):
    """computes the "summary" of the pattern"""
    summary = sum((100 * r for r in find_reflections(pattern)))
    summary += sum(r for r in find_reflections(transpose(pattern)))
    return summary


def solve_day13_part1():
    """Solve the problem"""

    summary = 0

    with open("input.txt", "r", encoding="utf-8") as f:
        pattern = []

        for line in f:
            if line.isspace():
                summary += summarize(pattern)
                pattern = []
            else:
                pattern.append(line.strip())

        if pattern:
            summary += summarize(pattern)

    print(summary)


if __name__ == "__main__":
    solve_day13_part1()
