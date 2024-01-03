""" Advent of Code 2023 (https://adventofcode.com/)
    Day 21 Part 2. """
from math import inf
from queue import PriorityQueue


def shortest_distances(source, garden):
    """Dijkstra's algorithm to compute shortest distances between a source pixel
    and the rest of them"""
    h = len(garden)
    w = len(garden[0])
    dists = [[inf] * w for _ in range(h)]
    visited = set()
    queue = PriorityQueue()
    queue.put((0, source))

    while not queue.empty():
        d, node = queue.get()
        if node in visited:
            continue
        visited.add(node)

        row, column = node
        if row > 0:
            if garden[row - 1][column] == ".":
                if d + 1 < dists[row - 1][column]:
                    dists[row - 1][column] = d + 1
                    queue.put((d + 1, (row - 1, column)))
        if row < h - 1:
            if garden[row + 1][column] == ".":
                if d + 1 < dists[row + 1][column]:
                    dists[row + 1][column] = d + 1
                    queue.put((d + 1, (row + 1, column)))
        if column > 0:
            if garden[row][column - 1] == ".":
                if d + 1 < dists[row][column - 1]:
                    dists[row][column - 1] = d + 1
                    queue.put((d + 1, (row, column - 1)))
        if column < w - 1:
            if garden[row][column + 1] == ".":
                if d + 1 < dists[row][column + 1]:
                    dists[row][column + 1] = d + 1
                    queue.put((d + 1, (row, column + 1)))

    return dists


def part(row, column):
    """return the part where the coordinate pair belongs to"""
    if row + column < 65:
        return "UL"
    elif column > row + 65:
        return "UR"
    elif column + 65 < row:
        return "DL"
    elif row + column > 3 * 65:
        return "DR"
    else:
        return "M"


def maximum_distance_by_part(source, p, garden):
    """returns the maximum distance (< inf) between the source pixel
    and the pixels in a given part of the tile"""
    distances = shortest_distances(source, garden)
    return max(
        distances[row][column]
        for row in range(len(garden))
        for column in range(len(garden[0]))
        if part(row, column) == p and distances[row][column] < inf
    )


