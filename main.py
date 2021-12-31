import sys

orij_words = None


def print_board(board):
    for row in board:
        for char in row:
            if char is None:
                print("-", end=" ")
            else:
                print(char, end=" ")

        print()
    print()


class BoardPutPossibility:
    def __init__(self, row, col, hor):
        self.row = row
        self.col = col
        self.hor = hor


def get_first_word_position(rows, cols, word):
    mid_row = rows // 2 - 1
    mid_col = cols // 2 - 1
    mid_word = len(word) // 2
    return mid_row, mid_col - mid_word


def put_word_on_board(word, board, row, col, hor):
    if hor:
        for i, char in enumerate(word):
            board[row][col + i] = word[i]
    else:
        for i, char in enumerate(word):
            board[row + i][col] = word[i]


def makes_new_perp_word(board, char, row, col, hor):
    prev_char = board[row][col]
    board[row][col] = char
    try:
        if hor:
            end_col = col
            for i in range(0, len(board[0])):
                if board[row][col + i] is not None:
                    end_col = col + i
                else:
                    break

            start_col = col
            for i in range(0, len(board[0])):
                if board[row][col - i] is not None:
                    start_col = col - i
                else:
                    break

            if start_col == end_col:
                return False

            string = ""
            for i in range(start_col, end_col + 1):
                string += board[row][i]

            for word in orij_words:
                if string == word:
                    return False

            print("{} is a new word".format(string))
            # print_board(board)
            return True

        else:
            end_row = row
            for i in range(0, len(board[0])):
                if board[row + i][col] is not None:
                    end_row = row + i
                else:
                    break

            start_row = row
            for i in range(0, len(board[0])):
                if board[row - i][col] is not None:
                    start_row = row - i
                else:
                    break

            if start_row == end_row:
                return False

            string = ""
            for i in range(start_row, end_row + 1):
                string += board[i][col]

            for word in orij_words:
                if string == word:
                    return False

            print("{} is a new word".format(string))
            # print_board(board)
            return True

    finally:
        board[row][col] = prev_char


# you have a problem if there is a character there and it is not the same as the one you are trying to lay down
def can_put_word_on_board(word, board, row, col, hor):

    row_inc = 0
    col_inc = 0
    if hor:
        col_inc += 1
    else:
        row_inc += 1

    for i, char in enumerate(word):
        char_at_spot_on_board = board[row + (row_inc * i)][col + (col_inc * i)]
        if char_at_spot_on_board != char and char_at_spot_on_board is not None:
            return False
        elif makes_new_perp_word(board, char, row + (row_inc * i), col + (col_inc * i), not hor):
            return False
    return True


def get_word_on_board_possibilities(word, board):
    def validate_not_dupe_and_put_in_possibilities(possibility, possibilities_in_func):
        for x in possibilities_in_func:
            if x.row == possibility.row and x.col == possibility.col and x.hor == possibility.hor:
                return False

        possibilities_in_func.append(possibility)
        return True

    possibilities = []

    for char_pos, char in enumerate(word):
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell == char:
                    can_hor = can_put_word_on_board(word, board, i, j - char_pos, True)
                    can_vert = can_put_word_on_board(word, board, i - char_pos, j, False)

                    if can_hor:
                        # print("can hor")
                        validate_not_dupe_and_put_in_possibilities(BoardPutPossibility(i, j - char_pos, True),
                                                                   possibilities)
                    if can_vert:
                        # print("can vert")
                        validate_not_dupe_and_put_in_possibilities(BoardPutPossibility(i - char_pos, j, False),
                                                                   possibilities)

    return possibilities


def deep_copy_board(board):
    return [row[:] for row in board]


def recurse_on_word(board, words):
    # print("recursing with words {}".format(len(words)))
    if len(words) == 0:
        return [deep_copy_board(board)]

    board_deep_copy = deep_copy_board(board)
    all_finished_boards = []

    word = words[0]
    # print("Seeing if we can put word {} on the board".format(word))
    board_put_possibilities = get_word_on_board_possibilities(word, board)
    for board_poss in board_put_possibilities:
        put_word_on_board(word, board, board_poss.row, board_poss.col, board_poss.hor)
        curr_finished_boards = recurse_on_word(board, words[1:])
        # print("curr_finished_boards: {}".format(curr_finished_boards))
        board = board_deep_copy
        board_deep_copy = deep_copy_board(board)
        all_finished_boards.extend(curr_finished_boards)

    return all_finished_boards


def run_algo(args, board):
    # print_board(board)
    first_word_row, first_word_col = get_first_word_position(len(board), len(board[0]), args[0])
    put_word_on_board(args[0], board, first_word_row, first_word_col, True)

    valid_boards = recurse_on_word(board, args[1:])

    print("there are {} valid boards. Here they are".format(len(valid_boards)))
    for valid_board in valid_boards:
        print_board(valid_board)


def main():
    empty_board = []
    for i in range(40):
        row = []
        for j in range(40):
            row.append(None)
        empty_board.append(row)

    words = sys.argv[1:]

    global orij_words
    orij_words = [word for word in words]

    run_algo(words, empty_board)

    # for i in range(len(words)):
    #     # shuffle
    #     words.append(words[0])
    #     words = words[1:]
    #
    #     run_algo(words, deep_copy_board(empty_board))









main()
