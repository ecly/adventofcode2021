import heapq
from copy import deepcopy


def get_adjacent(grid, x, y):
    options = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    adjacent = []
    for dx, dy in options:
        nx = x + dx
        ny = y + dy
        if (nx, ny) in grid:
            adjacent.append((nx, ny))

    return adjacent


def shortest_path(grid):
    queue = [(0, (0, 0))]
    seen = {}
    while queue:
        cv, c = heapq.heappop(queue)
        if c in seen:
            continue

        seen[c] = cv
        for n in get_adjacent(grid, *c):
            if n in seen:
                continue
            nv = cv + grid[n]
            heapq.heappush(queue, (nv, n))

    max_x = max(k[0] for k in grid.keys())
    max_y = max(k[1] for k in grid.keys())
    return seen[(max_x, max_y)]


def part1(grid):
    return shortest_path(grid)


def part2(grid):
    grid = deepcopy(grid)
    max_x = max(k[0] for k in grid.keys()) + 1
    max_y = max(k[1] for k in grid.keys()) + 1
    for i in range(1, 5):
        for x in range(max_x):
            nx = i * max_x + x
            for y in range(max_y):
                base_v = grid[(x % max_x, y)]
                nv = base_v + i
                if nv > 9:
                    nv = nv % 10 + 1
                grid[(nx, y)] = nv

    for i in range(1, 5):
        for y in range(max_y):
            ny = i * max_y + y
            for x in range(max_x * 5):
                base_v = grid[(x, ny % max_y)]
                nv = base_v + i
                if nv > 9:
                    nv = nv % 10 + 1
                grid[(x, ny)] = nv

    return shortest_path(grid)


def main():
    grid = {}
    with open("input") as f:
        for y, row in enumerate(f):
            for x, risk in enumerate(row.strip()):
                grid[(x, y)] = int(risk)

    print(part1(grid))
    print(part2(grid))


if __name__ == "__main__":
    main()
