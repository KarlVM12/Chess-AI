import os.path
import math
import pygame
import enum
#import alphaBetaPruning as ab
pygame.init()

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500
ROWS = 8
COLS = 8
SQUARE_SIZE = 46
BOARD_SIZE = SQUARE_SIZE * COLS
BOARD_START_X = int(( SCREEN_WIDTH / 2 ) - (BOARD_SIZE / 2))
BOARD_END_X = int(( SCREEN_WIDTH / 2 ) + (BOARD_SIZE / 2))

DARK_SQUARE_COLOR = (102,0,0)
LIGHT_SQUARE_COLOR = (248,231,187)
BACKGROUND_COLOR = (251,245,222)
SELECTED_COLOR = (0,68,116)

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Chess AI')
#boardSquares = [[0 for i in range(COLS)] for j in range(ROWS)]
#previousMove = [0 for i in range(2)]

#Sprites
PAWN_W_SPRITE = pygame.image.load(os.path.join("Sprites", "pawn_w.png")).convert_alpha()
PAWN_B_SPRITE = pygame.image.load(os.path.join("Sprites", "pawn_b.png")).convert_alpha()
ROOK_W_SPRITE = pygame.image.load(os.path.join("Sprites", "rook_W.png")).convert_alpha()
ROOK_B_SPRITE = pygame.image.load(os.path.join("Sprites", "rook_b.png")).convert_alpha()
KNIGHT_W_SPRITE = pygame.image.load(os.path.join("Sprites", "knight_w.png")).convert_alpha()
KNIGHT_B_SPRITE = pygame.image.load(os.path.join("Sprites", "knight_b.png")).convert_alpha()
BISHOP_W_SPRITE = pygame.image.load(os.path.join("Sprites", "bishop_w.png")).convert_alpha()
BISHOP_B_SPRITE = pygame.image.load(os.path.join("Sprites", "bishop_b.png")).convert_alpha()
QUEEN_W_SPRITE = pygame.image.load(os.path.join("Sprites", "queen_w.png")).convert_alpha()
QUEEN_B_SPRITE = pygame.image.load(os.path.join("Sprites", "queen_b.png")).convert_alpha()
KING_W_SPRITE = pygame.image.load(os.path.join("Sprites", "king_w.png")).convert_alpha()
KING_B_SPRITE = pygame.image.load(os.path.join("Sprites", "king_b.png")).convert_alpha()


class Piece(enum.Enum):
    EMPTY = "EMPTY"
    PAWN = "PAWN"
    ROOK = "ROOK"
    KNIGHT = "KNIGHT"
    BISHOP = "BISHOP"
    QUEEN = "QUEEN"
    KING = "KING"


class Square:
    def __init__(self, x = 0, y = 0, piece = Piece.EMPTY, pieceColor = None, sprite = None):
        self.x = x
        self.y = y
        self.row = int((y - BOARD_START_X) / SQUARE_SIZE)
        self.col = int((x - BOARD_START_X) / SQUARE_SIZE) 
        self.piece = piece
        self.firstMove = False
        if(self.piece == Piece.PAWN):
            self.firstMove = True

        self.pieceColor = pieceColor
        self.sprite = sprite

    def copy(self, square):
        self.x = square.x
        self.y = square.y
        self.row = square.row
        self.col = square.col 
        self.piece = square.piece
        self.pieceColor = square.pieceColor
        self.sprite = PieceSprite((x,y), square.sprite.image)

    def __str__(self) -> str:
        return "( " + str(self.y) + ", " + str(self.x) + ") [ " + str(self.row) + ", " + str(self.col) + "] " + str(self.piece) + " " + str(self.sprite)

