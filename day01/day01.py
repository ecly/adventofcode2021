import fileinput
depths = list(map(int, fileinput.input()))
print(sum(x < y for x, y in zip(depths, depths[1:])))
sliding_windows = [sum(t) for t in zip(depths, depths[1:], depths[2:])]
print(sum(x < y for x, y in zip(sliding_windows, sliding_windows[1:])))
