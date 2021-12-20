def get_bounds(grid):
    x = [x for x, _ in grid]
    y = [y for _, y in grid]
    return min(x), max(x), min(y), max(y)


def get_window(grid, x, y, oob_default):
    window = []
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            window.append(grid.get((x + dx, y + dy), oob_default))

    return "".join(window)


def get_index_from_window(window):
    return int("".join("1" if c == "#" else "0" for c in window), 2)


def enhance_image(grid, algorithm, steps):  # pylint: disable=too-many-locals
    for step in range(steps):
        default = "."
        if algorithm[0] == "#":
            default = algorithm[-1] if step % 2 == 0 else algorithm[0]

        n = {}
        min_x, max_x, min_y, max_y = get_bounds(grid)
        for x in range(min_x - 1, max_x + 2):
            for y in range(min_y - 1, max_y + 2):
                window = get_window(grid, x, y, default)
                index = get_index_from_window(window)
                nc = algorithm[index]
                n[(x, y)] = nc

        grid = n

    return grid


def solve(grid, algorithm, steps):
    enhanced_image = enhance_image(grid, algorithm, steps)
    return sum(c == "#" for c in enhanced_image.values())


def part1(grid, algorithm):
    return solve(grid, algorithm, 2)


def part2(grid, algorithm):
    return solve(grid, algorithm, 50)


def main():
    with open("input", encoding="utf-8") as f:
        algorithm, image = f.read().split("\n\n")
        algorithm = algorithm.replace("\n", "")

    grid = {}
    for y, l in enumerate(image.split("\n")):
        for x, c in enumerate(l.strip()):
            grid[(x, y)] = c

    print(part1(grid, algorithm))
    print(part2(grid, algorithm))


if __name__ == "__main__":
    main()
