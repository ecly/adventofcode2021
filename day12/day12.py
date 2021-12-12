import fileinput
from collections import defaultdict, deque


def get_paths(adj, is_part2=False):
    finished = set()
    queue = deque([(["start"], False)])
    while queue:
        path, seen_small_twice = queue.popleft()
        current = path[-1]
        if current == "end":
            finished.add(tuple(path))
            continue

        for n in adj[current]:
            if n == "start":
                continue
            if n.isupper() or n not in path:
                queue.append((path + [n], seen_small_twice))
            if not seen_small_twice and is_part2:
                queue.append((path + [n], True))

    return set(tuple(f) for f in finished)


def part1(adj):
    paths = get_paths(adj)
    return len(paths)


def part2(adj):
    paths = get_paths(adj, is_part2=True)
    return len(paths)


def main():
    adj = defaultdict(list)
    with fileinput.input("input") as f:
        for l in f:
            a, b = l.strip().split("-")
            adj[a].append(b)
            adj[b].append(a)

    print(part1(adj))
    print(part2(adj))


if __name__ == "__main__":
    main()
