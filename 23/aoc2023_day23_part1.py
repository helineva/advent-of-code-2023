""" Advent of Code 2023 (https://adventofcode.com/)
    Day 23 Part 1. """


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
            if (next_y, next_x) != (prev_y, prev_x) and (
                c in ".*"
                or (c == ">" and next_x - curr_x == 1)
                or (c == "v" and next_y - curr_y == 1)
            ):
                next_tiles.append((next_y, next_x))
        assert len(next_tiles) == 1
        prev_y, prev_x, curr_y, curr_x = curr_y, curr_x, *next_tiles[0]
        dist += 1

    return (curr_y, curr_x, dist)


def solve_day23_part1():
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
            if trails[n_y][n_x] == ">" and n_x - x == 1:
                arcs[i].append(follow_trail(node, "R", trails, h, w))
            if trails[n_y][n_x] == "v" and n_y - y == 1:
                arcs[i].append(follow_trail(node, "D", trails, h, w))

    # replace the node coordinates with the node's index in the list "nodes"
    arcs = [[(nodes.index((y, x)), d) for y, x, d in a] for a in arcs]

    # check that the graph is a DAG and sort the nodes topologically
    visited = [False for _ in nodes]
    marker_to_detect_cycle = [False for _ in nodes]
    nodes_sorted_topologically = []

    def visit(i):
        if visited[i]:
            return
        assert not marker_to_detect_cycle[
            i
        ], "The graph is not a DAG. This method fails."
        marker_to_detect_cycle[i] = True
        for j, _ in arcs[i]:
            visit(j)
        marker_to_detect_cycle[i] = False
        visited[i] = True
        nodes_sorted_topologically.append(i)

    for i, b in enumerate(visited):
        if not b:
            visit(i)

    # in a DAG, longest paths can be found by processing the nodes
    # in a topological order
    distances = [0 for _ in nodes]
    for i in reversed(nodes_sorted_topologically):
        for j, dist in arcs[i]:
            new_dist = distances[i] + dist
            if new_dist > distances[j]:
                distances[j] = new_dist

    print(distances[1])  # end node has index 1


if __name__ == "__main__":
    solve_day23_part1()
