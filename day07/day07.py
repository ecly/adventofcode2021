import math


def part1(positions):
    bp = sorted(positions)[len(positions) // 2]
    return sum(abs(p - bp) for p in positions)


def part2(positions):
    mean = sum(positions) // len(positions)
    options = set([math.floor(mean), math.ceil(mean)])
    return min(sum(sum(range(1, abs(p - o) + 1)) for p in positions) for o in options)


def main():
    positions = list(map(int, input().split(",")))
    print(part1(positions))
    print(part2(positions))


if __name__ == "__main__":
    main()
