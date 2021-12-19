import fileinput
import math
from copy import deepcopy
from itertools import permutations
from typing import List, Optional, Union


class SnailfishNumber:  # pylint:disable=missing-class-docstring
    def __init__(
        self,
        left_or_val: Union["SnailfishNumber", List, int],
        right: Optional[Union["SnailfishNumber", List, int]] = None,
        parent: Optional["SnailfishNumber"] = None,
    ):
        if right is None:
            assert isinstance(left_or_val, int)
            self.left = left_or_val
            self.right = None
            self.parent = parent
            return

        if isinstance(left_or_val, list):
            assert len(left_or_val) == 2
            self.left = SnailfishNumber(*left_or_val, parent=self)
        elif isinstance(left_or_val, SnailfishNumber):
            left_or_val.parent = self
            self.left = left_or_val
        else:
            self.left = SnailfishNumber(left_or_val, parent=self)

        if isinstance(right, list):
            assert len(right) == 2
            self.right = SnailfishNumber(*right, parent=self)
        elif isinstance(right, SnailfishNumber):
            right.parent = self
            self.right = right
        elif isinstance(right, int):
            self.right = SnailfishNumber(right, parent=self)
        else:
            self.right = None

        self.parent = parent

    @property
    def is_value(self):
        return self.right is None

    @property
    def value(self):
        assert self.is_value
        return self.left

    @property
    def is_left(self):
        """Whether this node is the left node of its parent."""
        if self.parent.left == self:
            return True

        assert self.parent.right == self
        return False

    @property
    def nestation(self):
        level = 0
        n = self
        while True:
            p = n.parent
            if not p:
                break

            level += 1
            n = p

        return level

    def traverse(self):
        if self.is_value:
            yield self
            return

        yield from self.left.traverse()
        yield from self.right.traverse()
        return

    def reduce(self):  # pylint: disable=too-many-branches
        while True:
            # print(self)
            nums = list(self.traverse())
            is_reduced = True

            # explode loop
            for i, n in enumerate(nums):
                # because we iterate values we traverse values nestation should be 5 instead of 4
                # we always find with `n` as its left value due to the ordered traversal
                if n.nestation >= 5:
                    p = n.parent
                    if i != 0:
                        nums[i - 1].left += p.left.value
                    if i != len(nums) - 2:
                        nums[i + 2].left += p.right.value

                    pp = p.parent
                    if p.is_left:
                        pp.left = SnailfishNumber(0, parent=pp)
                    else:
                        pp.right = SnailfishNumber(0, parent=pp)

                    is_reduced = False
                    break

            if not is_reduced:
                continue

            # split loop
            for i, n in enumerate(nums):
                if n.value >= 10:
                    p = n.parent
                    replacement = SnailfishNumber(
                        math.floor(n.value / 2), math.ceil(n.value / 2), parent=p
                    )
                    if n.is_left:
                        p.left = replacement
                    else:
                        p.right = replacement

                    is_reduced = False
                    break

            if is_reduced:
                break

        return self

    def magnitude(self):
        if self.is_value:
            return self.value

        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def __str__(self):
        if self.is_value:
            return str(self.left)

        return f"[{self.left},{self.right}]"

    def __add__(self, other):
        return SnailfishNumber(self, other).reduce()


def line_to_snail(l):
    return SnailfishNumber(*eval(l))  # pylint: disable=W0123


def part1(lines):
    numbers = [line_to_snail(l) for l in lines]
    final = numbers[0]
    for n in numbers[1:]:
        final += n

    return final.magnitude()


def part2(lines):
    numbers = [line_to_snail(l) for l in lines]
    return max(
        (deepcopy(a) + deepcopy(b)).magnitude() for a, b in permutations(numbers, 2)
    )


def main():
    with fileinput.input("input") as f:
        lines = [l.strip() for l in f]

    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    main()
