""" Advent of Code 2023 (https://adventofcode.com/)
    Day 18 Part 2. """


def decode(code):
    """extract direction and distance from color code"""
    hex_to_dec = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "a": 10,
        "b": 11,
        "c": 12,
        "d": 13,
        "e": 14,
        "f": 15,
    }
    hex_to_direction = {"0": "R", "1": "D", "2": "L", "3": "U"}
    distance = sum((hex_to_dec[c] * 16**e for e, c in enumerate(code[-2:0:-1])))
    direction = hex_to_direction[code[-1]]
    return (direction, distance)


def solve_day18_part2():
    """Solve the problem"""

    plan = []

    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            _, _, code = line.strip().split()
            plan.append(decode(code[1:-1]))

    # calculate the area bounded by the closed curve using the Trapezoid formula
    # https://en.wikipedia.org/wiki/Shoelace_formula#Trapezoid_formula
    # A = (1/2) * sum_{i=0}^{n-1} (y_i + y_{i+1})*(x_i - x_{i+1})
    area = 0
    y = 0
    for direction, distance in plan:
        if direction == "D":
            y += distance
        elif direction == "U":
            y -= distance
        elif direction == "R":
            area -= distance * 2 * y
        elif direction == "L":
            area += distance * 2 * y

    # make sure that the orientation is clockwise
    if area < 0:
        plan.reverse()
        reverse_directions = {"L": "R", "R": "L", "U": "D", "D": "U"}
        plan = [(reverse_directions[d], l) for d, l in plan]
        area = -area

    # trench area created when travelling D or L is not included in
    # the previous area computation, we still need to add this
    # (this is also possibly close to sum(distance) // 2 ?)
    #
    # added: the number is likely to be exactly 1 + sum(distance) / 2
    # sum(distance) / 2 comes from the fact that the distance travelled
    # up is equal to the distance travelled down, and similarly
    # the distance travelled right is equal to the distance travelled left,
    # since the curve is closed
    # + 1 comes from the fact that there are exactly one more
    # D-to-L transitions (adding one extra unit of area) than
    # L-to-D transitions (subtracting one unit)
    additional_area = 0
    prev_direction = plan[-1][0]
    for direction, distance in plan:
        if direction == "L":
            additional_area += distance
            if prev_direction == "D":
                additional_area += 1
        if direction == "D":
            additional_area += distance
            if prev_direction == "L":
                additional_area -= 1
        prev_direction = direction

    print(area // 2 + additional_area)


if __name__ == "__main__":
    solve_day18_part2()
