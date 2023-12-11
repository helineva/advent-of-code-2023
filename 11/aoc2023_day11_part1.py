""" Advent of Code 2023 (https://adventofcode.com/)
    Day 11 Part 1. """


def solve_day11_part1():
    """Solve the problem"""

    galaxies = []

    with open("input.txt", "r", encoding="utf-8") as f:
        for row, line in enumerate(f):
            for column, char in enumerate(line.strip()):
                if char == "#":
                    galaxies.append((row, column))

    rows = galaxies[-1][0] + 1
    columns = max((g[1] for g in galaxies)) + 1

    rows_without_galaxies = set(range(rows)).difference(set((g[0] for g in galaxies)))
    columns_without_galaxies = set(range(columns)).difference(
        set((g[1] for g in galaxies))
    )

    rows_without_galaxies = sorted(list(rows_without_galaxies))
    columns_without_galaxies = sorted(list(columns_without_galaxies))

    new_rows = []
    offset = 0
    current_index = 0
    for r in range(rows):
        if (
            current_index < len(rows_without_galaxies)
            and rows_without_galaxies[current_index] < r
        ):
            offset += 1
            current_index += 1
        new_rows.append(r + offset)

    new_columns = []
    offset = 0
    current_index = 0
    for c in range(columns):
        if (
            current_index < len(columns_without_galaxies)
            and columns_without_galaxies[current_index] < c
        ):
            offset += 1
            current_index += 1
        new_columns.append(c + offset)

    new_galaxies = [(new_rows[g[0]], new_columns[g[1]]) for g in galaxies]

    sum_of_distances = 0
    for i, g1 in enumerate(new_galaxies):
        for g2 in new_galaxies[i + 1 :]:
            sum_of_distances += abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])

    print(sum_of_distances)


if __name__ == "__main__":
    solve_day11_part1()
