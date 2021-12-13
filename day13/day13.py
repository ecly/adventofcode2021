import copy


def fold(grid, axis, i):
    if axis == "x":
        for x in range(i, len(grid[0])):
            nx = i - (x - i)
            for y in range(len(grid)):
                if grid[y][nx] == "#":
                    continue

                grid[y][nx] = grid[y][x]

        for j in range(len(grid)):
            grid[j] = grid[j][:i]

    else:
        for y in range(i, len(grid)):
            ny = i - (y - i)
            for x in range(len(grid[0])):
                if grid[ny][x] == "#":
                    continue

                grid[ny][x] = grid[y][x]

        for j in range(i, len(grid)):
            grid.pop()


def part1(grid, folds):
    grid = copy.deepcopy(grid)
    axis, i = folds[0]
    fold(grid, axis, i)
    return sum(c == "#" for r in grid for c in r)


def part2(grid, folds):
    grid = copy.deepcopy(grid)
    for axis, i in folds:
        fold(grid, axis, i)

    return "\n".join("".join(l) for l in grid)


def main():
    with open("input") as f:
        dots, folds_ = f.read().strip().split("\n\n")

    dots = [tuple(map(int, d.split(","))) for d in dots.splitlines()]
    max_x = max(d[0] for d in dots) + 1
    max_y = max(d[1] for d in dots) + 1
    grid = [["."] * max_x for _ in range(max_y)]
    for x, y in dots:
        grid[y][x] = "#"

    folds = []
    for f in folds_.splitlines():
        axis, i = f.split()[-1].split("=")
        folds.append((axis, int(i)))

    print(part1(grid, folds))
    print(part2(grid, folds))


if __name__ == "__main__":
    main()
