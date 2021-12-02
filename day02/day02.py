from collections import defaultdict
import fileinput


def part1(steps):
    d = defaultdict(int)
    for direction, amount in steps:
        d[direction] += amount

    return d["forward"] * (d["down"] - d["up"])


def part2(steps):
    aim, horizontal, depth = 0, 0, 0
    for direction, amount in steps:
        if direction == "forward":
            horizontal += amount
            depth += amount * aim
        if direction == "down":
            aim += amount
        if direction == "up":
            aim -= amount

    return horizontal * depth


def main():
    steps = []
    for line in fileinput.input():
        direction, amount = line.split()
        steps.append((direction, int(amount)))

    print(part1(steps))
    print(part2(steps))


if __name__ == "__main__":
    main()
