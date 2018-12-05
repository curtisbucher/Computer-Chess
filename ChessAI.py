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

##def score(board,  start, end, black = True,):
##    temp_board = Chessboard.chessboard(board)
##    temp_board.move_piece(start, end)
##    
##    scores = {"p":10, "r":20, "h":30,"b":40, "q":100, "k":1000}
##    total_score = 0
##    for x in range(8):
##        for y in range(8):
##            piece = temp_board.pieces[y][x]
##            if piece != " ":
##                if (piece.isUpper() and black) or (piece.isLower() and not black):
##                    total_score += scores[piece.toLower()]
##                else:
##                    total_score -= scores[piece.toLower()]
##    return total_score         
##            
                        
## Player is white
while True:
    ChessBoard.draw_board(board, False)
    
    start, end = ChessBoard.get_move()
    while not ChessBoard.legal_move(board, start, end, False):
        print("Illegal Move")
        start, end = ChessBoard.get_move()
    board.move_piece(start,end)

    ## Making random legal move for AI
    max_score = -math.inf
    max_move = gen_possible_moves(board)[0]
    for move in gen_possible_moves(board):
        start, end = move
        score = score(board, True, start, end)
        if score > max_score:
            max_score = score
            max_move = move
            
    max_move.execute()
    print("<<<",end=" ")
    print(move)

