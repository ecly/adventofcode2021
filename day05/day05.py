import fileinput
from collections import defaultdict


def get_step(start, end):
    if start == end:
        return 0

    return -1 if start > end else 1


def compute_point_overlap(lines, include_diagonals=False):
    grid = defaultdict(int)
    for (x1, y1), (x2, y2) in lines:
        if (x1 != x2 and y1 != y2) and not include_diagonals:
            continue

        x, y = x1, y1
        dx = get_step(x1, x2)
        dy = get_step(y1, y2)
        for _ in range(max(abs(x1 - x2), abs(y1 - y2)) + 1):
            grid[(x, y)] += 1
            x += dx
            y += dy

    return sum(v >= 2 for v in grid.values())


def part1(lines):
    return compute_point_overlap(lines)


def part2(lines):
    return compute_point_overlap(lines, True)


def main():
    lines = []
    for line in fileinput.input():
        c1, c2 = line.split(" -> ")
        x1, y1 = map(int, c1.split(","))
        x2, y2 = map(int, c2.split(","))

        lines.append(((x1, y1), (x2, y2)))

    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    main()
