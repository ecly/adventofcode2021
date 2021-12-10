import fileinput

TAGS = {"[": "]", "(": ")", "<": ">", "{": "}"}


def find_illegal(line):
    stack = []
    for c in line:
        if c in TAGS:
            stack.append(c)
        else:
            expected = TAGS[stack.pop()]
            if c != expected:
                return c

    return None


def find_completion(line):
    stack = []
    for c in line:
        if c in TAGS:
            stack.append(c)
        else:
            expected = TAGS[stack.pop()]
            if c != expected:
                return c

    return "".join(TAGS[c] for c in stack[::-1])


def score_completion(completion):
    score = 0
    points = {")": 1, "]": 2, "}": 3, ">": 4}
    for c in completion:
        score *= 5
        score += points[c]

    return score


def part1(lines):
    illegal = [c for l in lines if (c := find_illegal(l))]
    points = {")": 3, "]": 57, "}": 1197, ">": 25137}
    return sum(points[c] for c in illegal)


def part2(lines):
    incomplete = [l for l in lines if not find_illegal(l)]
    completions = [find_completion(l) for l in incomplete]
    scores = [score_completion(c) for c in completions]
    return sorted(scores)[len(scores) // 2]


def main():
    with fileinput.input("input") as f:
        lines = [l.strip() for l in f]

    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    main()
