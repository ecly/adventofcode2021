from collections import Counter, defaultdict


def count_fish(timers, days):
    buckets = defaultdict(int, Counter(timers))
    for _ in range(days):
        buckets = defaultdict(int, {k - 1: v for k, v in buckets.items()})
        buckets[8] += buckets[-1]
        buckets[6] += buckets[-1]
        del buckets[-1]

    return sum(buckets.values())


def part1(timers):
    return count_fish(timers, 80)


def part2(timers):
    return count_fish(timers, 256)


def main():
    timers = list(map(int, input().split(",")))
    print(part1(timers))
    print(part2(timers))


if __name__ == "__main__":
    main()
