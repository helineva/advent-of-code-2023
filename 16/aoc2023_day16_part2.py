""" Advent of Code 2023 (https://adventofcode.com/)
    Day 16 Part 2. """


def compute_energized_tiles(grid, beams):
    """compute the number of energized tiles"""
    n = len(grid)

    # record the direction of a beam energizing a tile
    energized = [[set() for _ in range(n)] for _ in range(n)]

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

    return sum(1 for row in energized for element in row if element)


def solve_day16_part2():
    """Solve the problem"""

    grid = []

    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            grid.append(line.strip())

    n = len(grid)
    beams = (
        [(x, 0, "D") for x in range(n)]
        + [(x, n - 1, "U") for x in range(n)]
        + [(0, y, "R") for y in range(n)]
        + [(n - 1, y, "L") for y in range(n)]
    )

    number_of_energized_tiles = [
        compute_energized_tiles(grid, [beam]) for beam in beams
    ]
    print(max(number_of_energized_tiles))


if __name__ == "__main__":
    solve_day16_part2()
