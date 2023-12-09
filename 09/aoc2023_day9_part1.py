""" Advent of Code 2023 (https://adventofcode.com/)
    Day 9 Part 1. """


def solve_day9_part1():
    """Solve the problem"""

    data = []

    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            data.append([int(s) for s in line.strip().split()])

    sum_of_extrapolated_values = 0

    for seq in data:
        diff_seqs = [seq]
        curr = seq

        while any((e != 0 for e in curr)):
            diff_seq = []
            for i in range(1, len(curr)):
                diff_seq.append(curr[i] - curr[i - 1])
            curr = diff_seq
            diff_seqs.append(curr)

        diff_seqs[-1].append(0)

        for i in reversed(range(len(diff_seqs) - 1)):
            diff_seqs[i].append(diff_seqs[i][-1] + diff_seqs[i + 1][-1])

        sum_of_extrapolated_values += diff_seqs[0][-1]

    print(sum_of_extrapolated_values)


if __name__ == "__main__":
    solve_day9_part1()
