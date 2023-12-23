""" Advent of Code 2023 (https://adventofcode.com/)
    Day 23 Part 2. """


def neighbors(j, i, h, w):
    """helper function that generates the coordinates of neighboring tiles"""
    if j > 0:
        yield (j - 1, i)
    if j < h - 1:
        yield (j + 1, i)
    if i > 0:
        yield (j, i - 1)
    if i < w - 1:
        yield (j, i + 1)


def follow_trail(node, direction, trails, h, w):
    """follows the trail from "node" using initial "direction" until reaches another node,
    returns the coordinates of that node and the travelled distance"""
    prev_y, prev_x = node
    curr_y, curr_x = node
    if direction == "L":
        curr_x -= 1
    elif direction == "R":
        curr_x += 1
    elif direction == "U":
        curr_y -= 1
    elif direction == "D":
        curr_y += 1
    dist = 1

    while trails[curr_y][curr_x] != "*":
        next_tiles = []
        for next_y, next_x in neighbors(curr_y, curr_x, h, w):
            c = trails[next_y][next_x]
            if (next_y, next_x) != (prev_y, prev_x) and c != "#":
                next_tiles.append((next_y, next_x))
        assert len(next_tiles) == 1
        prev_y, prev_x, curr_y, curr_x = curr_y, curr_x, *next_tiles[0]
        dist += 1

    return (curr_y, curr_x, dist)


def solve_day23_part2():
    """Solve the problem"""

    trails = []

    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            trails.append(list(line.strip()))

    h = len(trails)
    w = len(trails[0])

    # find all the intersections in the trails map (surrounded by slopes)
    # add them to the list "nodes" together with the start and end point
    # mark them with *'s in the trails map (to distinguish from normal trail)
    start = (0, trails[0].index("."))
    trails[0][start[1]] = "*"

    end = (h - 1, trails[h - 1].index("."))
    trails[h - 1][end[1]] = "*"

    nodes = [start, end]

    for j, row in enumerate(trails):
        for i, c in enumerate(row):
            if c == "." and "." not in [trails[y][x] for y, x in neighbors(j, i, h, w)]:
                trails[j][i] = "*"
                nodes.append((j, i))

    # find trails between nodes and measure their distances
    arcs = [[] for _ in nodes]
    for i, node in enumerate(nodes):
        if node == start:
            arcs[i].append(follow_trail(node, "D", trails, h, w))
            continue
        y, x = node
        for n_y, n_x in neighbors(y, x, h, w):
            if trails[n_y][n_x] == ">":
                if n_x - x == 1:
                    arcs[i].append(follow_trail(node, "R", trails, h, w))
                elif n_x - x == -1:
                    arcs[i].append(follow_trail(node, "L", trails, h, w))
            if trails[n_y][n_x] == "v":
                if n_y - y == 1:
                    arcs[i].append(follow_trail(node, "D", trails, h, w))
                elif n_y - y == -1:
                    arcs[i].append(follow_trail(node, "U", trails, h, w))

    # replace the node coordinates with the node's index in the list "nodes"
    arcs = [[(nodes.index((y, x)), d) for y, x, d in a] for a in arcs]

    # very slow and inelegant brute force solution
    # generate all simple paths from start to end node
    # keeping record of the maximum length of those

    max_dist = 0
    stack = [(0, set(), 0)]
    while stack:
        i, visited, d = stack.pop()
        new_visited = set(visited)
        new_visited.add(i)

        if i == 1 and d > max_dist:  # end node has index 1
            max_dist = d

        for j, dist in arcs[i]:
            if j not in visited:
                stack.append((j, new_visited, d + dist))

    print(max_dist)


if __name__ == "__main__":
    solve_day23_part2()
