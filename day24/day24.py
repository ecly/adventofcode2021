from typing import Optional


def find_valid_model_number(instructions, digits):
    seen = set()

    def recurse(step, register, model) -> Optional[int]:
        if step >= len(instructions):
            if register["z"] == 0:
                return int(model)

            return None

        ins, *r = instructions[step]

        if ins == "inp":
            for d in digits:
                if step == 0:
                    print(d)
                nr = register.copy()
                nr[r[0]] = d
                key = (str(nr), len(model))
                if key not in seen:
                    seen.add(key)
                    result = recurse(step + 1, nr, model + str(d))
                    if result:
                        return result

            return None

        a, b = r
        b = register[b] if b.isalpha() else int(b)
        if ins == "add":
            register[a] = register[a] + b
        if ins == "mul":
            register[a] = register[a] * b
        if ins == "div":
            register[a] = register[a] // b
        if ins == "mod":
            register[a] = register[a] % b
        if ins == "eql":
            register[a] = int(register[a] == b)

        return recurse(step + 1, register, model)

    return recurse(0, {"w": 0, "x": 0, "y": 0, "z": 0}, "")


def part1(instructions):
    return find_valid_model_number(instructions, range(9, 0, -1))


def part2(instructions):
    return find_valid_model_number(instructions, range(1, 10))


def main():
    with open("input") as f:
        instructions = [l.strip().split() for l in f]

    # takes about ~6 minutes for both with pypy3 on my machine
    print(part1(instructions))
    print(part2(instructions))


if __name__ == "__main__":
    main()
