""" Advent of Code 2023 (https://adventofcode.com/)
    Day 3 Part 2. """
import re


def solve_day3_part2():
    """Solve the problem"""

    sum_gear_ratios = 0

    with open("input.txt", "r", encoding="utf-8") as f:
        schematic = [line.strip() for line in f]

    prog_parts = re.compile(r"\d+")
    prog_gears = re.compile(r"\*")
    for i, line in enumerate(schematic):
        for match_gear in prog_gears.finditer(line):
            gear_pos = match_gear.start()
            count_adjacent = 0
            gear_ratio = 1
            if i > 0:
                for match_part in prog_parts.finditer(schematic[i - 1]):
                    if (
                        gear_pos >= match_part.start() - 1
                        and gear_pos <= match_part.end()
                    ):
                        count_adjacent += 1
                        gear_ratio *= int(match_part.group())
            if i < len(schematic) - 1:
                for match_part in prog_parts.finditer(schematic[i + 1]):
                    if (
                        gear_pos >= match_part.start() - 1
                        and gear_pos <= match_part.end()
                    ):
                        count_adjacent += 1
                        gear_ratio *= int(match_part.group())
            for match_part in prog_parts.finditer(line):
                if gear_pos >= match_part.start() - 1 and gear_pos <= match_part.end():
                    count_adjacent += 1
                    gear_ratio *= int(match_part.group())
            if count_adjacent == 2:
                sum_gear_ratios += gear_ratio

    print(sum_gear_ratios)


if __name__ == "__main__":
    solve_day3_part2()
