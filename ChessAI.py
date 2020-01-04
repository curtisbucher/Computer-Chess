import ChessBoard
import random
import math
import itertools
from multiprocessing import Pool, cpu_count

BOARD = ChessBoard.chessboard()
DEPTH = 3


def gen_possible_moves(board, black=True):
    """ Goes through every single move on the board, finds which ones are
    legal, then returns a list of move objects that are legal"""
    legal_moves = []
    # Iterating through every possible move on the board
    for (sx, sy, ex, ey) in itertools.product(range(8), range(8), range(8), range(8)):
        if ChessBoard.legal_move(board, (sx, sy), (ex, ey), black):
            legal_moves.append(ChessBoard.move(
                board, (sx, sy), (ex, ey), black))
    return legal_moves


def score_board(board):
    """ Scores the curret move based on how many peices are on the board after the move is executed"""
    offensive_scores = {"p": 1, "r": 5, "h": 3, "b": 3, "q": 9, "k": 130}
    defensive_scores = {"p": 1, "r": 5, "h": 3, "b": 3, "q": 9, "k": 40}

    total_score = 0
    for (x, y) in itertools.product(range(8), range(8)):
        piece = board.pieces[y][x]
        if piece != " ":
            if piece.isupper():   # black
                total_score += offensive_scores[piece.lower()]
            else:
                total_score -= defensive_scores[piece.lower()]
    return total_score


def alphabeta(board, depth, alpha, beta, black=True):
    # print(depth)
    if not depth:
        # ChessBoard.draw_board(board)
        return score_board(board)
    if black:
        value = -math.inf
        # Calculating node children
        for move in gen_possible_moves(board, black):

            # Creating a new child board that impliments the child
            child = ChessBoard.chessboard(board)
            child.move_piece(move.start_coords, move.end_coords)
            # Recursing down the child node
            value = max(value, alphabeta(
                child, depth - 1, alpha, beta, not black))

            alpha = max(alpha, value)
            if alpha >= beta:
                break
        # print(value)
        return value
    else:
        value = math.inf
        # Calculating node children
        for move in gen_possible_moves(board, black):

            # Creating a new child board that impliments the child
            child = ChessBoard.chessboard(board)
            child.move_piece(move.start_coords, move.end_coords)
            # Recursing down the child node
            value = min(value, alphabeta(
                child, depth - 1, alpha, beta, not black))

            beta = min(beta, value)
            if alpha >= beta:
                break

        return value


def score_branch(args):
    move, depth, black, new_board = args
    # Creating a new board, where the move was executed
    # Executing and scoreing move`
    new_board.move_piece(move.start_coords, move.end_coords)
    # move.score = score(board, move, black)
    score = alphabeta(new_board, depth, -math.inf, math.inf, black)
    print("#", end="", flush=True)
    return score


def best_move(board, depth, black=True):
    """ Scores all the possible moves for the computer make by calling recur_score_move() on each move"""
    moves = gen_possible_moves(board, black)
    print(id(moves[0]))

    # For viewing processing time
    print("Legal Moves: " + str(len(moves)))
    print("-" * len(moves))

    # Multiprocessing, one process for every branch to score
    P = Pool(cpu_count())
    args = [(move, depth, black, ChessBoard.chessboard(board))
            for move in moves]
    scores = P.map(score_branch, args)

    for x in range(len(moves)):
        moves[x].score = scores[x]

    print()

    # Creating new, blank move with default score to be compared to max_move
    max_move = moves[0]

    # Finding the highest scoring move
    for move in moves:
        if move.score > max_move.score:
            max_move = move
    return max_move


def player_v_CPU():
    quit = False
    while ("k" in sum(BOARD.pieces, [])) and ("K" in sum(BOARD.pieces, []) and quit == False):
        ChessBoard.draw_board(BOARD, True)

        user_move = ChessBoard.get_move(BOARD, False)
        if not user_move:
            print("Terminating...")
            break

        while not user_move.legal_move:
            print("Illegal Move")
            print(user_move.black)
            user_move = ChessBoard.get_move(BOARD, False)
        user_move.execute()

        # Testing for King in check
        is_check, is_black = ChessBoard.check(BOARD)
        if is_check:
            print(
                ("Black" * is_black) + ("White" *
                                        (not is_black)) + " king is in check!"
            )

        max_move = best_move(BOARD, DEPTH, True)
        max_move.execute()

        # Testing for King in check
        is_check, is_black = ChessBoard.check(BOARD)
        if is_check:
            print(
                ("Black" * is_black) + ("White" *
                                        (not is_black)) + " king is in check!"
            )

        # Ascii bell tone
        print("\a")

        print("<<<", end=" ")
        print("Move: " + str(max_move))
        print("    Score: " + str(max_move.score))


def CPU_v_CPU():
    while True:

        ChessBoard.draw_board(BOARD, True)

        A_max_move = best_move(BOARD, DEPTH, False)
        A_max_move.execute()

        print("<<<", end=" ")
        print("Move: " + str(A_max_move))
        print("    Score: " + str(A_max_move.score))

        B_max_move = best_move(BOARD, DEPTH, True)
        B_max_move.execute()

        print("<<<", end=" ")
        print("Move: " + str(B_max_move))
        print("    Score: " + str(B_max_move.score))

        # Ascii bell tone
        print("\a")


# CPU_v_CPU()
player_v_CPU()
