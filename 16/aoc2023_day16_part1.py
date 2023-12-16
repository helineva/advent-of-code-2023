""" Advent of Code 2023 (https://adventofcode.com/)
    Day 16 Part 1. """


def solve_day16_part1():
    """Solve the problem"""

    grid = []

    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            grid.append(line.strip())

    n = len(grid)

    # record the direction of a beam energizing a tile
    energized = [[set() for _ in range(n)] for _ in range(n)]

    beams = [(0, 0, "R")]
    while beams:
        curr_x, curr_y, direction = beams.pop()
        while 0 <= curr_x < n and 0 <= curr_y < n:
            if direction in energized[curr_y][curr_x]:
                break
            else:
                energized[curr_y][curr_x].add(direction)
            if grid[curr_y][curr_x] == ".":
                if direction == "L":
                    curr_x -= 1
                elif direction == "R":
                    curr_x += 1
                elif direction == "U":
                    curr_y -= 1
                elif direction == "D":
                    curr_y += 1
            elif grid[curr_y][curr_x] == "\\":
                if direction == "L":
                    curr_y -= 1
                    direction = "U"
                elif direction == "R":
                    curr_y += 1
                    direction = "D"
                elif direction == "U":
                    curr_x -= 1
                    direction = "L"
                elif direction == "D":
                    curr_x += 1
                    direction = "R"
            elif grid[curr_y][curr_x] == "/":
                if direction == "L":
                    curr_y += 1
                    direction = "D"
                elif direction == "R":
                    curr_y -= 1
                    direction = "U"
                elif direction == "U":
                    curr_x += 1
                    direction = "R"
                elif direction == "D":
                    curr_x -= 1
                    direction = "L"
            elif grid[curr_y][curr_x] == "|":
                if direction in ("L", "R"):
                    beams.append((curr_x, curr_y + 1, "D"))
                    beams.append((curr_x, curr_y - 1, "U"))
                elif direction == "U":
                    curr_y -= 1
                elif direction == "D":
                    curr_y += 1
            elif grid[curr_y][curr_x] == "-":
                if direction == "L":
                    curr_x -= 1
                elif direction == "R":
                    curr_x += 1
                elif direction in ("U", "D"):
                    beams.append((curr_x - 1, curr_y, "L"))
                    beams.append((curr_x + 1, curr_y, "R"))

    print(sum(1 for row in energized for element in row if element))


if __name__ == "__main__":
    solve_day16_part1()
