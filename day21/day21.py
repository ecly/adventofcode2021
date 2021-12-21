from collections import defaultdict, namedtuple
from functools import lru_cache
from itertools import cycle, product
from typing import Dict

GameState = namedtuple("GameState", "spaces scores turn")


def play_roll(state: GameState, roll: int) -> GameState:
    spaces, scores, turn = state
    space, score = spaces[turn], scores[turn]

    new_space = ((space - 1 + roll) % 10) + 1
    new_score = score + new_space

    new_spaces = list(spaces)
    new_spaces[turn] = new_space
    new_scores = list(scores)
    new_scores[turn] = new_score
    new_turn = (turn + 1) % len(spaces)

    return GameState(tuple(new_spaces), tuple(new_scores), new_turn)


@lru_cache(maxsize=None)
def play_quantum_game(state: GameState) -> Dict[int, int]:
    wins = defaultdict(int)
    for roll in [sum(x) for x in product([1, 2, 3], repeat=3)]:
        new_state = play_roll(state, roll)
        if new_state.scores[state.turn] >= 21:
            wins[state.turn] += 1
        else:
            new_wins = play_quantum_game(new_state)
            for p, w in new_wins.items():
                wins[p] += w

    return wins


def part2(p1, p2):
    start_state = GameState((p1, p2), (0, 0), 0)
    wins = play_quantum_game(start_state)
    return max(wins.values())


def part1(p1, p2):
    state = GameState((p1, p2), (0, 0), 0)
    rolls = 0
    die = cycle(range(1, 101))
    while all(s < 1000 for s in state.scores):
        roll = sum(next(die) for _ in range(3))
        state = play_roll(state, roll)
        rolls += 3

    return min(state.scores) * rolls


def main():
    p1, p2 = 8, 6
    print(part1(p1, p2))
    print(part2(p1, p2))


if __name__ == "__main__":
    main()
