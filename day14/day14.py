from collections import Counter


def solve(polymer, rules, steps=10):
    pair_counts = Counter({p: polymer.count(p) for p, _ in rules})
    char_counts = Counter(polymer)
    for _ in range(steps):
        np = Counter()
        for rule, insert in rules:
            c = pair_counts[rule]
            char_counts[insert] += c
            np[rule[0] + insert] += c
            np[insert + rule[1]] += c

        pair_counts = np

    mc = char_counts.most_common()
    return mc[0][1] - mc[-1][1]


def part1(template, rules):
    return solve(template, rules, steps=10)


def part2(template, rules):
    return solve(template, rules, steps=40)


def main():
    with open("input") as f:
        template, rules = f.read().strip().split("\n\n")
        rules = [tuple(r.strip().split(" -> ")) for r in rules.splitlines()]

    print(part1(template, rules))
    print(part2(template, rules))


if __name__ == "__main__":
    main()
