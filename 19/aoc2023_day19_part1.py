""" Advent of Code 2023 (https://adventofcode.com/)
    Day 19 Part 1. """
import re


def solve_day19_part1():
    """Solve the problem"""

    prog_workflow = re.compile(r"(\w+)\{([^\}]*)\}")
    prog_condition = re.compile(r"(\w+)(<|>)(\d+)")
    prog_ratings = re.compile(r"\{([^\{\}]+)\}")

    workflows = {}
    parts = []

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
                    category, op, value = prog_condition.match(cond).groups()
                    parsed_rules.append(((category, op, int(value)), dest))
            workflows[name] = parsed_rules
            line = f.readline()

        line = f.readline()
        while line and not line.isspace():
            ratings = prog_ratings.match(line).groups()[0]
            part = {}
            for rating in ratings.split(","):
                category, value = rating.split("=")
                part[category] = int(value)
            parts.append(part)
            line = f.readline()

    sum_ratings = 0

    for part in parts:
        curr_workflow = "in"

        while curr_workflow not in ("A", "R"):
            for cond, dest in workflows[curr_workflow]:
                if not cond:
                    break
                category, op, value = cond
                if op == "<" and part[category] < value:
                    break
                if op == ">" and part[category] > value:
                    break
            curr_workflow = dest

        if curr_workflow == "A":
            sum_ratings += sum(part.values())

    print(sum_ratings)


if __name__ == "__main__":
    solve_day19_part1()
