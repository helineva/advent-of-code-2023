""" Advent of Code 2023 (https://adventofcode.com/)
    Day 19 Part 2. """
import re
from math import prod


def solve_day19_part2():
    """Solve the problem"""

    prog_workflow = re.compile(r"(\w+)\{([^\}]*)\}")
    prog_condition = re.compile(r"(\w+)(<|>)(\d+)")

    workflows = {}
    cats = "xmas"  # to map the categories to integers

    with open("input.txt", "r", encoding="utf-8") as f:
        line = f.readline()

        while line and not line.isspace():
            name, rules = prog_workflow.match(line).groups()
            rules = rules.split(",")
            parsed_rules = []
            for rule in rules:
                rule = rule.split(":")
                if len(rule) < 2:
                    parsed_rules.append(((), rule[0]))
                else:
                    cond, dest = rule
                    cat, op, value = prog_condition.match(cond).groups()
                    parsed_rules.append(((cats.index(cat), op, int(value)), dest))
            workflows[name] = parsed_rules
            line = f.readline()

    sum_of_combs = 0

    c = len(cats)
    min_rating = 1
    max_rating = 4000

    # traverse the workflow tree with the root "in" and the leaves "A(ccepted)"
    # and "R(ejected)" keeping record of the min and max bounds for each category,
    # at an "Accepted" leaf add the combinations allowed by the currect bounds,
    # this is simply the product of the length of the intervals given by the bounds,
    # the conditions are pairwise exclusive at the leaves so that the result is correct

    stack = []
    stack.append(("in", [min_rating] * c, [max_rating] * c))

    while stack:
        curr_workflow, min_bnds, max_bnds = stack.pop()

        if curr_workflow == "A":
            sum_of_combs += prod(
                (max(0, u - l + 1) for l, u in zip(min_bnds, max_bnds))
            )

        elif curr_workflow == "R":
            continue

        else:
            for cond, dest in workflows[curr_workflow]:
                if cond:
                    cat, op, value = cond
                    if op == "<":
                        new_min_bnds, new_max_bnds = list(min_bnds), list(max_bnds)
                        new_max_bnds[cat] = value - 1
                        stack.append((dest, new_min_bnds, new_max_bnds))
                        min_bnds[cat] = value
                    elif op == ">":
                        new_min_bnds, new_max_bnds = list(min_bnds), list(max_bnds)
                        new_min_bnds[cat] = value + 1
                        stack.append((dest, new_min_bnds, new_max_bnds))
                        max_bnds[cat] = value
                else:
                    stack.append((dest, min_bnds, max_bnds))

    print(sum_of_combs)


if __name__ == "__main__":
    solve_day19_part2()
