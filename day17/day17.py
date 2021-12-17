def test_config(vx, vy, *input_):
    lx, hx, ly, hy = input_
    x, y = 0, 0
    max_y = 0
    while True:
        x += vx
        y += vy
        if vx != 0:
            vx += -1 if vx > 0 else 1
        vy -= 1
        max_y = max(y, max_y)
        if ly <= y <= hy and lx <= x <= hx:
            return max_y

        if x > hx:
            return -1

        if y < ly:
            return -1


def part1(*input_):
    max_y = 0
    b = input_[1]
    for vx in range(1, b):
        for vy in range(-b, abs(b)):
            ny = test_config(vx, vy, *input_)
            if ny > max_y:
                print(vx, vy)
                max_y = ny

    return max_y


def part2(*input_):
    c = 0
    lb, hb = -input_[1] * 2, input_[1] * 2
    for vx in range(lb, hb):
        for vy in range(lb, hb):
            ny = test_config(vx, vy, *input_)
            if ny >= 0:
                c += 1

    return c


def main():
    input_ = 185, 221, -122, -74
    print(part1(*input_))
    print(part2(*input_))


if __name__ == "__main__":
    main()
