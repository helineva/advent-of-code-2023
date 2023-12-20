""" Advent of Code 2023 (https://adventofcode.com/)
    Day 20 Part 1. """
from queue import Queue


def solve_day20_part1():
    """Solve the problem"""

    module_type = {}
    connections = {}
    state = {}

    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            source, dests = line.strip().split(" -> ")
            if source.startswith("%"):
                name = source[1:]
                module_type[name] = "flip-flop"
                state[name] = 0
            elif source.startswith("&"):
                name = source[1:]
                module_type[name] = "conjunction"
                state[name] = {}
            else:
                name = source
                module_type[name] = "broadcaster"
            dests = dests.split(", ")
            connections[name] = dests

    for module, dests in connections.items():
        for dest in dests:
            if dest in module_type and module_type[dest] == "conjunction":
                state[dest][module] = 0

    total_low = 0
    total_high = 0
    pulse_queue = Queue()

    for _ in range(1000):
        pulse_queue.put(("button", "broadcaster", 0))
        while not pulse_queue.empty():
            source, dest, pulse = pulse_queue.get()
            if pulse == 0:
                total_low += 1
            else:
                total_high += 1
            if dest not in module_type:
                continue
            if module_type[dest] == "flip-flop" and pulse == 0:
                state[dest] = not state[dest]
                for d in connections[dest]:
                    pulse_queue.put((dest, d, state[dest]))
            elif module_type[dest] == "conjunction":
                state[dest][source] = pulse
                output = not all(state[dest].values())
                for d in connections[dest]:
                    pulse_queue.put((dest, d, output))
            elif module_type[dest] == "broadcaster":
                for d in connections[dest]:
                    pulse_queue.put((dest, d, pulse))

    print(total_low * total_high)


if __name__ == "__main__":
    solve_day20_part1()
