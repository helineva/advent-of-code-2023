""" Advent of Code 2023 (https://adventofcode.com/)
    Day 25 Part 1. """


def augment_path(source, dest, edges):
    """depth-first search to find a path from source to dest if it exists,
    if exists updates the edge capacities as in Ford-Fulkerson algorithm and returns True
    if does not exist return False"""
    visited = set()
    parent = {source: None}
    capacity = {}
    stack = [source]
    found = False

    while stack:
        node = stack.pop()
        visited.add(node)
        if node == dest:
            found = True
            break
        for neighbor, c in edges[node].items():
            if neighbor not in visited and c > 0:
                stack.append(neighbor)
                parent[neighbor] = node
                capacity[neighbor] = c

    if found:
        path = []
        node = dest
        min_capacity = None

        while node is not None:
            path.append(node)
            if min_capacity is None or (node != source and capacity[node] < min_capacity):
                min_capacity = capacity[node]
            node = parent[node]

        path.reverse()

        for n, m in zip(path, path[1:]):
            edges[n][m] -= min_capacity
            edges[m][n] += min_capacity
        return True

    return False


def connected_component(source, edges):
    """returns the connected component of a node"""
    visited = set()
    stack = [source]

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for neighbor, c in edges[node].items():
            if c > 0:
                stack.append(neighbor)

    return visited


def outedges(nodes, edges):
    """returns the number of edges between a set of nodes and its complement"""
    return sum((1 for node in nodes for n in edges[node] if n not in nodes))

def reset_edges(edges):
    """resets all the edge capacities to 1"""
    for d in edges:
        for n in d:
            d[n] = 1

def solve_day25_part1():
    """Solve the problem"""

    data = []

    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            data.append(line.strip().replace(":", "").split())

    nodes_in_letters = set([node for d in data for node in d])
    node_count = 0
    nodes = {}
    edges = []

    for node in nodes_in_letters:
        nodes[node] = node_count
        node_count += 1

    edges = [{} for _ in range(node_count)]

    for d in data:
        source, dests = d[0], d[1:]
        for dest in dests:
            edges[nodes[source]][nodes[dest]] = 1
            edges[nodes[dest]][nodes[source]] = 1

    source = 0  # arbitrary choice for source node
    # for all destination nodes except source, compute the minimum number of edges needed
    # to be removed from the graph to disconnect the source and destination nodes,
    # this is equal to the number of outward edges from the connected component
    # of the source node in the residual network resulting when the Ford-Fulkerson
    # max-flow algorithm terminates
    for dest in range(1, node_count):
        while augment_path(source, dest, edges):
            pass

        comp = connected_component(source, edges)
        if outedges(comp, edges) == 3:
            print(len(comp) * (node_count - len(comp)))
            break

        reset_edges(edges)


if __name__ == "__main__":
    solve_day25_part1()
