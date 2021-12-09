import fileinput
from functools import reduce
from operator import mul


def get_adjacent(grid, x, y):
    options = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    max_x = len(grid)
    max_y = len(grid[0])
    adjacent = []
    for dx, dy in options:
        nx = x + dx
        ny = y + dy
        if 0 <= nx < max_x and 0 <= ny < max_y:
            adjacent.append((nx, ny))

    return adjacent


def get_lows(grid):
    lows = []
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            v = grid[x][y]
            adj = get_adjacent(grid, x, y)
            if all(grid[nx][ny] > v for nx, ny in adj):
                lows.append((x, y))

    return lows


def get_basin_size(grid, lx, ly):
    seen = set()
    queue = [(lx, ly)]
    while queue:
        head = queue.pop(0)
        if head in seen:
            continue

        seen.add(head)
        for a in get_adjacent(grid, *head):
            av = grid[a[0]][a[1]]
            if a in seen or av == 9:
                continue

            queue.append(a)

    return len(seen)


def part1(grid):
    lows = get_lows(grid)
    return sum(grid[x][y] for x, y in lows) + len(lows)


def part2(grid):
    lows = get_lows(grid)
    basin_sizes = [get_basin_size(grid, x, y) for x, y in lows]
    return reduce(mul, sorted(basin_sizes)[-3:], 1)


def main():
    grid = []
    for line in fileinput.input("input"):
        grid.append(list(map(int, line.strip())))

    print(part1(grid))
    print(part2(grid))


if __name__ == "__main__":
    main()
