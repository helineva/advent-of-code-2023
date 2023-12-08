""" Advent of Code 2023 (https://adventofcode.com/)
    Day 8 Part 1. """


def solve_day8_part1():
    """Solve the problem"""

    left = {}
    right = {}

    with open("input.txt", "r", encoding="utf-8") as f:
        instructions = f.readline().strip()
        for line in f:
            if line.isspace():
                continue
            node, leftright = line.strip().split('=')
            node = node.strip()
            l, r = leftright.strip(" ()").split(',')
            l = l.strip()
            r = r.strip()
            left[node] = l
            right[node] = r

    current = "AAA"
    count = 0
    length = len(instructions)

    while current != "ZZZ":
        instruction = instructions[count % length]
        if instruction == "L":
            current = left[current]
        else:
            current = right[current]
        count += 1

    print(count)


if __name__ == "__main__":
    solve_day8_part1()