class PieceSprite(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

    # checks the destination square, if its the same color, false, else removes what is there or just moves
    def checkAndRemove(self, game, newrow, newcol, color):
        # if rows are empty but destination has an opoosite color piece, removes the piece and moves
        if(game.boardSquares[newrow][newcol].piece != Piece.EMPTY):
            if(game.boardSquares[newrow][newcol].pieceColor == color):
                return False

            game.pieces.remove(game.boardSquares[newrow][newcol].sprite)
            return True

        # if destination is just empty, valid move
        return True

    def validMove(self, game, piece, color, oldrow, oldcol, newrow, newcol):
        
        # --Black and white Pawns--
        if(piece == Piece.PAWN):
            if(color == "black"):
                
                # first move where it can go 2 squares
                if(game.boardSquares[oldrow][oldcol].firstMove and newrow == oldrow+2 and newcol == oldcol and game.boardSquares[oldrow+1][newcol].piece == Piece.EMPTY and game.boardSquares[newrow][newcol].piece == Piece.EMPTY):
                    game.boardSquares[oldrow][oldcol].firstMove = False
                    return True
                # just moving forward    
                if(newrow == oldrow+1 and oldcol == newcol and game.boardSquares[newrow][newcol].piece == Piece.EMPTY):
                    return True
                # moving diagonal to capture a piece
                if(newrow == oldrow+1 and (newcol == oldcol-1 or newcol == oldcol+1) and game.boardSquares[newrow][newcol].piece != Piece.EMPTY and game.boardSquares[newrow][newcol].pieceColor != "black"):
                    game.pieces.remove(game.boardSquares[newrow][newcol].sprite)
                    return True
                
            if(color == "white"):
                # first move where it can go 2 squares
                if(game.boardSquares[oldrow][oldcol].firstMove and newrow == oldrow-2 and newcol == oldcol and game.boardSquares[oldrow-1][newcol].piece == Piece.EMPTY and game.boardSquares[newrow][newcol].piece == Piece.EMPTY):
                    game.boardSquares[oldrow][oldcol].firstMove = False
                    return True
                # just moving forward
                if(newrow == oldrow-1 and oldcol == newcol and game.boardSquares[newrow][newcol].piece == Piece.EMPTY):
                    return True
                # moving diagonal to capture a piece
                if(newrow == oldrow-1 and (newcol == oldcol-1 or newcol == oldcol+1 )and game.boardSquares[newrow][newcol].piece != Piece.EMPTY and game.boardSquares[newrow][newcol].pieceColor != "white"):
                    game.pieces.remove(game.boardSquares[newrow][newcol].sprite)
                    return True

        # --Black and White Rook and Queen--
        if(piece == Piece.ROOK or piece == Piece.QUEEN):
            if((newrow != oldrow and newcol == oldcol)):
                # checks if up and down columns are empty
                if(newrow >= oldrow):
                    for i in range(oldrow+1, newrow):
                        if (game.boardSquares[i][newcol].piece != Piece.EMPTY):
                            return False
                elif (newrow < oldrow):
                    for i in range(newrow+1, oldrow):
                        if (game.boardSquares[i][newcol].piece != Piece.EMPTY):
                            return False

                # if destination is not empty but has an opposite color piece, removes that piece
                if(game.boardSquares[newrow][newcol].piece != Piece.EMPTY):
                    if(game.boardSquares[newrow][newcol].pieceColor == color):
                        return False

                    game.pieces.remove(game.boardSquares[newrow][newcol].sprite)
                    return True

                # if destination is just empty, valid move
                return True

            if(newrow == oldrow and newcol != oldcol):
                # checks if rows between move is all empty
                if(newcol >= oldcol):
                    for i in range(oldcol+1, newcol):
                        if (game.boardSquares[newrow][i].piece != Piece.EMPTY):
                            return False
                elif (newcol < oldcol):
                    for i in range(newcol+1, oldcol):
                        if (game.boardSquares[newrow][i].piece != Piece.EMPTY):
                            return False

                # if rows are empty but destination has an opoosite color piece, removes the piece and moves
                if(game.boardSquares[newrow][newcol].piece != Piece.EMPTY):
                    if(game.boardSquares[newrow][newcol].pieceColor == color):
                        return False

                    game.pieces.remove(game.boardSquares[newrow][newcol].sprite)
                    return True

                # if destination is just empty, valid move
                return True
            
        # --Black and White Knight--
        if(piece == Piece.KNIGHT):
            if(newrow == oldrow-2 and newcol == oldcol+1):
                return self.checkAndRemove(game, newrow, newcol, color)
            if(newrow == oldrow-1 and newcol == oldcol+2):
                return self.checkAndRemove(game, newrow, newcol, color)
            if(newrow == oldrow+1 and newcol == oldcol+2):
                return self.checkAndRemove(game, newrow, newcol, color)
            if(newrow == oldrow+2 and newcol == oldcol+1):
                return self.checkAndRemove(game, newrow, newcol, color)
            if(newrow == oldrow+2 and newcol == oldcol-1):
                return self.checkAndRemove(game, newrow, newcol, color)
            if(newrow == oldrow+1 and newcol == oldcol-2):
                return self.checkAndRemove(game, newrow, newcol, color)
            if(newrow == oldrow-1 and newcol == oldcol-2):
                return self.checkAndRemove(game, newrow, newcol, color)
            if(newrow == oldrow-2 and newcol == oldcol-1):
                return self.checkAndRemove(game, newrow, newcol, color)
        
        # --Black and White Bishop and Queen--
        if(piece == Piece.BISHOP or piece == Piece.QUEEN):
            if(int(math.fabs(newrow - oldrow)) == int(math.fabs(newcol - oldcol))):
                #[-, +]
                if(newrow < oldrow and newcol > oldcol): 
                    for i in range(1, oldrow-newrow):
                        if(game.boardSquares[oldrow-i][oldcol+i].piece != Piece.EMPTY):
                            return False
                
                    return self.checkAndRemove(game, newrow, newcol, color)
                
                #[+, +]
                elif (newrow > oldrow and newcol > oldcol): 
                    for i in range(1, newrow-oldrow):
                        if(game.boardSquares[oldrow+i][oldcol+i].piece != Piece.EMPTY):
                            return False
                
                    return self.checkAndRemove(game, newrow, newcol, color)
                
                #[+, -]
                elif (newrow > oldrow and newcol < oldcol): 
                    for i in range(1, newrow-oldrow):
                        if(game.boardSquares[oldrow+i][oldcol-i].piece != Piece.EMPTY):
                            return False
                
                    return self.checkAndRemove(game, newrow, newcol, color)
                
                #[-, -]
                elif (newrow < oldrow and newcol < oldcol):
                    for i in range(1, oldrow-newrow):
                        if(game.boardSquares[oldrow-i][oldcol-i].piece != Piece.EMPTY):
                            return False
                
                    return self.checkAndRemove(game, newrow, newcol, color)
        
        # --Black and White King--
        if(piece == Piece.KING):
            if(newrow == oldrow and (newcol == oldcol-1 or newcol == oldcol+1)):
                return self.checkAndRemove(game, newrow, newcol, color)
            elif((newrow == oldrow-1 or newrow == oldrow+1) and newcol == oldcol):
                return self.checkAndRemove(game, newrow, newcol, color)
            elif((newrow == oldrow-1 or newrow == oldrow+1) and (newcol == oldcol-1 or newcol == oldcol+1)):
                return self.checkAndRemove(game, newrow, newcol, color)
            elif((newrow == oldrow-1 and newcol == oldcol-1) or (newrow == oldrow+1 and newcol == oldcol+1)):
                return self.checkAndRemove(game, newrow, newcol, color)

        return False

    def move(self, game, piece, color, oldrow, oldcol, newrow, newcol):
        # if clicked same square
        if(oldrow == newrow and oldcol == newcol):
            print("Same square, not a move.")
            return False

        if (self.validMove(game, piece, color, oldrow, oldcol, newrow, newcol)):
            
            #boardSquares[newrow][newcol].copy(boardSquares[oldrow][oldcol])
            game.previousMove[0] = game.boardSquares[oldrow][oldcol]
            game.previousMove[1] = game.boardSquares[newrow][newcol]

            self.rect.x = (newcol * SQUARE_SIZE) + BOARD_START_X +1
            self.rect.y = (newrow * SQUARE_SIZE) + BOARD_START_X +2
            game.boardSquares[newrow][newcol].x = self.rect.x
            game.boardSquares[newrow][newcol].y = self.rect.y
            
            game.boardSquares[newrow][newcol] = Square(self.rect.x - 1, self.rect.y - 2, game.boardSquares[oldrow][oldcol].piece, game.boardSquares[oldrow][oldcol].pieceColor, game.boardSquares[oldrow][oldcol].sprite)
            game.boardSquares[oldrow][oldcol] = Square((oldcol * SQUARE_SIZE) + BOARD_START_X, (oldrow * SQUARE_SIZE) + BOARD_START_X, Piece.EMPTY, None, None)
            
            if(piece == Piece.PAWN):
                game.boardSquares[newrow][newcol].firstMove = False

            print("Valid Move, New Square:", game.boardSquares[newrow][newcol])
            
            return True
            #self.rect = self.image.get_rect(topleft=(newrow * SQUARE_SIZE, newcol * SQUARE_SIZE))
        else:
            print("Invalid Move")
            return False

    def __str__(self) -> str:
        return super().__str__() + str(self.rect)
    

class game:
    def __init__(self):
        self.boardSquares = [[0 for i in range(COLS)] for j in range(ROWS)]
        self.previousMove = [0 for i in range(2)]

        # Groups sprite together to be displayed
        self.pieces = pygame.sprite.Group()

        # Initializes board with pieces
        # self.initializeBoard(self.pieces)
        self.pieceSelected = False
        self.selectedPos = (-1,-1)

        self.whiteCheck = False
        self.whiteCheckCounter = 0
        self.whiteCheckMate = False

        self.blackCheck = False
        self.blackCheckCounter = 0
        self.blackCheckMate = False

        self.playerTurn = "white"


    def initializeBoard(self):
        for y in range(BOARD_START_X, BOARD_END_X, SQUARE_SIZE):
            row = int((y - BOARD_START_X) / SQUARE_SIZE)
            
            for x in range(BOARD_START_X, BOARD_END_X, SQUARE_SIZE):
                col = int((x - BOARD_START_X) / SQUARE_SIZE)
                
                # puts the correct pieces in the correct places on the boards
                # additions to sprite coords to center sprite
                if(row == 0):
                    if(col == 0 or col == 7):
                        self.boardSquares[row][col] = Square(x, y, Piece.ROOK, "black", PieceSprite((x+1,y+2), ROOK_B_SPRITE))
                    elif(col == 1 or col == 6):
                        self.boardSquares[row][col] = Square(x, y, Piece.KNIGHT, "black", PieceSprite((x+1,y+2), KNIGHT_B_SPRITE))
                    elif(col == 2 or col == 5):
                        self.boardSquares[row][col] = Square(x, y, Piece.BISHOP, "black", PieceSprite((x+1,y+2), BISHOP_B_SPRITE))
                    elif(col == 3):
                        self.boardSquares[row][col] = Square(x, y, Piece.QUEEN, "black", PieceSprite((x+1,y+2), QUEEN_B_SPRITE))
                    elif(col == 4):
                        self.boardSquares[row][col] = Square(x, y, Piece.KING, "black", PieceSprite((x+1,y+2), KING_B_SPRITE))
                elif(row == 1):
                    self.boardSquares[row][col] = Square(x, y, Piece.PAWN, "black", PieceSprite((x+1,y+2), PAWN_B_SPRITE))
                elif(row == 6):
                    self.boardSquares[row][col] = Square(x, y, Piece.PAWN,  "white", PieceSprite((x+1,y+2), PAWN_W_SPRITE))
                elif(row == 7):
                    if(col == 0 or col == 7):
                        self.boardSquares[row][col] = Square(x, y, Piece.ROOK, "white", PieceSprite((x+1,y+2), ROOK_W_SPRITE))
                    elif(col == 1 or col == 6):
                        self.boardSquares[row][col] = Square(x, y, Piece.KNIGHT, "white", PieceSprite((x+1,y+2), KNIGHT_W_SPRITE))
                    elif(col == 2 or col == 5):
                        self.boardSquares[row][col] = Square(x, y, Piece.BISHOP, "white", PieceSprite((x+1,y+2), BISHOP_W_SPRITE))
                    elif(col == 3):
                        self.boardSquares[row][col] = Square(x, y, Piece.QUEEN, "white", PieceSprite((x+1,y+2), QUEEN_W_SPRITE))
                    elif(col == 4):
                        self.boardSquares[row][col] = Square(x, y, Piece.KING, "white", PieceSprite((x+1,y+2), KING_W_SPRITE))
                else:
                    self.boardSquares[row][col] = Square(x, y, Piece.EMPTY)

                if(self.boardSquares[row][col].sprite != None):
                    self.pieces.add(self.boardSquares[row][col].sprite)

    # draws board
    def drawBoard(self):
        white = False
        color = LIGHT_SQUARE_COLOR

        # 96 is where the board starts, because (500 / 2) - (304 / 2) = 98 
        for y in range(BOARD_START_X, BOARD_END_X, SQUARE_SIZE):
            row = int((y - BOARD_START_X) / SQUARE_SIZE)

            for x in range(BOARD_START_X, BOARD_END_X, SQUARE_SIZE):
                col = int((x - BOARD_START_X) / SQUARE_SIZE)

                square = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
                
                # Alternates color
                if(white):
                    color = DARK_SQUARE_COLOR
                    white = False
                else:
                    color = LIGHT_SQUARE_COLOR
                    white = True

                pygame.draw.rect(screen, color, square)
            
            # alternates next row color
            if(white):
                white = False
            else:
                white = True

    # returns king position of certain color
    def findKing(self, color):
        for i in range(ROWS):
            for j in range(COLS):
                if(self.boardSquares[i][j].piece == Piece.KING and self.boardSquares[i][j].pieceColor == color):
                    return (i, j)

    # makes sure iteration is within bounds of board
    def inBoardBounds(self, i,j):
        return (0 <= i < ROWS) and (0 <= j < COLS)

    # checks if that color is in check, subfunction for inCheck()
    def inCheckColor(self, color):
        rowK, colK = self.findKing(color)
        for i in range(ROWS):
            for j in range(COLS):
                if (self.boardSquares[i][j].pieceColor != color):
                    
                    # if the king is diagonally from a pawn, king in check
                    if(self.boardSquares[i][j].piece == Piece.PAWN and self.inBoardBounds(i,j)):
                        if (color == "white"):
                            if((i-1 == rowK and j-1 == colK) or (i-1 == rowK and j+1 == colK)):
                                return 1
                            
                        if (color == "black"):
                            if((i+1 == rowK and j+1 == colK) or (i+1 == rowK and j-1 == colK)):
                                return 2

                    # Queen shares up and down functionality with Rook
                    if(self.boardSquares[i][j].piece == Piece.ROOK or self.boardSquares[i][j].piece == Piece.QUEEN):
                        #[-, x], up
                        king = False
                        for k in range(rowK, i):
                            if (self.boardSquares[k][j].piece != Piece.EMPTY and self.boardSquares[k][j].piece != Piece.KING):
                                king = False
                                break
                            if (self.boardSquares[k][j].piece == Piece.KING and self.boardSquares[k][j].pieceColor == color):
                                king = True

                        if(king):
                            return (1 if color == "black" else 2)

                        #[+, x], down
                        king = False
                        for k in range(i+1, rowK+1):
                            if (self.boardSquares[k][j].piece != Piece.EMPTY and self.boardSquares[k][j].piece != Piece.KING):
                                king = False
                                break
                            if (self.boardSquares[k][j].piece == Piece.KING and self.boardSquares[k][j].pieceColor == color):
                                king = True

                        if(king):
                            return (1 if color == "black" else 2)

                        #[x, -], left
                        king = False
                        for k in range(colK, j):
                            if (self.boardSquares[i][k].piece != Piece.EMPTY and self.boardSquares[i][k].piece != Piece.KING):
                                king = False
                                break
                            if (self.boardSquares[i][k].piece == Piece.KING and self.boardSquares[i][k].pieceColor == color):
                                king = True

                        if(king):
                            return (1 if color == "black" else 2)

                        #[x, +], right   
                        king = False
                        for k in range(j+1, colK+1):
                            if (self.boardSquares[i][k].piece != Piece.EMPTY and self.boardSquares[i][k].piece != Piece.KING):
                                king = False
                                break
                            if (self.boardSquares[i][k].piece == Piece.KING and self.boardSquares[i][k].pieceColor == color):
                                king = True

                        if(king):
                            return (1 if color == "black" else 2)

                    # Bishop and Queen share diagonal functionality
                    if(self.boardSquares[i][j].piece == Piece.BISHOP or self.boardSquares[i][j].piece == Piece.QUEEN):
                        #[-, +], up right
                        king = False
                        for k in range(1, i-rowK+1):
                            if (self.inBoardBounds(i-k, j+k) and self.boardSquares[i-k][j+k].piece != Piece.EMPTY and self.boardSquares[i-k][j+k].piece != Piece.KING):
                                #print("blocking king", rowK, colK, "[",i, j,"] ", k, i-k, j+k)
                                king = False
                                break
                            if (self.inBoardBounds(i-k, j+k) and self.boardSquares[i-k][j+k].piece == Piece.KING and self.boardSquares[i-k][j+k].pieceColor == color):
                                #print("king location", i-k, j+k)
                                king = True

                        #print(king)
                        if(king):
                            return (1 if color == "black" else 2)

                        #[+, +], down right
                        king = False
                        for k in range(1, rowK-i+1):
                            if (self.inBoardBounds(i+k, j+k) and self.boardSquares[i+k][j+k].piece != Piece.EMPTY and self.boardSquares[i+k][j+k].piece != Piece.KING):
                                king = False
                                break
                            if (self.inBoardBounds(i+k, j+k) and self.boardSquares[i+k][j+k].piece == Piece.KING and self.boardSquares[i+k][j+k].pieceColor == color):
                                king = True

                        #print(king)
                        if(king):
                            return (1 if color == "black" else 2)

                        #[+, -], down left
                        king = False
                        for k in range(1, rowK-i+1):
                            if (self.inBoardBounds(i+k, j-k) and self.boardSquares[i+k][j-k].piece != Piece.EMPTY and self.boardSquares[i+k][j-k].piece != Piece.KING):
                                king = False
                                break
                            if (self.inBoardBounds(i+k, j-k) and self.boardSquares[i+k][j-k].piece == Piece.KING and self.boardSquares[i+k][j-k].pieceColor == color):
                                king = True

                        if(king):
                            return (1 if color == "black" else 2)

                        #[-, -], up left   
                        king = False
                        for k in range(1, i-rowK+1):
                            if (self.inBoardBounds(i-k, j-k) and self.boardSquares[i-k][j-k].piece != Piece.EMPTY and self.boardSquares[i-k][j-k].piece != Piece.KING):
                                king = False
                                break
                            if (self.inBoardBounds(i-k, j-k) and self.boardSquares[i-k][j-k].piece == Piece.KING and self.boardSquares[i-k][j-k].pieceColor == color):
                                king = True

                        if(king):
                            return (1 if color == "black" else 2)
                    
                    # if another knight move puts the King in check, king in check
                    if(self.boardSquares[i][j].piece == Piece.KNIGHT):
                        if(rowK == i-2 and colK == j+1):
                            return (1 if color == "black" else 2)
                        if(rowK == i-1 and colK == j+2):
                            return (1 if color == "black" else 2)
                        if(rowK == i+1 and colK == j+2):
                            return (1 if color == "black" else 2)
                        if(rowK == i+2 and colK == j+1):
                            return (1 if color == "black" else 2)
                        if(rowK == i+2 and colK == j-1):
                            return (1 if color == "black" else 2)
                        if(rowK == i+1 and colK == j-2):
                            return (1 if color == "black" else 2)
                        if(rowK == i-1 and colK == j-2):
                            return (1 if color == "black" else 2)
                        if(rowK == i-2 and colK == j-1):
                            return (1 if color == "black" else 2)

                    if(self.boardSquares[i][j].piece == Piece.KING):
                        if(rowK == i and (colK == j-1 or colK == j+1)):
                            return (1 if color == "black" else 2)
                        elif((rowK == i-1 or rowK == i+1) and colK == j):
                            return (1 if color == "black" else 2)
                        elif((rowK == i-1 or rowK == i+1) and (colK == j-1 or colK == j+1)):
                            return (1 if color == "black" else 2)
                        elif((rowK == i-1 and colK == j-1) or (rowK == i+1 and colK == j+1)):
                            return (1 if color == "black" else 2)

        return 0

    # returns 0 for no check, 1 for black in check, 2 for white in check
    def inCheck(self):
        
        if(self.inCheckColor("black") == 1):
            return 1
        
        if(self.inCheckColor("white") == 2):
            return 2

        return 0

    """ # Groups sprite together to be displayed
    pieces = pygame.sprite.Group()

    # Initializes board with pieces
    initializeBoard(pieces)
    pieceSelected = False
    selectedPos = (-1,-1)

    whiteCheck = False
    whiteCheckCounter = 0
    whiteCheckMate = False

    blackCheck = False
    blackCheckCounter = 0
    blackCheckMate = False

    playerTurn = "white"
    """
    # resets all variables and sprites, new game
    def newGame(self):
        for p in self.pieces:
            p.kill()

        self.initializeBoard()  

        self.pieceSelected = False
        self.selectedPos = (-1,-1)

        self.whiteCheck = False
        self.whiteCheckCounter = 0
        self.whiteCheckMate = False

        self.blackCheck = False
        self.blackCheckCounter = 0
        self.blackCheckMate = False


        self.playerTurn = "white"

        print("\n======New Game=====\n")

    # un-does last move
    def undoMove(self,oldrow, oldcol, newrow, newcol):
        # removes sprite from new location
        self.pieces.remove(self.boardSquares[newrow][newcol].sprite)

        # restores previous data of squares
        self.boardSquares[oldrow][oldcol] = self.previousMove[0]
        self.boardSquares[newrow][newcol] = self.previousMove[1]
        
        # sprite adjustments messes with selection square, so have to readjust coords
        self.boardSquares[newrow][newcol].x -= 1
        self.boardSquares[newrow][newcol].y -= 2 
        
        # re-calculates location of old sprite
        self.boardSquares[oldrow][oldcol].sprite.rect.x = (oldcol * SQUARE_SIZE) + BOARD_START_X+1
        self.boardSquares[oldrow][oldcol].sprite.rect.y = (oldrow * SQUARE_SIZE) + BOARD_START_X+2
        
        # re-adds old sprite
        self.pieces.add(self.boardSquares[oldrow][oldcol].sprite)
        
        # if previous move had removed a piece from the new location, restores that sprite as well
        if(self.previousMove[1].sprite != None):
            self.boardSquares[newrow][newcol].sprite.rect.x = (newcol * SQUARE_SIZE) + BOARD_START_X+1
            self.boardSquares[newrow][newcol].sprite.rect.y = (newrow * SQUARE_SIZE) + BOARD_START_X+2
            self.pieces.add(self.boardSquares[newrow][newcol].sprite)


chess = game()
chess.newGame()

running = True
while running:
    # "X"-ed window out
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # n for new game
        elif (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_n):
                chess.newGame()

        # selected a square
        elif (event.type == pygame.MOUSEBUTTONUP and (not chess.pieceSelected)):
            pos = pygame.mouse.get_pos()

            if(BOARD_START_X <= pos[0] <= BOARD_END_X and BOARD_START_X <= pos[1] <= BOARD_END_X ):
                chess.selectedPos = (int((pos[1] - BOARD_START_X) / SQUARE_SIZE), int((pos[0] - BOARD_START_X) / SQUARE_SIZE))
                print("\nSelected Piece:", chess.boardSquares[chess.selectedPos[0]][chess.selectedPos[1]].piece)

                if(chess.boardSquares[chess.selectedPos[0]][chess.selectedPos[1]].piece != Piece.EMPTY):
                    chess.pieceSelected = True
                else:
                    chess.pieceSelected = False
                    chess.selectedPos = (-1,-1) 

        # selected a second square
        elif (event.type == pygame.MOUSEBUTTONUP and chess.pieceSelected):
            pos = pygame.mouse.get_pos()
            x, y = pos
            oldrow = chess.selectedPos[0]
            oldcol = chess.selectedPos[1]
            newrow = int((y - BOARD_START_X) / SQUARE_SIZE)
            newcol = int((x - BOARD_START_X) / SQUARE_SIZE)

            # checks if the king is in check before move
            if(chess.inCheck() == 1):
                print("black king in check")
                chess.blackCheck = True
            elif (chess.inCheck() == 2):
                print("white king in check")
                chess.whiteCheck = True
            else:
                print("kings are safe before")
                chess.blackCheck = False
                chess.whiteCheck = False

            # makes sure coords are in bounds and moves piece
            if(BOARD_START_X <= x <= BOARD_END_X and BOARD_START_X <= y <=BOARD_END_X):
                print("[",oldrow, ", ", oldcol, "]->[", newrow, ", ", newcol, "]", chess.boardSquares[oldrow][oldcol].piece)
                
                # if you click the same square, move invalid
                if(newrow == oldrow and newcol == oldcol):
                    print("Same square, please select a valid move.")
                    chess.pieceSelected = False
                    chess.selectedPos = (-1,-1) 
                    break

                # makes sure the correct color goes 
                if(chess.boardSquares[oldrow][oldcol].pieceColor == chess.playerTurn):
                    validMove = chess.boardSquares[oldrow][oldcol].sprite.move(chess, chess.boardSquares[oldrow][oldcol].piece, chess.boardSquares[oldrow][oldcol].pieceColor, oldrow, oldcol, newrow, newcol)

                    # if valid, switches turn
                    if(validMove):
                        chess.playerTurn = "black" if chess.playerTurn == "white" else "white"
                    
                    # if black is still in check after it moves, invalid
                    if(chess.inCheck() == 1 and chess.blackCheck):
                        print("Invalid move, black king still in check")
                        chess.undoMove(oldrow, oldcol, newrow, newcol)

                        chess.playerTurn = "black"

                    # if it switched over to white and black is in check, black put itself into check, invalid
                    elif(chess.inCheck() == 1 and chess.playerTurn == "white"):
                        print("Invalid move, black can't put itself into check")
                        chess.undoMove(oldrow, oldcol, newrow, newcol)

                        chess.playerTurn = "black"

                    # if white is still in check after it moves, invalid
                    elif(chess.inCheck() == 2 and chess.whiteCheck):
                        print("Invalid move, white king still in check")
                        chess.undoMove(oldrow, oldcol, newrow, newcol)

                        chess.playerTurn = "white"

                    # if it switched over to black and white is in check, white put itself into check, invalid
                    elif(chess.inCheck() == 2 and chess.playerTurn == "black"):
                        print("Invalid move, white can't put itself into check")
                        chess.undoMove(oldrow, oldcol, newrow, newcol)

                        chess.playerTurn = "white"

                else:
                    print("It is", chess.playerTurn, "turn, select a", chess.playerTurn, "piece.")
            else:
                print("out of bounds")

            # checks if the king is in check after move
            if(chess.inCheck() == 1 and chess.blackCheck):
                print("Invalid move, black king still in check")
            elif(chess.inCheck() == 1 and not chess.blackCheck):
                print("black king in check")
                chess.blackCheck = True
            elif (chess.inCheck() == 2 and chess.whiteCheck):
                print("Invalid move, white king still in check")
            elif(chess.inCheck() == 2 and not chess.whiteCheck):
                print("white king in check")
                chess.blackCheck = True
            else:
                print("kings are safe after")
                chess.blackCheck = False
                chess.whiteCheck = False


            #reset selected piece
            chess.pieceSelected = False
            chess.selectedPos = (-1,-1)


    # Fill the background with white
    screen.fill(BACKGROUND_COLOR)

    # Creates chess board border and blit it to the center of the screen
    surf = pygame.Surface((BOARD_SIZE + 2, BOARD_SIZE + 2))
    surf.fill((DARK_SQUARE_COLOR))
    screen.blit(surf, (BOARD_START_X - 1, BOARD_START_X -1))

    # draws board
    chess.drawBoard()

    # if piece is selected, highlights it with a color
    if(chess.pieceSelected):
        pygame.draw.rect(screen, SELECTED_COLOR, pygame.Rect(chess.boardSquares[chess.selectedPos[0]][chess.selectedPos[1]].x, chess.boardSquares[chess.selectedPos[0]][chess.selectedPos[1]].y, SQUARE_SIZE, SQUARE_SIZE) )
               
    # draws pieces to screen
    chess.pieces.draw(screen)

    # updates the screen every frame
    pygame.display.flip()


pygame.quit()
