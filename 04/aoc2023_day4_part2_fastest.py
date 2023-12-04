""" Advent of Code 2023 (https://adventofcode.com/)
    Day 4 Part 2 (fastest solution). """


def solve_day4_part2():
    """Solve the problem"""

    hits = []

    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            _, numbers = line.strip().split(":")
            winning, candidates = numbers.split("|")
            winning = winning.strip().split()
            candidates = candidates.strip().split()
            hit = 0
            for c in candidates:
                if c in winning:
                    hit += 1
            hits.append(hit)

    counts = [0] * len(hits)
    for i in reversed(range(len(counts))):
        counts[i] = 1 + sum(counts[i + 1 : min(len(counts), i + hits[i] + 1)])

    print(sum(counts))


if __name__ == "__main__":
    solve_day4_part2()
