import re
from collections import namedtuple
from typing import List, Optional

Cuboid = namedtuple("Coords", "lx hx ly hy lz hz")
Volume = namedtuple("Volume", "state cuboid")


def get_volume(c: Cuboid) -> int:
    lx, hx, ly, hy, lz, hz = c
    return abs(hx - lx + 1) * abs(hy - ly + 1) * abs(hz - lz + 1)


def get_intersection(a: Cuboid, b: Cuboid) -> Optional[Cuboid]:
    # pylint: disable=R0916
    if (
        a.hx < b.lx
        or b.hx < a.lx
        or a.hy < b.ly
        or b.hy < a.ly
        or a.hz < b.lz
        or b.hz < a.lz
    ):
        return None

    lx = max(a.lx, b.lx)
    hx = min(a.hx, b.hx)
    ly = max(a.ly, b.ly)
    hy = min(a.hy, b.hy)
    lz = max(a.lz, b.lz)
    hz = min(a.hz, b.hz)

    return Cuboid(lx, hx, ly, hy, lz, hz)


def add_volume(existing_volumes: List[Volume], new_volume: Volume) -> List[Volume]:
    """In place add a volume to a list of existing volumes.

    The existing_volumes will be extended with the following volumes:
        - The provided `step` (Volume) as is
        - Any overlapping volumes between `new_volume` and `existing_volumes` that are already on
          These new volumes will have state -1 to counteract the overlap.
    """
    new_volumes = [new_volume]
    for state, cuboid in existing_volumes:
        intersection = get_intersection(new_volume.cuboid, cuboid)
        if intersection and state:
            new_volumes.append(Volume(-1 * state, intersection))

    existing_volumes.extend(new_volumes)


def get_on_cube_count(volumes: List[Volume]):
    return sum(v.state * get_volume(v.cuboid) for v in volumes)


def part2(steps: List[Volume]) -> int:
    volumes = []
    for volume in steps:
        add_volume(volumes, volume)

    return get_on_cube_count(volumes)


def part1(steps: List[Volume]) -> int:
    volumes = []
    for volume in steps:
        if not any(abs(i) > 50 for i in volume.cuboid):
            add_volume(volumes, volume)

    return get_on_cube_count(volumes)


def main():
    steps = []
    with open("input") as f:
        for l in f:
            on_off, rest = l.split()
            ns = [int(x) for x in re.findall(r"-?\d+", rest)]
            cuboid = Cuboid(*sorted(ns[:2]), *sorted(ns[2:4]), *sorted(ns[4:]))
            volume = Volume(int(on_off == "on"), cuboid)
            steps.append(volume)

    print(part1(steps))
    print(part2(steps))


if __name__ == "__main__":
    main()
