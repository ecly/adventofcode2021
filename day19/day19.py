from collections import defaultdict
from itertools import permutations, product

AXIS = list(permutations(range(3)))
SIGNS = list(product([-1, 1], [-1, 1], [-1, 1]))
BEACONS_TRIED_FOR_SCANNER = defaultdict(set)


def all_rotations(coords):
    # note that this gives 48 rotations because I'm not smart enough to filter out the mirrored ones
    for a1, a2, a3 in AXIS:
        for s1, s2, s3 in SIGNS:
            rotations = []
            for c in coords:
                rotations.append((c[a1] * s1, c[a2] * s2, c[a3] * s3))

            yield rotations


def sub_triple(a, b):
    return a[0] - b[0], a[1] - b[1], a[2] - b[2]


def add_triple(a, b):
    return a[0] + b[0], a[1] + b[1], a[2] + b[2]


def try_locate_scanner(beacons, coords):
    for candidate in all_rotations(coords):
        for c in candidate:
            for b in beacons:
                shift = sub_triple(b, c)
                shifted = {add_triple(x, shift) for x in candidate}
                if len(shifted.intersection(beacons)) >= 12:
                    return shift, shifted

    return None, None


def part1(scanners):
    scanner_positions = {0: (0, 0, 0)}
    beacons = set(scanners[0])
    unlocated_scanners = dict(scanners)
    unlocated_scanners.pop(0)

    while unlocated_scanners:
        for scanner_idx, points in unlocated_scanners.items():
            shift, shifted = try_locate_scanner(beacons, points)

            if shift:
                del unlocated_scanners[scanner_idx]
                scanner_positions[scanner_idx] = shift
                scanners[scanner_idx] = shifted
                beacons.update(shifted)
                break

    return beacons, scanner_positions


def part2(scanner_positions):
    return max(
        sum(abs(a - b) for a, b in zip(c1, c2))
        for c1, c2 in permutations(scanner_positions.values(), 2)
    )


def main():
    with open("input", encoding="utf-8") as f:
        blocks = f.read().split("\n\n")
        scanners = {}
        for i, b in enumerate(blocks):
            beacons = set()
            for l in b.splitlines()[1:]:
                x, y, z = map(int, l.split(","))
                beacons.add((x, y, z))

            scanners[i] = beacons

    beacons, scanner_positions = part1(scanners)
    print(len(beacons))
    print(part2(scanner_positions))


if __name__ == "__main__":
    main()
