""" Advent of Code 2023 (https://adventofcode.com/)
    Day 5 Part 2. """


def map_element(s, mapping):
    """Return the image of an element under a given mapping"""
    for m in mapping:
        if m[1] <= s and s < m[1] + m[2]:
            return m[0] + s - m[1]
    return s


def inverse_map_element(s, mapping):
    """Return the inverse image of an element under a given mapping"""
    for m in mapping:
        if m[0] <= s and m[0] + m[2] > s:
            return m[1] + s - m[0]
    return s


def solve_day5_part2():
    """Solve the problem"""

    mappings = []

    with open("input.txt", "r", encoding="utf-8") as f:
        line = f.readline()
        _, seed_ranges = line.split(":")
        seed_ranges = [int(s) for s in seed_ranges.strip().split()]
        seed_ranges = list(zip(seed_ranges[::2], seed_ranges[1::2]))
        for line in f:
            if "map" in line:
                mappings.append([])
                continue
            if not line.isspace():
                t = [int(s) for s in line.strip().split()]
                mappings[-1].append(t)

    candidates = []

    for mapping in mappings[::-1]:
        candidates = [inverse_map_element(c, mapping) for c in candidates]
        candidates += [0] + [t[1] for t in mapping] + [t[1] + t[2] for t in mapping]

    candidates_filtered = [s[0] for s in seed_ranges]
    for c in candidates:
        for sr in seed_ranges:
            if c >= sr[0] and c < sr[0] + sr[1]:
                candidates_filtered.append(c)
                break

    locations = []

    for c in candidates_filtered:
        for mapping in mappings:
            c = map_element(c, mapping)
        locations.append(c)

    print(min(locations))


if __name__ == "__main__":
    solve_day5_part2()
