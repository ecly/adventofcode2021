import fileinput


def part1(entries):
    count = 0
    for _, outputs in entries:
        for output in outputs:
            if len(output) in (2, 3, 4, 7):
                count += 1

    return count


def get_output_value_for_entry(signals, outputs):
    l2d = {2: 1, 3: 7, 4: 4, 7: 8}
    m = {l2d[d]: s for s in signals if (d := len(s)) in l2d}

    # len 6 signals
    s6 = [s for s in signals if len(s) == 6]
    m[6] = [s for s in s6 if not m[7].issubset(s)][0]
    s6 = [s for s in s6 if s != m[6]]
    m[9] = [s for s in s6 if m[4].issubset(s)][0]
    m[0] = [s for s in s6 if s != m[9]][0]

    # len 5 signals
    s5 = [s for s in signals if len(s) == 5]
    m[3] = [s for s in s5 if m[7].issubset(s)][0]
    s5 = [s for s in s5 if s != m[3]]
    m[5] = [s for s in s5 if m[6].issuperset(s)][0]
    m[2] = [s for s in s5 if s != m[5]][0]

    s2v = {"".join(sorted(v)): k for k, v in m.items()}
    digits = [str(s2v["".join(sorted(o))]) for o in outputs]
    return int("".join(digits))


def part2(entries):
    return sum(get_output_value_for_entry(*e) for e in entries)


def main():
    entries = []
    for line in fileinput.input():
        signals, outputs = line.strip().split(" | ")
        signals = [set(s) for s in signals.split()]
        outputs = [set(o) for o in outputs.split()]
        entries.append((signals, outputs))

    print(part1(entries))
    print(part2(entries))


if __name__ == "__main__":
    main()
