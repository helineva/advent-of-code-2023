""" Advent of Code 2023 (https://adventofcode.com/)
    Day 17 Part 2. """
from queue import PriorityQueue


def neighbors(j, i, vj, vi, h, w):
    """generate all neighbors of the given node"""
    coords = []
    if j > 0:
        coords.append((j - 1, i))
    if j < h - 1:
        coords.append((j + 1, i))
    if i > 0:
        coords.append((j, i - 1))
    if i < w - 1:
        coords.append((j, i + 1))

    for new_j, new_i in coords:
        diff_j = new_j - j
        diff_i = new_i - i
        if diff_j * vj < 0 or diff_i * vi < 0:  # no turning back
            continue
        new_vj = vj + diff_j
        new_vi = vi + diff_i

        # moving too far in the same direction
        if abs(new_vj) > 10 or abs(new_vi) > 10:
            continue

        if new_vj != 0 and new_vi != 0:  # a turn
            # allowed only if moved far enough in the same direction
            if max(abs(vj), abs(vi)) > 3:
                yield (new_j, new_i, diff_j, diff_i)
        else:
            yield (new_j, new_i, new_vj, new_vi)


def solve_day17_part2():
    """Solve the problem"""

    heat_loss = []

    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            heat_loss.append([int(c) for c in line.strip()])

    w = len(heat_loss[0])
    h = len(heat_loss)

    # Dijkstra-style shortest path algorithm in a graph having nodes of the form (j,i,vj,vi)
    # where 0 <= j < h, 0 <= i < w, 0 < vj,vi <= 10, vj*vi == 0 (plus (0,0,0,0))
    # i.e. the heat_loss grid nodes augmented by direction vectors that describe
    # the movement entering the node (from which direction and how far in that direction)

    queue = PriorityQueue()
    queue.put((0, 0, 0, 0, 0))
    dist = {}

    while not queue.empty():
        d, j, i, vj, vi = queue.get()
        if (j, i, vj, vi) in dist:
            continue

        dist[(j, i, vj, vi)] = d

        for n in neighbors(j, i, vj, vi, h, w):
            new_d = d + heat_loss[n[0]][n[1]]
            queue.put((new_d, *n))

    dists_to_dest = []
    for j in range(4, 11):
        dists_to_dest.append(dist[(h - 1, w - 1, j, 0)])
    for i in range(4, 11):
        dists_to_dest.append(dist[(h - 1, w - 1, 0, i)])

    print(min(dists_to_dest))


if __name__ == "__main__":
    solve_day17_part2()
