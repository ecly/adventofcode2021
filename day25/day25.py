def part1(grid):
    max_y = len(grid)
    max_x = len(grid[0])
    steps = 0
    while True:
        ng = []
        for _ in range(max_y):
            ng.append(["."] * max_x)

        for y in range(max_y):
            for x in range(max_x):
                c = grid[y][x]
                if c != ">":
                    continue
                nx, ny = ((x + 1) % max_x, y)
                if grid[ny][nx] == ".":
                    ng[ny][nx] = c
                else:
                    ng[y][x] = c

        for y in range(max_y):
            for x in range(max_x):
                c = grid[y][x]
                if c != "v":
                    continue
                nx, ny = (x, (y + 1) % max_y)
                if grid[ny][nx] != "v" and ng[ny][nx] == ".":
                    ng[ny][nx] = c
                else:
                    ng[y][x] = c

        steps += 1
        if ng == grid:
            break

        grid = ng

    return steps


def main():
    grid = []
    with open("input") as f:
        for l in f:
            grid.append(list(l.strip()))


if __name__ == "__main__":
    main()
