## A Chess package for playing chess against another user
## Problem with legal bishop function alwasy out of range when scanning to make sure path is clear.
import copy
class chessboard:
    """ The Chessboard object that contains the peices and their positions on
    the board, and enables the user to move the peices, legally or otherwise"""
    def __init__(self, board = False):
        ## Switch capital and lowercase
        if not board:
            self.pieces = [["r","h","b","k","q","b","h","r"],
                          ["p","p","p","p","p","p","p","p"],
                          [" "," "," "," "," "," "," "," "],
                          [" "," "," "," "," "," "," "," "],
                          [" "," "," "," "," "," "," "," "],
                          [" "," "," "," "," "," "," "," "],
                          ["P","P","P","P","P","P","P","P"],
                          ["R","H","B","K","Q","B","H","R"]]
        else:
            self.pieces = copy.deepcopy(board.pieces)
            
        self.board = board
        self.pawn = "Pp"
        self.rook = "Rr"
        self.horse = "Hh"
        self.bishop = "Bb"
        self.king = "Kk"
        self.queen = "Qq"
                
    def move_piece(self, start_coords, end_coords):
        """ Moves a peice from one spot to another on the board, regardless of
        legality. The starting position of the peice is left empty"""
        ax,ay = end_coords
        x,y = start_coords
        
        self.pieces[ay][ax] = self.pieces[y][x]
        self.pieces[y][x] = " "

class move:
    """ This class includes all the variables for a single move on the chessboard, as well
    as mathods for moving"""
    def __init__(self,board, start_coords, end_coords, black = False):
        """ Defining the necessary movement variables, as well as a boolean for legal_move"""
        self.board = board
        self.start_coords = start_coords
        self.end_coords = end_coords
        self.black = black

        if board:
            self.legal_move = legal_move(self.board, self.start_coords, self.end_coords, black)
    
    def execute(self):
        """ If the move is legal, moves the peice and returns true, else returns false"""
        if self.legal_move:
            self.board.move_piece(self.start_coords, self.end_coords)
            return True
        return False
    
    def __str__(self):
        """ Returns a string of the move in chess notation. Ex, A1B2"""
        letters = ["A","B","C","D","E","F","G","H"]
        return (letters[self.start_coords[0]] + str(self.start_coords[1]) +
               letters[self.end_coords[0]] + str(self.end_coords[1]))
    def __iter__(self):
        """ Allows tuple() or list() to be called on a move object. Returns a two part iterable with
        start coords at index 0 and end coords at index 1"""
        for i in range(2):
            if not i:
                yield self.start_coords
            else:
                yield self.end_coords
    def __eq__(self, other):
        """ Tests if two move objects are equal to one another"""
        return(self.start_coords == other.start_coords and other.end_coords == self.end_coords)
        

def legal_move(board, start, end ,black = False):
    """ Checking if the move follows any of the rules, which includes
    being that type of peice"""
    (x, y) = start
    (ax, ay) = end

    ## Checking each individual move function to see if the move is legal, and then checking
    ## to make sure the piece isn't taking his own man
    if((legal_white_pawn(board, start, end) or legal_black_pawn(board, start, end)
        or legal_rook(board, start, end) or legal_horse(board, start, end)
        or legal_bishop(board, start, end) or legal_king(board, start, end)
        or legal_queen(board, start, end))
        and ((not black and board.pieces[y][x].islower() and not board.pieces[ay][ax].islower())
            or (black and board.pieces[y][x].isupper() and not board.pieces[ay][ax].isupper()))):
        return True
    return False

def legal_white_pawn(board, start, end):

    x1, y1 = start
    x2, y2 = end

    if board.pieces[y1][x1] != board.pawn[1]:
        return False
    
    dx = abs(x2 - x1)
    dy = y2 - y1

    # Can move the pawn if...
    # Moving one forward with no horizontal movement, and with no one in front
    if dy == 1 and dx == 0 and board.pieces[y2][x2] == " ":
        return True
    # Moving two forward with no horizontal movement, and with no one within two spaces
    elif dy == 2 and dx == 0 and y1 == 1 and board.pieces[y1+1][x2] == " " and board.pieces[y1+2][x2] == " ":
        return True
    # If someone is adjecant and the player moves there
    elif board.pieces[y2][x2].isupper() and dy == 1 and dx == 1:
        return True
    # Otherwise false
    else:
        return False

def legal_black_pawn(board, start, end):

    x1, y1 = start
    x2, y2 = end

    if board.pieces[y1][x1] != board.pawn[0]:
        return False
    
    dx = abs(x2 - x1)
    dy = y2 - y1

    # Can move the pawn if...
    # Moving one backward with no horizontal movement, and with no one in behind
    if dy == -1 and dx == 0 and board.pieces[y2][x2] == " ":
        return True

    # Moving two backward with no horizontal movement, and with no one within the two spaces
    elif dy == -2 and dx == 0 and y1 == 6 and board.pieces[y1-1][x2] == " " and board.pieces[y1-2][x2] == " ":
        return True
    # If someone is adjecent and the player moves there
    elif board.pieces[y2][x2].islower() and dy == -1 and dx == 1:
        return True
    # Otherwise False
    else:
        return False

