import copy
import heapq
from collections import defaultdict
from itertools import product

DESTINATIONS = {
    "A": [(3, 2), (3, 3)],
    "B": [(5, 2), (5, 3)],
    "C": [(7, 2), (7, 3)],
    "D": [(9, 2), (9, 3)],
}
# The entrances to the different rooms
BLOCKED_COORDS = [(3, 1), (5, 1), (7, 1), (9, 1)]

MAX_X = 0
MAX_Y = 0
VALID_POSITIONS = []


class Burrow(defaultdict):
    def __str__(self):
        rows = []
        for y in range(MAX_X + 1):
            rows.append("".join(self[(x, y)] for x in range(MAX_Y + 1)))

        return "\n".join(rows)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, another):
        return hash(self) == hash(another)

    def __gt__(self, another):
        # hack to handle priority collision for tuples with Burrows on them
        return True


def is_solved(grid):
    for p, destinations in DESTINATIONS.items():
        for d in destinations:
            if grid[d] != p:
                return False

    return True


def get_cost(origin, destination, piece):
    x, y = origin
    nx, ny = destination
    md = abs(x - nx) + abs(y - ny)
    c = {"A": 1, "B": 10, "C": 100, "D": 1000}
    return md * c[piece]


def can_move(origin, destination, grid):
    # pylint: disable=too-many-branches,too-many-return-statements
    if destination in BLOCKED_COORDS:
        return False

    x, y = origin
    dx, dy = destination

    # moving from room
    if y > 1:
        # never move from room to room
        if dy > 1:
            return False

        p = grid[origin]
        # check if both pieces for this letter are already in place
        if all(grid[o] == p for o in DESTINATIONS[p]):
            return False

    # moving from hall
    if y == 1:
        # never move from hall to hall
        if dy == 1:
            return False

        p = grid[origin]
        possible_destinations = DESTINATIONS[p]
        # can only move to final destination
        if destination not in possible_destinations:
            return False

        # and only if other spot is either empty or occuppied by piece with same letter
        if any(grid[d] not in (p, ".", "#") for d in possible_destinations):
            return False

    # check collision on path
    path = []
    x_step = 1 if dx > x else -1
    if y < dy:
        for cx in range(x + x_step, dx + x_step, x_step):
            path.append((cx, y))

        for cy in range(y + 1, dy + 1):
            path.append((cx, cy))
    else:
        for cy in range(y - 1, dy - 1, -1):
            path.append((x, cy))

        for cx in range(x + x_step, dx + x_step, x_step):
            path.append((cx, cy))

    if any(grid[p] != "." for p in path):
        return False

    return True


def get_possible_moves(grid):
    origins = []
    destinations = []
    for (x, y) in VALID_POSITIONS:
        c = grid[(x, y)]

        if c == ".":
            destinations.append((x, y))
        elif c in "ABCD":
            origins.append((x, y))

    for origin, destination in product(origins, destinations):
        if not can_move(origin, destination, grid):
            continue

        cost = get_cost(origin, destination, grid[origin])
        yield cost, origin, destination


def solve(grid):
    queue = [(0, copy.copy(grid))]
    seen = set()
    while queue:
        energy, g = heapq.heappop(queue)
        if g in seen:
            continue

        if is_solved(g):
            return energy

        seen.add(g)
        for cost, f, t in get_possible_moves(g):
            ng = copy.copy(g)
            ng[t] = ng[f]
            ng[f] = "."
            nv = energy + cost
            heapq.heappush(queue, (nv, ng))

    return None


def burrow_from_lines(lines):
    grid = Burrow(lambda: "#")
    for y, l in enumerate(lines):
        for x, c in enumerate(l.center(len(lines[0]), "#")):
            grid[(x, y)] = c

    return grid


def valid_positions(burrow):
    positions = []
    for position, v in burrow.items():
        if v in ".ABCD" and position not in BLOCKED_COORDS:
            positions.append(position)

    return positions


def main():
    # pylint: disable=W0603
    global VALID_POSITIONS
    global MAX_X
    global MAX_Y
    with open("input") as f:
        lines = [l.strip() for l in f]

    grid = burrow_from_lines(lines)
    MAX_X = max(x for x, _ in grid.keys())
    MAX_Y = max(y for y, _ in grid.keys())
    VALID_POSITIONS = valid_positions(grid)

    # ~2m on my machine
    print(solve(grid))

    lines.insert(3, "#D#C#B#A#")
    lines.insert(4, "#D#B#A#C#")
    p2_grid = burrow_from_lines(lines)
    MAX_X = max(x for x, _ in p2_grid.keys())
    MAX_Y = max(y for y, _ in p2_grid.keys())
    VALID_POSITIONS = valid_positions(p2_grid)
    DESTINATIONS["A"].extend([(3, 4), (3, 5)])
    DESTINATIONS["B"].extend([(5, 4), (5, 5)])
    DESTINATIONS["C"].extend([(7, 4), (7, 5)])
    DESTINATIONS["D"].extend([(9, 4), (9, 5)])

    # ~7m on my machine
    print(solve(p2_grid))


if __name__ == "__main__":
    main()
