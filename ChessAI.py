import ChessBoard
import random
import math
board = ChessBoard.chessboard()

def gen_possible_moves(board, black = True):
    """ Goes through every single move on the board, finds which ones are
    legal, then returns a list of move objects that are legal"""
    legal_moves = []
    ## Iterating through every possible move on the board
    for sx in range(8):
        for sy in range(8):
            for ex in range(8):
                for ey in range(8):
                    if ChessBoard.legal_move(board, (sx,sy),(ex,ey), black):
                        legal_moves.append(ChessBoard.move(board,(sx,sy),(ex,ey),black))
    return legal_moves

def score(board, score_move, black = True,):
    temp_board = ChessBoard.chessboard(board)
    start, end = tuple(score_move)
    temp_board.move_piece(start, end)
    
    scores = {"p":10, "r":20, "h":30,"b":40, "q":100, "k":1000}
    total_score = 0
    for x in range(8):
        for y in range(8):
            piece = temp_board.pieces[y][x]
            if piece != " ":
                if (piece.isupper() and black) or (piece.islower() and not black):
                    total_score += scores[piece.lower()]
                else:
                    total_score -= scores[piece.lower()]
    temp_board.move_piece(end, start)
    return total_score         
            
                        
## Player is white
while True:
    ChessBoard.draw_board(board, True)
    
    user_move = ChessBoard.get_move(board,False)
    while not user_move.legal_move:
        print("Illegal Move")
        print(user_move.black)
        user_move = ChessBoard.get_move(board,False)
    user_move.execute()

    max_move = random.choice(gen_possible_moves(board))

    ## Scoring all the moves
    max_score = -math.inf
    max_move = gen_possible_moves(board)[0]
    for score_move in gen_possible_moves(board):
        move_score = score(board, score_move,True)
        if move_score > max_score:
            max_score = move_score
            max_move = score_move
            
    max_move.execute()
    print("<<<",end=" ")
    print("Move: " + str(max_move))
    print("    Score: " + str(max_score))


