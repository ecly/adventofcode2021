import sys


def did_board_win(board, numbers):
    for i, row in enumerate(board):
        column = []
        for j in range(5):
            column.append(board[j][i])

        if all(i in numbers for i in column) or all(i in numbers for i in row):
            return True

    return False


def get_score(board, numbers):
    unmarked = [n for l in board for n in l if n not in numbers]
    return sum(unmarked) * numbers[-1]


def get_winners(boards, numbers):
    for i in range(1, len(numbers)):
        n = numbers[:i]
        incomplete_boards = []
        for board in boards:
            if did_board_win(board, n):
                yield board, n
            else:
                incomplete_boards.append(board)

        boards = incomplete_boards


def part1(boards, numbers):
    board, n = next(get_winners(boards, numbers))
    return get_score(board, n)


def part2(boards, numbers):
    winners = list(get_winners(boards, numbers))
    return get_score(*winners[-1])


def get_boards_and_numbers():
    numbers, *blocks = sys.stdin.read().strip().split("\n\n")
    numbers = list(map(int, numbers.split(",")))
    boards = []
    for block in blocks:
        lines = block.splitlines()
        board = []
        for line in lines:
            board.append(list(map(int, line.split())))

        boards.append(board)

    return boards, numbers


def main():
    boards, numbers = get_boards_and_numbers()
    print(part1(boards, numbers))
    print(part2(boards, numbers))


if __name__ == "__main__":
    main()
