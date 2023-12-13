""" Advent of Code 2023 (https://adventofcode.com/)
    Day 13 Part 2. """


def number_of_differing_characters(s, t):
    """compares the first character of s to the first character of t,
             the second character of s to the second character of s,
             and so on,
    and return the number of differing characters"""
    return sum((1 for c, d in zip(s, t) if c != d))


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
    """finds all the horizontal reflections with exactly one smudge"""

    reflections = []
    n = len(pattern)
    for i in range(n - 1):
        diff = 0
        for j in range(min(i + 1, n - i - 1)):
            diff += number_of_differing_characters(pattern[i - j], pattern[i + j + 1])
            if diff > 1:
                break
        if diff == 1:
            reflections.append(i + 1)
    return reflections


def summarize(pattern):
    """computes the "summary" of the pattern"""
    summary = sum((100 * r for r in find_reflections(pattern)))
    summary += sum(r for r in find_reflections(transpose(pattern)))
    return summary


def solve_day13_part2():
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
    solve_day13_part2()
