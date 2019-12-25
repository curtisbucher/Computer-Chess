import ChessBoard
import random
import math
import os
from functools import lru_cache
import itertools

board = ChessBoard.chessboard()
# Variables for pruning
DEPTH = 4
PRUNE = 3


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


def score(board, score_move, black=True):
    """ Scores the curret move based on how many peices are on the board after the move is executed"""

    temp_board = ChessBoard.chessboard(board)
    start, end = tuple(score_move)
    temp_board.move_piece(start, end)

    offensive_scores = {"p": 1, "r": 5, "h": 3, "b": 3, "q": 9, "k": 130}
    defensive_scores = {"p": 1, "r": 5, "h": 3, "b": 3, "q": 9, "k": 40}

    total_score = 0
    for (x, y) in itertools.product(range(8), range(8)):
        piece = temp_board.pieces[y][x]
        if piece != " ":
            if piece.isupper() == black:  # upper and black or lower and not black
                total_score += offensive_scores[piece.lower()]
            else:
                total_score -= defensive_scores[piece.lower()]
    temp_board.move_piece(end, start)
    return total_score


def recur_score_move(depth, board, black=True, curr_depth=0):
    """ Scores the board by recursing `depth` moves deep. Prunes tree based by only taking the best half
    of moves"""

    tot_score = 0

    # Finding all the legal moves for the computer
    moves = gen_possible_moves(board, black)

    # Pruning, finding the best `number` of moves

    # Scoring
    for move in moves:
        move.score = score(board, move, black)
        tot_score += move.score

    # Sorting by score
    sorted_moves = sorted(moves, key=lambda x: x.score, reverse=True)
    moves = sorted_moves[0:PRUNE]

    if curr_depth < depth:
        # Runs if the maximum recursion depth is not reached

        # Scoring all the moves
        for move in moves:
            # Creating a new board, where the move was executed
            new_board = ChessBoard.chessboard(board)
            new_board.move_piece(move.start_coords, move.end_coords)

            # Scoring the move by adding all its own possible moves and subtracting the others. Deals with averages
            tot_score -= recur_score_move(
                depth, new_board, black=not black, curr_depth=curr_depth + 1
            ) / (
                PRUNE
            )  # ** depth)
    # returning score to collapse tree if not root
    # print(curr_depth)

    # If computer's turn to move, curr_depth will be an odd number and score will be returned positive
    # if curr_depth%2:
    # os.system('cls')
    # ChessBoard.draw_board(board, True)
    return tot_score


# If player's turn to move, curr_depth will be an even numver and score will be returned negetive
# else:
# return -score


def best_move(board, depth, black=True):
    """ Scores all the possible moves for the computer make by calling recur_score_move() on each move"""
    moves = gen_possible_moves(board, black)

    # For viewing processing time
    print("Legal Moves: " + str(len(moves)))
    print("-" * len(moves))

    for move in moves:
        print("#", end="", flush=True)
        # Creating a new board, where the move was executed
        new_board = ChessBoard.chessboard(board)
        # Executing and scoreing move`
        new_board.move_piece(move.start_coords, move.end_coords)
        move.score = score(board, move, black)

        # Recursively scoring next gen possible moves
        move.score -= recur_score_move(
            depth, new_board, black=not black, curr_depth=0
        ) / (
            PRUNE
        )  # ** depth)

    print()

    # Creating new, blank move with default score to be compared to max_move
    max_move = moves[0]

    # Finding the highest scoring move
    for move in moves:
        if move.score > max_move.score:
            max_move = move

    return max_move


def player_v_CPU():
    while ("k" in sum(board.pieces, [])) and ("K" in sum(board.pieces, [])):
        ChessBoard.draw_board(board, True)

        user_move = ChessBoard.get_move(board, False)
        while not user_move.legal_move:
            print("Illegal Move")
            print(user_move.black)
            user_move = ChessBoard.get_move(board, False)
        user_move.execute()

        # Testing for King in check
        is_check, is_black = ChessBoard.check(board)
        if is_check:
            print(
                ("Black" * is_black) + ("White" *
                                        (not is_black)) + " king is in check!"
            )

        max_move = best_move(board, DEPTH, True)
        max_move.execute()

        # Testing for King in check
        is_check, is_black = ChessBoard.check(board)
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

        ChessBoard.draw_board(board, True)

        A_max_move = best_move(board, DEPTH, False)
        A_max_move.execute()

        print("<<<", end=" ")
        print("Move: " + str(A_max_move))
        print("    Score: " + str(A_max_move.score))

        B_max_move = best_move(board, DEPTH, True)
        B_max_move.execute()

        print("<<<", end=" ")
        print("Move: " + str(B_max_move))
        print("    Score: " + str(B_max_move.score))

        # Ascii bell tone
        print("\a")


# CPU_v_CPU()
player_v_CPU()
