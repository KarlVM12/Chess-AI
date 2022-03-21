import os.path
import math
import pygame
import enum
from Piece import Piece as Piece
import alphaBetaPruning

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
        self.attackingSquares = []

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

            #print("Valid Move, New Square:", game.boardSquares[newrow][newcol])
            
            return True
            #self.rect = self.image.get_rect(topleft=(newrow * SQUARE_SIZE, newcol * SQUARE_SIZE))
        else:
            #print("Invalid Move")
            game.previousMove[0] = game.boardSquares[oldrow][oldcol]
            game.previousMove[1] = game.boardSquares[newrow][newcol]
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

        self.BLACK_WIN = -1
        self.STALEMATE = 0
        self.WHITE_WIN = 1

        self.whiteScore = 0
        self.blackScore = 0
        

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
    def findPiece(self, color, piece):
        for i in range(ROWS):
            for j in range(COLS):
                if(self.boardSquares[i][j].piece == piece and self.boardSquares[i][j].pieceColor == color):
                    return (i, j)

        return (-1, -1)

    # returns list of the possible moves of a piece
    def piecePossibleMoves(self, color, piece, row, col):
        possibleMoves = []
        
        for i in range(ROWS):
            for j in range(COLS):
                if(self.boardSquares[row][col].sprite.move(self, piece, color, row, col, i, j)):
                    possibleMoves.append([i,j])
                    self.undoMove(row, col, i, j)

        return possibleMoves

    # makes sure iteration is within bounds of board
    def inBoardBounds(self, i,j):
        return (0 <= i < ROWS) and (0 <= j < COLS)

    # checks if that color of a certain piece is under attack (or check), subfunction for inCheck()
    def inAttackColor(self, color, piece, rowIn = -1, colIn = -1):
        if(piece != Piece.EMPTY):
            rowK, colK = self.findPiece(color, piece)

        if(self.inBoardBounds(rowIn, colIn)):
            rowK = rowIn
            colK = colIn
        
        for i in range(ROWS):
            for j in range(COLS):
                if (self.boardSquares[i][j].pieceColor != color):
                    
                    # if the king is diagonally from a pawn, king in check
                    if(self.boardSquares[i][j].piece == Piece.PAWN and self.inBoardBounds(i,j)):
                        if (color == "black"):
                            if((i-1 == rowK and j-1 == colK) or (i-1 == rowK and j+1 == colK)):
                                return True, i, j
                            
                        if (color == "white"):
                            if((i+1 == rowK and j+1 == colK) or (i+1 == rowK and j-1 == colK)):
                                return True, i, j
                        
                        # for checking for checkmate of empty squares
                        if(piece == Piece.EMPTY):
                            # because a double first move can block a check
                            if(color == "black" and self.boardSquares[i][j].firstMove):
                                if(i-2 == rowK and j == colK):
                                    return True, i, j
                            if(color == "white" and self.boardSquares[i][j].firstMove):
                                if(i+2 == rowK and j == colK):
                                    return True, i, j
                    # Queen shares up and down functionality with Rook
                    if(self.boardSquares[i][j].piece == Piece.ROOK or self.boardSquares[i][j].piece == Piece.QUEEN):
                        #[-, x], up
                        king = False
                        for k in range(rowK, i):
                            if (self.boardSquares[k][j].piece != Piece.EMPTY and self.boardSquares[k][j].piece != piece):
                                king = False
                                break
                            if (self.boardSquares[k][j].piece == piece and self.boardSquares[k][j].pieceColor == color):
                                king = True

                        if(king):
                            return True, i, j

                        #[+, x], down
                        king = False
                        for k in range(i+1, rowK+1):
                            if (self.boardSquares[k][j].piece != Piece.EMPTY and self.boardSquares[k][j].piece != piece):
                                king = False
                                break
                            if (self.boardSquares[k][j].piece == piece and self.boardSquares[k][j].pieceColor == color):
                                king = True

                        if(king):
                            return True, i, j

                        #[x, -], left
                        king = False
                        for k in range(colK, j):
                            if (self.boardSquares[i][k].piece != Piece.EMPTY and self.boardSquares[i][k].piece != piece):
                                king = False
                                break
                            if (self.boardSquares[i][k].piece == piece and self.boardSquares[i][k].pieceColor == color):
                                king = True

                        if(king):
                            return True, i, j

                        #[x, +], right   
                        king = False
                        for k in range(j+1, colK+1):
                            if (self.boardSquares[i][k].piece != Piece.EMPTY and self.boardSquares[i][k].piece != piece):
                                king = False
                                break
                            if (self.boardSquares[i][k].piece == piece and self.boardSquares[i][k].pieceColor == color):
                                king = True

                        if(king):
                            return True, i, j

                    # Bishop and Queen share diagonal functionality
                    if(self.boardSquares[i][j].piece == Piece.BISHOP or self.boardSquares[i][j].piece == Piece.QUEEN):
                        #[-, +], up right
                        king = False
                        for k in range(1, i-rowK+1):
                            if (self.inBoardBounds(i-k, j+k) and self.boardSquares[i-k][j+k].piece != Piece.EMPTY and self.boardSquares[i-k][j+k].piece != piece):
                                #print("blocking king", rowK, colK, "[",i, j,"] ", k, i-k, j+k)
                                king = False
                                break
                            if (self.inBoardBounds(i-k, j+k) and self.boardSquares[i-k][j+k].piece == piece and self.boardSquares[i-k][j+k].pieceColor == color):
                                #print("king location", i-k, j+k)
                                king = True

                        #print(king)
                        if(king):
                            return True, i, j

                        #[+, +], down right
                        king = False
                        for k in range(1, rowK-i+1):
                            if (self.inBoardBounds(i+k, j+k) and self.boardSquares[i+k][j+k].piece != Piece.EMPTY and self.boardSquares[i+k][j+k].piece != piece):
                                king = False
                                break
                            if (self.inBoardBounds(i+k, j+k) and self.boardSquares[i+k][j+k].piece == piece and self.boardSquares[i+k][j+k].pieceColor == color):
                                king = True

                        #print(king)
                        if(king):
                            return True, i, j

                        #[+, -], down left
                        king = False
                        for k in range(1, rowK-i+1):
                            if (self.inBoardBounds(i+k, j-k) and self.boardSquares[i+k][j-k].piece != Piece.EMPTY and self.boardSquares[i+k][j-k].piece != piece):
                                king = False
                                break
                            if (self.inBoardBounds(i+k, j-k) and self.boardSquares[i+k][j-k].piece == piece and self.boardSquares[i+k][j-k].pieceColor == color):
                                king = True

                        if(king):
                            return True, i, j

                        #[-, -], up left   
                        king = False
                        for k in range(1, i-rowK+1):
                            if (self.inBoardBounds(i-k, j-k) and self.boardSquares[i-k][j-k].piece != Piece.EMPTY and self.boardSquares[i-k][j-k].piece != piece):
                                king = False
                                break
                            if (self.inBoardBounds(i-k, j-k) and self.boardSquares[i-k][j-k].piece == piece and self.boardSquares[i-k][j-k].pieceColor == color):
                                king = True

                        if(king):
                            return True, i, j
                    
                    # if another knight move puts the King in check, king in check
                    if(self.boardSquares[i][j].piece == Piece.KNIGHT):
                        if(rowK == i-2 and colK == j+1):
                            return True, i, j
                        if(rowK == i-1 and colK == j+2):
                            return True, i, j
                        if(rowK == i+1 and colK == j+2):
                            return True, i, j
                        if(rowK == i+2 and colK == j+1):
                            return True, i, j
                        if(rowK == i+2 and colK == j-1):
                            return True, i, j
                        if(rowK == i+1 and colK == j-2):
                            return True, i, j
                        if(rowK == i-1 and colK == j-2):
                            return True, i, j
                        if(rowK == i-2 and colK == j-1):
                            return True, i, j

                    if(self.boardSquares[i][j].piece == Piece.KING):
                        if(rowK == i and (colK == j-1 or colK == j+1)):
                            return True, i, j
                        elif((rowK == i-1 or rowK == i+1) and colK == j):
                            return True, i, j
                        elif((rowK == i-1 or rowK == i+1) and (colK == j-1 or colK == j+1)):
                            return True, i, j
                        elif((rowK == i-1 and colK == j-1) or (rowK == i+1 and colK == j+1)):
                            return True, i, j

        return False, -1, -1

    # returns 0 for no check, 1 for black in check, 2 for white in check
    def inCheck(self):
        
        if(self.inAttackColor("black", Piece.KING)[0]):
            return 1
        
        if(self.inAttackColor("white", Piece.KING)[0]):
            return 2

        return 0

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

    def checkStalemate(self, color):
        checkCounter = 0
        rowK, colK = self.findPiece(color, Piece.KING)

        # [+, x]
        if self.inBoardBounds(rowK + 1, colK) and (self.boardSquares[rowK][colK].sprite.move(self, Piece.KING, color, rowK, colK, rowK + 1, colK)):
            if(self.inCheck()):
                checkCounter += 1

            self.undoMove( rowK, colK, rowK + 1, colK)

        # [-, x]
        if (self.inBoardBounds(rowK -1, colK) and self.boardSquares[rowK][colK].sprite.move(self, Piece.KING, color, rowK, colK, rowK - 1, colK)):
            if(self.inCheck()):
                checkCounter += 1
                
            self.undoMove( rowK, colK, rowK - 1, colK)

        # [x, +]
        if (self.inBoardBounds(rowK, colK+1) and self.boardSquares[rowK][colK].sprite.move(self, Piece.KING, color, rowK, colK, rowK, colK + 1)):
            if(self.inCheck()):
                checkCounter += 1
                
            self.undoMove( rowK, colK, rowK, colK + 1)

        # [x, -]
        if (self.inBoardBounds(rowK, colK-1) and self.boardSquares[rowK][colK].sprite.move(self, Piece.KING, color, rowK, colK, rowK, colK - 1)):
            if(self.inCheck()):
                checkCounter += 1
                
            self.undoMove( rowK, colK, rowK, colK - 1)

        # [-, +]
        if (self.inBoardBounds(rowK-1, colK+1) and self.boardSquares[rowK][colK].sprite.move(self, Piece.KING, color, rowK, colK, rowK - 1, colK + 1)):
            if(self.inCheck()):
                checkCounter += 1
                
            self.undoMove( rowK, colK, rowK - 1, colK + 1)

        # [+, +]
        if (self.inBoardBounds(rowK+1, colK+1) and self.boardSquares[rowK][colK].sprite.move(self, Piece.KING, color, rowK, colK, rowK + 1, colK + 1)):
            if(self.inCheck()):
                checkCounter += 1
                
            self.undoMove( rowK, colK, rowK + 1, colK + 1)

        # [+, -]
        if (self.inBoardBounds(rowK+1, colK-1) and self.boardSquares[rowK][colK].sprite.move(self, Piece.KING, color, rowK, colK, rowK + 1, colK - 1)):
            if(self.inCheck()):
                checkCounter += 1
                
            self.undoMove( rowK, colK, rowK + 1, colK - 1)

        # [-, -]
        if (self.inBoardBounds(rowK-1, colK-1) and self.boardSquares[rowK][colK].sprite.move(self, Piece.KING, color, rowK, colK, rowK - 1, colK - 1)):
            if(self.inCheck()):
                checkCounter += 1
                
            self.undoMove( rowK, colK, rowK - 1, colK - 1)

        if(checkCounter == 8):
            return True

        return False

    def invalidKingMoves(self, color):
        invalidCounter = 0
        rowK, colK = self.findPiece(color, Piece.KING)

        # [+, x]
        if (self.inBoardBounds(rowK + 1, colK)):
            valid = self.boardSquares[rowK][colK].sprite.move(self, Piece.KING, color, rowK, colK, rowK + 1, colK)
            if(self.inCheck() or not valid):
                invalidCounter += 1

            if(valid):
                self.undoMove( rowK, colK, rowK + 1, colK)
        elif (not self.inBoardBounds(rowK + 1, colK)):
            invalidCounter += 1

        # [-, x]
        if (self.inBoardBounds(rowK-1, colK)):
            valid = self.boardSquares[rowK][colK].sprite.move(self, Piece.KING, color, rowK, colK, rowK - 1, colK)
            if(self.inCheck() or not valid):
                invalidCounter += 1

            if(valid):
                self.undoMove( rowK, colK, rowK - 1, colK)
        elif (not self.inBoardBounds(rowK - 1, colK)):
            invalidCounter += 1

        # [x, +]
        if (self.inBoardBounds(rowK, colK+1)):
            valid = self.boardSquares[rowK][colK].sprite.move(self, Piece.KING, color, rowK, colK, rowK, colK + 1)
            if(self.inCheck() or not valid):
                invalidCounter += 1
                
            if(valid):    
                self.undoMove( rowK, colK, rowK, colK + 1)
        elif (not self.inBoardBounds(rowK, colK + 1)):
            invalidCounter += 1

        # [x, -]
        if (self.inBoardBounds(rowK, colK-1)):
            valid = self.boardSquares[rowK][colK].sprite.move(self, Piece.KING, color, rowK, colK, rowK, colK - 1)
            if(self.inCheck() or not valid):
                invalidCounter += 1
                
            if(valid):   
                self.undoMove( rowK, colK, rowK, colK - 1)
        elif (not self.inBoardBounds(rowK, colK - 1)):
            invalidCounter += 1

        # [-, +]
        if (self.inBoardBounds(rowK-1, colK+1)):
            valid = self.boardSquares[rowK][colK].sprite.move(self, Piece.KING, color, rowK, colK, rowK - 1, colK + 1)
            if(self.inCheck() or not valid):
                invalidCounter += 1
            
            if(valid):
                self.undoMove( rowK, colK, rowK - 1, colK + 1)
        elif (not self.inBoardBounds(rowK - 1, colK + 1)):
            invalidCounter += 1

        # [+, +]
        if (self.inBoardBounds(rowK+1, colK+1)):
            valid = self.boardSquares[rowK][colK].sprite.move(self, Piece.KING, color, rowK, colK, rowK + 1, colK + 1)
            if(self.inCheck() or not valid):
                invalidCounter += 1
            
            if(valid):    
                self.undoMove( rowK, colK, rowK + 1, colK + 1)
        elif (not self.inBoardBounds(rowK + 1, colK + 1)):
            invalidCounter += 1

        # [+, -]
        if (self.inBoardBounds(rowK+1, colK-1)):
            valid = self.boardSquares[rowK][colK].sprite.move(self, Piece.KING, color, rowK, colK, rowK + 1, colK - 1)
            if(self.inCheck() or not valid):
                invalidCounter += 1
            
            if(valid):    
                self.undoMove( rowK, colK, rowK + 1, colK - 1)
        elif (not self.inBoardBounds(rowK + 1, colK - 1)):
            invalidCounter += 1

        # [-, -]
        if (self.inBoardBounds(rowK-1, colK-1)):
            valid = self.boardSquares[rowK][colK].sprite.move(self, Piece.KING, color, rowK, colK, rowK - 1, colK - 1)
            if(self.inCheck() or not valid):
                invalidCounter += 1
                
            if(valid):
                self.undoMove( rowK, colK, rowK - 1, colK - 1)
        elif (not self.inBoardBounds(rowK - 1, colK - 1)):
            invalidCounter += 1

        if(invalidCounter == 8):
            return True

        return False

    def checkCheckmate(self, color):

        # if the king can't:
        #   1) Move the king so that it's no longer under attack.
        #   2) Capture the attacking piece.
        #   3) Block the attack by interposing a piece between the king and the attacker.

        checkmateCounter = 0
        
        #=======================================================#
        # 1) Move the king so that it's no longer under attack.
        #=======================================================#

        if (self.invalidKingMoves(color)):
            checkmateCounter += 1
            print("can't move king")
        else:
            return False

        #=================================#
        # 2) Capture the attacking piece.
        #=================================#

        # gets piece that is attacking king
        attacker = self.inAttackColor(color, Piece.KING)
        rowA, colA = attacker[1], attacker[2]

        # checks if that piece has the possibility of being captured
        attackingAttacker = self.inAttackColor(self.boardSquares[rowA][colA].pieceColor, self.boardSquares[rowA][colA].piece, rowA, colA)
        attackingAttacked, rowAA, colAA = attackingAttacker

        # if the attacker is not able to be captured or the only thing able to capture it is the King in check, which wouldn't be possible becuase we determined before there were no valid moves
        if(not attackingAttacked or (self.inBoardBounds(rowAA, colAA) and self.boardSquares[rowAA][colAA].pieceColor == color and self.boardSquares[rowAA][colAA].piece == Piece.KING)):
            checkmateCounter += 1
            print("attacker has none of its own attackers")
        else:
            return False


        #==============================================================================#
        # 3) Block the attack by interposing a piece between the king and the attacker.
        #==============================================================================#

        # if attacker is within one square of king, easy to check that nothing can block it
        # also, if pawn or knight, nothing can block their attacks since there is no empty space
        if (self.boardSquares[rowA][colA].piece == Piece.PAWN or self.boardSquares[rowA][colA].piece == Piece.KNIGHT):
            checkmateCounter += 1
        elif((self.inBoardBounds(rowA, colA-1) and self.boardSquares[rowA][colA-1].piece == Piece.KING and self.boardSquares[rowA][colA-1].pieceColor == color) or (self.inBoardBounds(rowA, colA+1) and self.boardSquares[rowA][colA+1].piece == Piece.KING and self.boardSquares[rowA][colA+1].pieceColor == color)):
            checkmateCounter += 1  
        elif((self.inBoardBounds(rowA-1, colA) and self.boardSquares[rowA-1][colA].piece == Piece.KING and self.boardSquares[rowA-1][colA].pieceColor == color) or (self.inBoardBounds(rowA+1, colA) and self.boardSquares[rowA+1][colA].piece == Piece.KING and self.boardSquares[rowA+1][colA].pieceColor == color)):
            checkmateCounter += 1 
        elif((self.inBoardBounds(rowA-1, colA-1) and self.boardSquares[rowA-1][colA-1].piece == Piece.KING and self.boardSquares[rowA-1][colA-1].pieceColor == color) or (self.inBoardBounds(rowA+1, colA+1) and self.boardSquares[rowA+1][colA+1].piece == Piece.KING and self.boardSquares[rowA+1][colA+1].pieceColor == color)):
            checkmateCounter += 1 
        elif((self.inBoardBounds(rowA-1, colA+1) and self.boardSquares[rowA-1][colA+1].piece == Piece.KING and self.boardSquares[rowA-1][colA+1].pieceColor == color) or (self.inBoardBounds(rowA+1, colA-1) and self.boardSquares[rowA+1][colA-1].piece == Piece.KING and self.boardSquares[rowA+1][colA-1].pieceColor == color)):
            checkmateCounter += 1              

        # just have to check if anything can block the path of the attacker
        # loop through path from attacker to king, stores the coords in an array, check if they can be blocked
        rowK, colK = self.findPiece(color, Piece.KING)
        emptySpaces = []
        oppositeColor = "white" if (color == "black") else "white"
                
        # attacker is bishop/queen
        if(self.boardSquares[rowA][colA].piece == Piece.BISHOP or self.boardSquares[rowA][colA].piece == Piece.QUEEN):
            # [-, +] up right
            if(rowA > rowK and colA < colK):
                for k in range(1, rowA-rowK):
                    if(self.boardSquares[rowA-k][colA+k].piece == Piece.EMPTY):
                        emptySpaces.append([rowA-k, colA+k])
            
            # [+, +] down right
            elif(rowA < rowK and colA < colK):
                for k in range(1, rowK-rowA):
                    if(self.boardSquares[rowA+k][colA+k].piece == Piece.EMPTY):
                        emptySpaces.append([rowA+k, colA+k])

            # [+, -] down left
            elif(rowA < rowK and colA > colK):
                for k in range(1, rowK-rowA):
                    if(self.boardSquares[rowA+k][colA-k].piece == Piece.EMPTY):
                        emptySpaces.append([rowA+k, colA-k])

            # [-, -] up left
            elif(rowA > rowK and colA > colK):
                for k in range(1, rowA-rowK):
                    if(self.boardSquares[rowA-k][colA-k].piece == Piece.EMPTY):
                        emptySpaces.append([rowA-k, colA-k])

            # gets the empty space between the king in check and the attacker (Bishop or Queen in this case)
            # then its acts as if those empty squares are pieces of the opposite color that can be threathened by the same color king's pieces
            # if even one of the empty squares are threathened, returns false and can't be checkmate
            for rc in emptySpaces:
                blocker = self.inAttackColor(oppositeColor, Piece.EMPTY, rc[0], rc[1])
                if(blocker and blocker[1] != rowK and blocker[2] != colK):
                    print("blocker at:", rc[0], rc[1], " ", emptySpaces)
                    return False
            
            checkmateCounter += 1
        
        # attacker is rook/queen
        emptySpaces = []
        if(self.boardSquares[rowA][colA].piece == Piece.ROOK or self.boardSquares[rowA][colA].piece == Piece.QUEEN):
            # [-, x] up
            if(rowA > rowK and colA == colK):
                for k in range(rowK+1, rowA):
                    if(self.boardSquares[k][colA].piece == Piece.EMPTY):
                        emptySpaces.append([k, colA])

            # [+, x] down
            if(rowA < rowK and colA == colK):
                for k in range(rowA+1, rowK):
                    if(self.boardSquares[k][colA].piece == Piece.EMPTY):
                        emptySpaces.append([k, colA])
            
            # [x, +] right
            if(rowA == rowK and colA < colK):
                for k in range(colA+1, colK):
                    if(self.boardSquares[rowA][k].piece == Piece.EMPTY):
                        emptySpaces.append([rowA, k])
            
            # [x, -] left
            if(rowA == rowK and colA > colK):
                for k in range(colK+1, colA):
                    if(self.boardSquares[rowA][k].piece == Piece.EMPTY):
                        emptySpaces.append([rowA, k])

            # search thro empty spaces for possible blockers
            for rc in emptySpaces:
                blocker = self.inAttackColor(oppositeColor, Piece.EMPTY, rc[0], rc[1])
                if(blocker and blocker[1] != rowK and blocker[2] != colK):
                    print("blocker at:", rc[0], rc[1], " ", emptySpaces)
                    return False
            
            checkmateCounter += 1

        if(checkmateCounter >= 3):
            return True    

        return False

    def win(self, color):

        if(color == "white"):
            self.whiteScore += 1
        else:
            self.blackScore += 1

        print("\n=====Game Over=====")
        print("White: ", self.whiteScore)
        print("Black: ", self.blackScore)

    def isTerminal(self):
        
        # Black Stalemate 
        if(not self.blackCheck):
            if(self.checkStalemate("black")):
                print("Black king in Stalemate")
                return True

        # White Stalemate
        if(not self.whiteCheck):
            if(self.checkStalemate("white")):
                print("White king in Stalemate")
                return True
       
        
        # Black Checkmate
        if(self.blackCheck):
            if(self.checkCheckmate("black")):
                print("Black king in Checkmate, White wins.")
                self.win("white")

                return True
                
        # White Checkmate
        if(self.whiteCheck):
            if(self.checkCheckmate("white")):
                print("White king in Checkmate, Black wins.")
                self.win("black")

                return True

        return False
        
    def utility(self, color):
    
        if(color == "black"):
            if(self.checkCheckmate("white")):
                return (1, None, None, None, None)
            elif(self.checkCheckmate("black")):
                return (-1, None, None, None, None)
            else:
                return (0, None, None, None, None)
        else:
            if(self.checkCheckmate("black")):
                return (-1, None, None, None, None)
            elif(self.checkCheckmate("white")):
                return (1, None, None, None, None)
            else:
                return (0, None, None, None, None)


chess = game()
chess.newGame()

# game is running and it is not a terminal state
running = True
while running and not chess.isTerminal():
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
                    #print(chess.piecePossibleMoves(chess.boardSquares[chess.selectedPos[0]][chess.selectedPos[1]].pieceColor, chess.boardSquares[chess.selectedPos[0]][chess.selectedPos[1]].piece, chess.selectedPos[0], chess.selectedPos[1]))
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
                        print("Valid Move, New Square:", chess.boardSquares[newrow][newcol])
                        chess.playerTurn = "black" if chess.playerTurn == "white" else "white"
                    else:
                        print("Invalid Move")
                    
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
                chess.whiteCheck = True
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