def legal_rook(board, start, end):
        
    x1, y1 = start
    x2, y2 = end

    if board.pieces[y1][x1] not in board.rook:
        return False
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    ## Testing for pieces in the current pieces path of travel
    ## Horizontal
    if(x2 > x1 and dy == 0):
        if(board.pieces[y1][x1 + 1:x2].count(' ')
           != len(board.pieces[y1][x1 + 1:x2])):
            return False
    
    if(x2 < x1 and dy == 0):
        if(board.pieces[y1][x2:x1 + 1].count(' ')
           != len(board.pieces[y1][x2:x1])):
            return False
    ## Verticle
    if(y2 > y1 and dx == 0):
            for x in range(1,dy):
                if(board.pieces[y1+x][x1] != " "):
                    return False
        
    if(y2 < y1 and dx == 0):
            for x in range(1,dy):
                if(board.pieces[y2+x][x1] != " "):
                    return False
                    
    
    # Can move if only going in one direction
    if dy and not dx:
        return True
    elif dx and not dy:
        return True
    else:
        return False

def legal_horse(board, start, end):

    x1, y1 = start
    x2, y2 = end

    if board.pieces[y1][x1] not in board.horse:
        return False
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    ## Can move if going two spaces in one direction and one in another
    ## It doesnt matter if anyone is in the way
    if dy == 2 and dx == 1:
        return True
    elif dy == 1 and dx == 2:
        return True
    else:
        return False


def legal_bishop(board, start, end):
        
    x1, y1 = start
    x2, y2 = end

    if board.pieces[y1][x1] not in board.bishop:
        return False
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    # Cannot move if they are not moving the same distance x and y
    if dy != dx:
        return False

    # Check to see if the bishop's path is open
        if(x1 < x2):
            directionX = 1
        else:
            directionX = -1

        if(y1 < y2):
            directionY = 1
        else:
            directionY = -1

        for a in range(1,dx):
            if board.pieces[y1 +(a * directionY)][x1+ (a*directionX)] != " ":
                return False

def legal_king(board, start, end):
        
    x1, y1 = start
    x2, y2 = end

    if board.pieces[y1][x1] not in board.king:
        return False

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

# Can only move 1 tile in 1 direction
    if dy == 1 and dx == 0:
        return True
    elif dx == 1 and dy == 0:
        return True
    else:
        return False
    
def legal_queen(board, start, end):
        
    x1, y1 = start
    x2, y2 = end

    if board.pieces[y1][x1] not in board.queen:
        return False
    
    ## A queen is the same as a rook and bishop combined
    if legal_bishop(board, start, end) or legal_rook(board, start, end):
        return True
    else:
        return False
        
def get_move(board = False, black = False):
    letters = ["A","B","C","D","E","F","G","H"]
    raw = input(">>> ")

    start = (letters.index(raw[0]),int(raw[1]))
    end = (letters.index(raw[2]), int(raw[3]))
    
    new_move = move(board, start, end, black)
    return new_move
        
def draw_board(board,flipped = False):
    """ Prints the chess board from the white perspective unless
    flipped = True, when it goes from the black perspective"""
    
    if not flipped:
        print("     A     B     C     D     E     F     G     H")
        print("  :-----:-----:-----:-----:-----:-----:-----:-----: ")
        for y in range(8):
            print(y, end = "")
            for x in range(8):
                print(" :  " + board.pieces[y][x], end = " ")
            print(" : \n  :-----:-----:-----:-----:-----:-----:-----:-----: ")
    else:
        print("     A     B     C     D     E     F     G     H")
        print("  :-----:-----:-----:-----:-----:-----:-----:-----: ")
        for y in range(7,-1,-1):
            print(y, end = "")
            for x in range(8):
                print(" :  " + board.pieces[y][x], end = " ")
            print(" : \n  :-----:-----:-----:-----:-----:-----:-----:-----: ")

def check(board):
    ## Finding the positions of both kings, returns two bools. in_check, is_black
    white_king_coords = (0,0)
    black_king_coords = (0,0)
    
    for x in range(8):
        for y in range(8):
            if board[y][x] == "k":
                white_king_coords = (x,y)
            if board[y][x] == "K":
                black_king_coords = (x,y)
            
                
    for x in range(8):
        for y in range(8):
            if legal_move(board,(x,y),white_king_coords, True):
                return True, False
            if legal_move(board,(x,y),black_king_coords, False):
                return True, True
        return False, False

if __name__ == "__main__": 
    turn = 0
    board = chessboard()
    while True:
        draw_board(board, turn%2)
        new_move = get_move(board,turn%2)
        while not new_move.legal_move:
            print("Illegal Move")
            new_move = get_move(board,turn%2)
        new_move.execute()
        turn += 1
