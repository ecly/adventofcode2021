import copy
import fileinput
from itertools import product

options = [(x, y) for x, y in product((-1, 0, 1), repeat=2) if x != 0 or y != 0]


def get_adjacent(grid, x, y):
    max_x = len(grid)
    max_y = len(grid[0])
    adjacent = []
    for dx, dy in options:
        nx = x + dx
        ny = y + dy
        if 0 <= nx < max_x and 0 <= ny < max_y:
            adjacent.append((nx, ny))

    return adjacent


def is_step_done(grid, flashes):
    for x, row in enumerate(grid):
        for y, energy in enumerate(row):
            if energy > 9 and (x, y) not in flashes:
                return False

    return True


def finish_step(grid):
    for x, row in enumerate(grid):
        for y, e in enumerate(row):
            if e > 9:
                grid[x][y] = 0


def step(grid):
    flashes = set()
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            grid[x][y] += 1

    while True:
        for x, row in enumerate(grid):
            for y, energy in enumerate(row):
                if energy < 10 or (x, y) in flashes:
                    continue

                flashes.add((x, y))
                for ax, ay in get_adjacent(grid, x, y):
                    grid[ax][ay] += 1

        if is_step_done(grid, flashes):
            finish_step(grid)
            return flashes


def part1(grid):
    count = 0
    for _ in range(100):
        flashes = step(grid)
        count += len(flashes)

    return count


def part2(grid):
    step_count = 0
    while True:
        step(grid)
        step_count += 1
        if all(e == 0 for r in grid for e in r):
            break

    return step_count


def main():
    grid = []
    with fileinput.input("input") as f:
        for l in f:
            grid.append(list(map(int, l.strip())))

    print(part1(copy.deepcopy(grid)))
    print(part2(copy.deepcopy(grid)))


if __name__ == "__main__":
    main()
