""" Advent of Code 2023 (https://adventofcode.com/)
    Day 10 Part 2. """


def solve_day10_part2():
    """Solve the problem"""

    diagram = []

    with open("input.txt", "r", encoding="utf-8") as f:
        for count, line in enumerate(f):
            diagram.append(list(line.strip()))
            if "S" in line:
                start_position = (count, line.index("S"))

    h = len(diagram)
    w = len(diagram[0])
    y, x = start_position

    # replace S by the correct pipe tile
    neighbors = []
    if x < w - 1:
        if diagram[y][x + 1] in "-J7":
            neighbors.append("R")
    if y < h - 1:
        if diagram[y + 1][x] in "|LJ":
            neighbors.append("D")
    if x > 0:
        if diagram[y][x - 1] in "-LF":
            neighbors.append("L")
    if y > 0:
        if diagram[y - 1][x] in "|7F":
            neighbors.append("U")

    map_neighbors_to_tile = {
        "RD": "F",
        "RL": "-",
        "RU": "L",
        "DL": "7",
        "DU": "|",
        "LU": "J",
    }
    diagram[y][x] = map_neighbors_to_tile["".join(neighbors)]

    # find the main loop
    loop = []
    entered_from = None
    curr = (y, x)

    while entered_from is None or curr != start_position:
        loop.append(curr)
        y, x = curr
        pipe = diagram[y][x]
        if pipe == "|":
            curr_y, curr_x, entered_from = (
                (y - 1, x, "D") if entered_from == "D" else (y + 1, x, "U")
            )
        if pipe == "-":
            curr_y, curr_x, entered_from = (
                (y, x - 1, "R") if entered_from == "R" else (y, x + 1, "L")
            )
        if pipe == "L":
            curr_y, curr_x, entered_from = (
                (y, x + 1, "L") if entered_from == "U" else (y - 1, x, "D")
            )
        if pipe == "J":
            curr_y, curr_x, entered_from = (
                (y - 1, x, "D") if entered_from == "L" else (y, x - 1, "R")
            )
        if pipe == "7":
            curr_y, curr_x, entered_from = (
                (y + 1, x, "U") if entered_from == "L" else (y, x - 1, "R")
            )
        if pipe == "F":
            curr_y, curr_x, entered_from = (
                (y + 1, x, "U") if entered_from == "R" else (y, x + 1, "L")
            )
        curr = (curr_y, curr_x)

    # make a new diagram with nothing else but the main loop
    new_diagram = []
    for i in range(h):
        new_diagram.append(["."] * w)

    for pipe in loop:
        new_diagram[pipe[0]][pipe[1]] = diagram[pipe[0]][pipe[1]]

    # count the tiles inside the loop;
    # on the previous line, exactly the tiles extending pipe downwards (|, F and 7)
    # mark boundary between outside and inside of the loop on the next line
    count = 0
    for i in range(h - 1):
        inside = False
        for j in range(w):
            if new_diagram[i][j] in "F7|":
                inside = not inside
            if new_diagram[i + 1][j] == "." and inside:
                count += 1

    print(count)


if __name__ == "__main__":
    solve_day10_part2()