def solve_day21_part2():
    """Solve the problem"""

    garden = []
    steps = 26501365

    with open("input.txt", "r", encoding="utf-8") as f:
        for row, line in enumerate(f):
            line = line.strip()
            if "S" in line:
                start = (row, line.index("S"))  # (65, 65)
                line = line.replace("S", ".")
            garden.append(line)

    h = len(garden)  # 131
    w = len(garden[0])  # 131
    n = steps // h  # 202300

    # moving back and forth allows us to waste steps so that
    # the pixels that can be reached after moving
    # exactly the given odd number of steps are the same
    # as the pixels that can be reached after moving any
    # odd number of steps up to the given limit
    # i.e. 1, 3, 5, ..., 26501365

    # inspection of the input (131 x 131 tile) reveals that there are paths
    # with no obstacles (rocks), shaped like
    # -----
    # | | |
    # --+--
    # | | |
    # -----
    # these paths form a grid that can be used to move around using minimal number
    # of steps
    # specifically when moving 26501365 steps up from the starting position
    # we arrive at the coordinate (0,65) on the tile that is 202300 tiles upwards
    # from the starting tile
    # when moving right 26501365 steps, we arrive at (65,130) on the tile that is 202300
    # tiles right from the starting tile
    # moving maximally down, arrive at (130,65) on the tile that is 202300 tiles down
    # moving maximally left, arrive at (65,0) on the tile that is 202300 tiles left
    # as can be seen on the input, conveniently, these points will be joined
    # by four diagonal paths having also no obstacles, these paths form a boundary
    # of a region so that no point outside of this region can not be reached by 26501365 steps
    # the remaining question is that which points inside the region can be reached

    # on the starting tile, using an odd number of steps, we can reach only pixels
    # having an odd coordinate sum, (so y + x is odd for point (y, x)), these pixels
    # form a checkerboard pattern on the tile, call them odd pixels
    # on the neighboring (horizontally or vertically) tiles, however, we can reach only the
    # the complement, that is the pixels having an even coordinate sum, call them even pixels
    # also call the starting tile even, its neighbors odd and so on,
    # again the even tiles make a checkerboard pattern, as does the odd tiles

    # the hypothesis is that the Elf can all the garden plots inside the boundaries that are
    # - odd pixels on the even tiles
    # - even pixels of the odd tiles
    # - not surrounded by rocks, i.e. in the same connected component with the start point

    # divide the input tile into five parts like this:
    # -------------
    # |    / \    |
    # |UL /   \ UR|
    # |  /     \  |
    # | /       \ |
    # |/         \|
    # |     M     |
    # |\         /|
    # | \       / |
    # |  \     /  |
    # |DL \   / DR|
    # |    \ /    |
    # -------------

    # the following should be enough to make the hypothesis true
    # ("reachable" here means in the same connected component with the start point):
    # - every reachable point in M can be reached with at most 65 steps from (65, 65)
    # - every reachable point in UL can be reached with at most 64 steps from (0, 0)
    # - every reachable point in UR can be reached with at most 64 steps from (0, 130)
    # - every reachable point in DL can be reached with at most 64 steps from (130, 0)
    # - every reachable point in DR can be reached with at most 64 steps from (130, 130)

    assert maximum_distance_by_part(start, "M", garden) <= 65
    assert maximum_distance_by_part((0, 0), "UL", garden) <= 64
    assert maximum_distance_by_part((0, 130), "UR", garden) <= 64
    assert maximum_distance_by_part((130, 0), "DL", garden) <= 64

    # with my input, the above does not hold in the case "DR": there is one pixel (108, 89)
    # that can not be reached by 64 steps, it is reached by 65 steps, however the farthest
    # occurrences of this pixel are all on odd tiles, and it is an odd pixel, so that it
    # does not falsify the hypothesis
    distances = shortest_distances((130, 130), garden)
    assert all(
        (
            (row + column) % 2 == 1
            for row in range(h)
            for column in range(w)
            if 64 < distances[row][column] < inf and part(row, column) == "DR"
        )
    )

    # now we count the parts of tile that this diamond-shaped region includes
    # do it row-wise

    # rows above the middle-row (middle-row means the one where the starting position lies)
    # in each row, the first even tile is missing UL; from the odd tile to the left of this tile
    # we must include one DR; the last even tile is missing UR; and from the odd tile to the right
    # we must include one DL
    # in the following W_E means the number of reachable (according to the hypothesis) pixels in an
    # even tile (so odd pixels lying in the same connected component as the start position)
    # W_O means the number of reachable pixels in an odd tile
    # similarly by parts: for example DL_E means the number of reachable pixels in the DL area of
    # an even tile
    # 1st row: W_E + DL_O + DR_O - UL_E - UR_E
    # 2nd row: 2 * W_E + 1 * W_O + DL_O + DR_O - UL_E - UR_E
    # 3rd row: 3 * W_E + 2 * W_O + DL_O + DR_O - UL_E - UR_E
    # ...
    # nth row: n * W_E + (n-1) * W_O + DL_O + DR_O - UL_E - UR_E   (where n = 202300)
    # summing these, we get (1+2+...+n)*W_E + (1+2+...+(n-1))*W_O + n*(DL_O + DR_O - UL_E - UR_E)
    # = (1/2)*n*(n+1)*W_E + (1/2)*(n-1)*n*W_O + n*(DL_O + DR_O - UL_E - UR_E)

    # rows below the middle-row are similar but exchange the roles of UL and DL, and UR and DR:
    # the sum is (1/2)*n*(n+1)*W_E + (1/2)*(n-1)*n*W_O + n*(UL_O + UR_O - DL_E - DR_E)

    # the middle-row: n+1 even tiles and n odd tiles and the even tile at the rightmost end
    # is missing UR and DR, and the even tile at the leftmost end is missing UL and DL
    # (n+1)*W_E + n*W_O - UR_E - DR_E - UL_E - DL_E

    # summing these three components, we get
    # (n+1)*(n+1)*W_E + n*n*W_O + n*(DL_O + DR_O + UL_O + UR_O) - (n+1)*(DL_E + DR_E + UL_E + UR_E)

    even = {"UL": 0, "UR": 0, "DL": 0, "DR": 0, "M": 0}
    odd = {"UL": 0, "UR": 0, "DL": 0, "DR": 0, "M": 0}

    for row in range(h):
        for column in range(w):
            if distances[row][column] < inf:
                if (row + column) % 2 == 1:
                    even[part(row, column)] += 1
                else:
                    odd[part(row, column)] += 1

    even_sum = sum(even.values())
    odd_sum = sum(odd.values())

    print(
        (n + 1) * (n + 1) * even_sum
        + n * n * odd_sum
        + n * (odd["DL"] + odd["DR"] + odd["UL"] + odd["UR"])
        - (n + 1) * (even["DL"] + even["DR"] + even["UL"] + even["UR"])
    )


if __name__ == "__main__":
    solve_day21_part2()
