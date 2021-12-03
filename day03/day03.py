import fileinput
from collections import Counter, defaultdict


def get_most_common_for_pos(nums, pos):
    bits = [n[pos] for n in nums]
    (b1, c1), (_, c2) = Counter(bits).most_common(2)
    return "1" if c1 == c2 else b1


def part1(nums):
    positions = defaultdict(list)
    for num in nums:
        for idx, bit in enumerate(num):
            positions[idx].append(bit)

    most_common = []
    least_common = []
    for idx, bits in positions.items():
        (b1, _), (b2, _) = Counter(bits).most_common(2)
        most_common.append(b1)
        least_common.append(b2)

    gamma_rate = int("".join(most_common), 2)
    epsilon = int("".join(least_common), 2)
    return gamma_rate * epsilon


def part2(nums):
    most_common = nums[::]
    least_common = nums[::]
    for i in range(len(nums[0])):
        if len(most_common) > 1:
            mc = get_most_common_for_pos(most_common, i)
            most_common = [x for x in most_common if x[i] == mc]
        if len(least_common) > 1:
            lc = str(abs(int(get_most_common_for_pos(least_common, i)) - 1))
            least_common = [x for x in least_common if x[i] == lc]

    oxygen_generator_rating = int("".join(most_common), 2)
    c02_scrubber_rating = int("".join(least_common), 2)
    return oxygen_generator_rating * c02_scrubber_rating


def main():
    nums = []
    for line in fileinput.input():
        nums.append(line.strip())

    print(part1(nums))
    print(part2(nums))


if __name__ == "__main__":
    main()
