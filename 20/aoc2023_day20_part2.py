""" Advent of Code 2023 (https://adventofcode.com/)
    Day 20 Part 2. """
from queue import Queue
from math import lcm


def simulate(observed, module_type, connections, state):
    """simulate the machine until observing high signal at a given module
    return the number of button presses until this happens, also return
    the signal counts when a low or a high signal is observed in the last run"""
    pulse_queue = Queue()
    button_count = 0
    cont = True

    while cont:
        pulse_queue.put(("button", "broadcaster", 0))
        button_count += 1
        signal_count = 0
        signal_counts_when_observed_low = []
        signal_counts_when_observed_high = []

        while not pulse_queue.empty():
            source, dest, pulse = pulse_queue.get()
            signal_count += 1
            if dest == observed:
                if pulse == 0:
                    signal_counts_when_observed_low.append(signal_count)
                if pulse == 1:
                    signal_counts_when_observed_high.append(signal_count)
                    cont = False
            if dest not in module_type:
                continue
            if module_type[dest] == "flip-flop" and pulse == 0:
                state[dest] = 1 - state[dest]
                for d in connections[dest]:
                    pulse_queue.put((dest, d, state[dest]))
            elif module_type[dest] == "conjunction":
                state[dest][source] = pulse
                output = 1 - int(all(state[dest].values()))
                for d in connections[dest]:
                    pulse_queue.put((dest, d, output))
            elif module_type[dest] == "broadcaster":
                for d in connections[dest]:
                    pulse_queue.put((dest, d, pulse))

    return (
        button_count,
        signal_counts_when_observed_low,
        signal_counts_when_observed_high,
    )


def connected_component(module, connections):
    """finds where a signal can propagate from a given module"""
    visited = set()
    stack = [module]
    while stack:
        m = stack.pop()
        visited.add(m)
        for n in connections[m]:
            if n not in visited:
                stack.append(n)
    return visited


def inputs(module, connections):
    """returns the input modules of a given module"""
    inp = set()
    for s, d in connections.items():
        if module in d:
            inp.add(s)
    return inp


def solve_day20_part2():
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

    output_modules = [
        m for c in connections.values() for m in c if m not in module_type
    ]
    for m in output_modules:
        module_type[m] = "other"
        connections[m] = []

    for module, dests in connections.items():
        for dest in dests:
            if module_type[dest] == "conjunction":
                state[dest][module] = 0

    # try to analyse the machine

    broadcaster = next((m for m, n in module_type.items() if n == "broadcaster"))
    dest_bc = connections[broadcaster]
    assert len(dest_bc) == 4

    cc = []
    for m in dest_bc:
        cc.append(connected_component(m, connections))

    intersection = cc[0].intersection(cc[1])
    for i in range(4):
        for j in range(i + 1, 4):
            assert cc[i].intersection(cc[j]) == intersection

    machines = [c.difference(intersection) for c in cc]

    assert len(intersection) == 2
    assert "rx" in intersection
    intersection.remove("rx")
    conjunction = intersection.pop()
    assert module_type[conjunction] == "conjunction"

    for machine in machines:
        for module in machine:
            for dest in connections[module]:
                if dest not in machine:
                    assert dest == conjunction

    assert connections[conjunction] == ["rx"]
    assert len(inputs(conjunction, connections)) == 4
    assert inputs("rx", connections) == {conjunction}

    # we can conclude that the situation is as in the following picture
    #
    #              |button|
    #                 |
    #            |broadcaster|
    #         /    /      \     \
    #      |M1|  |M2|     |M3|  |M4|
    #         \    |       |    /
    #            |conjunction|
    #                  |
    #                |rx|
    #
    # where the signals travel only from top to bottom
    # the low signal at rx appears exactly when the four inputs of
    # the module "conjunction" in the picture are all in the high state
    # each of these inputs come from a different machine Mi,
    # since there is no interaction between the machines M1, M2, M3, M4
    # we can examine their behaviour independently, more precisely
    # find when a high signal at "conjunction" from Mi happens,
    # at what button count and at what signal count

    button_counts = []
    signal_count_low = []
    signal_count_high = []

    for i in range(4):
        new_state = dict(state)
        new_connections = dict(connections)
        new_connections[broadcaster] = [dest_bc[i]]
        button, low, high = simulate(conjunction, module_type, new_connections, new_state)
        button_counts.append(button)
        signal_count_low.append(low)
        signal_count_high.append(high)

        # the state of the machine is back at the initial state
        # after high signal is observed at "conjunction"
        for s, v in new_state.items():
            assert v == state[s]

    # the state of the machine Mi resets to the initial state at the same
    # button press as high pulse is observed at "conjunction"
    # it means that the offset before the cycle starts repeating is zero
    # the first time high pulses from each machine Mi is observed simultaneously
    # at the same button press happens at the lowest common multiple of
    # the cycles

    # to be precise, in order for that to happen, no machine Mi should
    # not send a low signal to "conjunction" before all of them have
    # sent a high signal, check this

    # the high signal at "conjunction" is observed exactly once
    # and before any low signals
    for i in range(4):
        assert len(signal_count_high[i]) == 1
        assert signal_count_high[i][0] < signal_count_low[i][0]

    # we must check that lowest of the low signal counts is higher
    # than the highest of the high signal counts

    lowest = min(signal_count_low[i][0] for i in range(4))
    highest = max(signal_count_high[i][0] for i in range(4))
    assert highest < lowest


    print(lcm(*button_counts))


if __name__ == "__main__":
    solve_day20_part2()
