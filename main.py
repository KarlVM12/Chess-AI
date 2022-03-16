import os.path
import math
import pygame
import enum
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

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Chess AI')
boardSquares = [[0 for i in range(COLS)] for j in range(ROWS)]

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
    def checkAndRemove(self, newrow, newcol, color):
        # if rows are empty but destination has an opoosite color piece, removes the piece and moves
        if(boardSquares[newrow][newcol].piece != Piece.EMPTY):
            if(boardSquares[newrow][newcol].pieceColor == color):
                return False

            pieces.remove(boardSquares[newrow][newcol].sprite)
            return True

        # if destination is just empty, valid move
        return True

    def validMove(self, piece, color, oldrow, oldcol, newrow, newcol):
        
        # --Black and white Pawns--
        if(piece == Piece.PAWN):
            if(color == "black"):
                
                # first move where it can go 2 squares
                if(boardSquares[oldrow][oldcol].firstMove and newrow == oldrow+2 and newcol == oldcol and boardSquares[oldrow+1][newcol].piece == Piece.EMPTY and boardSquares[newrow][newcol].piece == Piece.EMPTY):
                    boardSquares[oldrow][oldcol].firstMove = False
                    return True
                # just moving forward    
                if(newrow == oldrow+1 and oldcol == newcol and boardSquares[newrow][newcol].piece == Piece.EMPTY):
                    return True
                # moving diagonal to capture a piece
                if(newrow == oldrow+1 and (newcol == oldcol-1 or newcol == oldcol+1) and boardSquares[newrow][newcol].piece != Piece.EMPTY and boardSquares[newrow][newcol].pieceColor != "black"):
                    pieces.remove(boardSquares[newrow][newcol].sprite)
                    return True
                
            if(color == "white"):
                # first move where it can go 2 squares
                if(boardSquares[oldrow][oldcol].firstMove and newrow == oldrow-2 and newcol == oldcol and boardSquares[oldrow-1][newcol].piece == Piece.EMPTY and boardSquares[newrow][newcol].piece == Piece.EMPTY):
                    boardSquares[oldrow][oldcol].firstMove = False
                    return True
                # just moving forward
                if(newrow == oldrow-1 and oldcol == newcol and boardSquares[newrow][newcol].piece == Piece.EMPTY):
                    return True
                # moving diagonal to capture a piece
                if(newrow == oldrow-1 and (newcol == oldcol-1 or newcol == oldcol+1 )and boardSquares[newrow][newcol].piece != Piece.EMPTY and boardSquares[newrow][newcol].pieceColor != "white"):
                    pieces.remove(boardSquares[newrow][newcol].sprite)
                    return True

        # --Black and White Rook and Queen--
        if(piece == Piece.ROOK or piece == Piece.QUEEN):
            if((newrow != oldrow and newcol == oldcol)):
                # checks if up and down columns are empty
                if(newrow >= oldrow):
                    for i in range(oldrow+1, newrow):
                        if (boardSquares[i][newcol].piece != Piece.EMPTY):
                            return False
                elif (newrow < oldrow):
                    for i in range(newrow+1, oldrow):
                        print(i, newcol)
                        if (boardSquares[i][newcol].piece != Piece.EMPTY):
                            return False

                # if destination is not empty but has an opposite color piece, removes that piece
                if(boardSquares[newrow][newcol].piece != Piece.EMPTY):
                    if(boardSquares[newrow][newcol].pieceColor == color):
                        return False

                    pieces.remove(boardSquares[newrow][newcol].sprite)
                    return True

                # if destination is just empty, valid move
                return True

            if(newrow == oldrow and newcol != oldcol):
                # checks if rows between move is all empty
                if(newcol >= oldcol):
                    for i in range(oldcol+1, newcol):
                        if (boardSquares[newrow][i].piece != Piece.EMPTY):
                            return False
                elif (newcol < oldcol):
                    for i in range(newcol+1, oldcol):
                        if (boardSquares[newrow][i].piece != Piece.EMPTY):
                            return False

                # if rows are empty but destination has an opoosite color piece, removes the piece and moves
                if(boardSquares[newrow][newcol].piece != Piece.EMPTY):
                    if(boardSquares[newrow][newcol].pieceColor == color):
                        return False

                    pieces.remove(boardSquares[newrow][newcol].sprite)
                    return True

                # if destination is just empty, valid move
                return True
            
        # --Black and White Knight--
        if(piece == Piece.KNIGHT):
            if(newrow == oldrow-2 and newcol == oldcol+1):
                return self.checkAndRemove(newrow, newcol, color)
            if(newrow == oldrow-1 and newcol == oldcol+2):
                return self.checkAndRemove(newrow, newcol, color)
            if(newrow == oldrow+1 and newcol == oldcol+2):
                return self.checkAndRemove(newrow, newcol, color)
            if(newrow == oldrow+2 and newcol == oldcol+1):
                return self.checkAndRemove(newrow, newcol, color)
            if(newrow == oldrow+2 and newcol == oldcol-1):
                return self.checkAndRemove(newrow, newcol, color)
            if(newrow == oldrow+1 and newcol == oldcol-2):
                return self.checkAndRemove(newrow, newcol, color)
            if(newrow == oldrow-1 and newcol == oldcol-2):
                return self.checkAndRemove(newrow, newcol, color)
            if(newrow == oldrow-2 and newcol == oldcol-1):
                return self.checkAndRemove(newrow, newcol, color)
        
        # --Black and White Bishop and Queen--
        if(piece == Piece.BISHOP or piece == Piece.QUEEN):
            if(int(math.fabs(newrow - oldrow)) == int(math.fabs(newcol - oldcol))):
                #[-, +]
                if(newrow < oldrow and newcol > oldcol): 
                    for i in range(1, oldrow-newrow):
                        if(boardSquares[oldrow-i][oldcol+i].piece != Piece.EMPTY):
                            return False
                
                    return self.checkAndRemove(newrow, newcol, color)
                
                #[+, +]
                elif (newrow > oldrow and newcol > oldcol): 
                    for i in range(1, newrow-oldrow):
                        if(boardSquares[oldrow+i][oldcol+i].piece != Piece.EMPTY):
                            return False
                
                    return self.checkAndRemove(newrow, newcol, color)
                
                #[+, -]
                elif (newrow > oldrow and newcol < oldcol): 
                    for i in range(1, newrow-oldrow):
                        if(boardSquares[oldrow+i][oldcol-i].piece != Piece.EMPTY):
                            return False
                
                    return self.checkAndRemove(newrow, newcol, color)
                
                #[-, -]
                elif (newrow < oldrow and newcol < oldcol):
                    for i in range(1, oldrow-newrow):
                        if(boardSquares[oldrow-i][oldcol-i].piece != Piece.EMPTY):
                            return False
                
                    return self.checkAndRemove(newrow, newcol, color)
        
        # --Black and White King--
        if(piece == Piece.KING):
            if(newrow == oldrow and (newcol == oldcol-1 or newcol == oldcol+1)):
                return self.checkAndRemove(newrow, newcol, color)
            elif((newrow == oldrow-1 or newrow == oldrow+1) and newcol == oldcol):
                return self.checkAndRemove(newrow, newcol, color)
            elif((newrow == oldrow-1 or newrow == oldrow+1) and (newcol == oldcol-1 or newcol == oldcol+1)):
                return self.checkAndRemove(newrow, newcol, color)
            elif((newrow == oldrow-1 and newcol == oldcol-1) or (newrow == oldrow+1 and newcol == oldcol+1)):
                return self.checkAndRemove(newrow, newcol, color)

        return False

    def move(self, piece, color, oldrow, oldcol, newrow, newcol):
        if (self.validMove(piece, color, oldrow, oldcol, newrow, newcol)):
            
            #boardSquares[newrow][newcol].copy(boardSquares[oldrow][oldcol])
            
            self.rect.x = (newcol * SQUARE_SIZE) + BOARD_START_X +1
            self.rect.y = (newrow * SQUARE_SIZE) + BOARD_START_X +2
            boardSquares[newrow][newcol].x = self.rect.x
            boardSquares[newrow][newcol].y = self.rect.y
            
            boardSquares[newrow][newcol] = Square(self.rect.x - 1, self.rect.y - 2, boardSquares[oldrow][oldcol].piece, boardSquares[oldrow][oldcol].pieceColor, boardSquares[oldrow][oldcol].sprite)
            boardSquares[oldrow][oldcol] = Square((oldcol * SQUARE_SIZE) + BOARD_START_X, (oldrow * SQUARE_SIZE) + BOARD_START_X, Piece.EMPTY, None, None)
            
            if(piece == Piece.PAWN):
                boardSquares[newrow][newcol].firstMove = False

            print(boardSquares[newrow][newcol])
            #self.rect = self.image.get_rect(topleft=(newrow * SQUARE_SIZE, newcol * SQUARE_SIZE))

    def __str__(self) -> str:
        return super().__str__() + str(self.rect)
    

def initializeBoard(pieces):
    for y in range(BOARD_START_X, BOARD_END_X, SQUARE_SIZE):
        row = int((y - BOARD_START_X) / SQUARE_SIZE)
        
        for x in range(BOARD_START_X, BOARD_END_X, SQUARE_SIZE):
            col = int((x - BOARD_START_X) / SQUARE_SIZE)
            
            # puts the correct pieces in the correct places on the boards
            # additions to sprite coords to center sprite
            if(row == 0):
                if(col == 0 or col == 7):
                    boardSquares[row][col] = Square(x, y, Piece.ROOK, "black", PieceSprite((x+1,y+2), ROOK_B_SPRITE))
                elif(col == 1 or col == 6):
                    boardSquares[row][col] = Square(x, y, Piece.KNIGHT, "black", PieceSprite((x+1,y+2), KNIGHT_B_SPRITE))
                elif(col == 2 or col == 5):
                    boardSquares[row][col] = Square(x, y, Piece.BISHOP, "black", PieceSprite((x+1,y+2), BISHOP_B_SPRITE))
                elif(col == 3):
                    boardSquares[row][col] = Square(x, y, Piece.QUEEN, "black", PieceSprite((x+1,y+2), QUEEN_B_SPRITE))
                elif(col == 4):
                    boardSquares[row][col] = Square(x, y, Piece.KING, "black", PieceSprite((x+1,y+2), KING_B_SPRITE))
            elif(row == 1):
                boardSquares[row][col] = Square(x, y, Piece.PAWN, "black", PieceSprite((x+1,y+2), PAWN_B_SPRITE))
            elif(row == 6):
                boardSquares[row][col] = Square(x, y, Piece.PAWN,  "white", PieceSprite((x+1,y+2), PAWN_W_SPRITE))
            elif(row == 7):
                if(col == 0 or col == 7):
                    boardSquares[row][col] = Square(x, y, Piece.ROOK, "white", PieceSprite((x+1,y+2), ROOK_W_SPRITE))
                elif(col == 1 or col == 6):
                    boardSquares[row][col] = Square(x, y, Piece.KNIGHT, "white", PieceSprite((x+1,y+2), KNIGHT_W_SPRITE))
                elif(col == 2 or col == 5):
                    boardSquares[row][col] = Square(x, y, Piece.BISHOP, "white", PieceSprite((x+1,y+2), BISHOP_W_SPRITE))
                elif(col == 3):
                    boardSquares[row][col] = Square(x, y, Piece.QUEEN, "white", PieceSprite((x+1,y+2), QUEEN_W_SPRITE))
                elif(col == 4):
                    boardSquares[row][col] = Square(x, y, Piece.KING, "white", PieceSprite((x+1,y+2), KING_W_SPRITE))
            else:
                boardSquares[row][col] = Square(x, y, Piece.EMPTY)

            if(boardSquares[row][col].sprite != None):
                pieces.add(boardSquares[row][col].sprite)

# draws board
def drawBoard():
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
def findKing(color):
    for i in range(ROWS):
        for j in range(COLS):
            if(boardSquares[i][j].piece == Piece.KING and boardSquares[i][j].pieceColor == color):
                return (i, j)

# makes sure iteration is within bounds of board
def inBoardBounds(i,j):
    return (0 <= i < 8) and (0 <= j < 8)

# returns 0 for no check, 1 for black in check, 2 for white in check
def inCheck():
    rowK, colK = findKing("black")
    for i in range(ROWS):
        for j in range(COLS):
            if (boardSquares[i][j].pieceColor == "white"):
                
                # if the king is diagonally from a pawn, king in check
                if(boardSquares[i][j].piece == Piece.PAWN and inBoardBounds(i,j)):
                    if((i-1 == rowK and j-1 == colK) or (i-1 == rowK and j+1 == colK)):
                        return 1

                # Queen shares up and down functionality with Rook
                if(boardSquares[i][j].piece == Piece.ROOK or boardSquares[i][j].piece == Piece.QUEEN):
                    #[-, x], up
                    king = False
                    for k in range(rowK, i):
                        if (boardSquares[k][j].piece != Piece.EMPTY and boardSquares[k][j].piece != Piece.KING):
                            king = False
                            break
                        if (boardSquares[k][j].piece == Piece.KING and boardSquares[k][j].pieceColor == "black"):
                            king = True

                    if(king):
                        return 1

                    #[+, x], down
                    king = False
                    for k in range(i+1, rowK+1):
                        if (boardSquares[k][j].piece != Piece.EMPTY and boardSquares[k][j].piece != Piece.KING):
                            king = False
                            break
                        if (boardSquares[k][j].piece == Piece.KING and boardSquares[k][j].pieceColor == "black"):
                            king = True

                    if(king):
                        return 1

                    #[x, -], left
                    king = False
                    for k in range(colK, j):
                        if (boardSquares[i][k].piece != Piece.EMPTY and boardSquares[i][k].piece != Piece.KING):
                            king = False
                            break
                        if (boardSquares[i][k].piece == Piece.KING and boardSquares[i][k].pieceColor == "black"):
                            king = True

                    if(king):
                        return 1

                    #[x, +], right   
                    king = False
                    for k in range(j+1, colK+1):
                        if (boardSquares[i][k].piece != Piece.EMPTY and boardSquares[i][k].piece != Piece.KING):
                            king = False
                            break
                        if (boardSquares[i][k].piece == Piece.KING and boardSquares[i][k].pieceColor == "black"):
                            king = True

                    if(king):
                        return 1

                # Bishop and Queen share diagonal functionality
                if(boardSquares[i][j].piece == Piece.BISHOP or boardSquares[i][j].piece == Piece.QUEEN):
                    #[-, +], up right
                    king = False
                    for k in range(1, i-rowK+1):
                        if (inBoardBounds(i-k, j+k) and boardSquares[i-k][j+k].piece != Piece.EMPTY and boardSquares[i-k][j+k].piece != Piece.KING):
                            #print("blocking king", rowK, colK, "[",i, j,"] ", k, i-k, j+k)
                            king = False
                            break
                        if (inBoardBounds(i-k, j+k) and boardSquares[i-k][j+k].piece == Piece.KING and boardSquares[i-k][j+k].pieceColor == "black"):
                            #print("king location", i-k, j+k)
                            king = True

                    #print(king)
                    if(king):
                        return 1

                    #[+, +], down right
                    king = False
                    for k in range(1, rowK-i+1):
                        if (inBoardBounds(i+k, j+k) and boardSquares[i+k][j+k].piece != Piece.EMPTY and boardSquares[i+k][j+k].piece != Piece.KING):
                            king = False
                            break
                        if (inBoardBounds(i+k, j+k) and boardSquares[i+k][j+k].piece == Piece.KING and boardSquares[i+k][j+k].pieceColor == "black"):
                            king = True

                    #print(king)
                    if(king):
                        return 1

                    #[+, -], down left
                    king = False
                    for k in range(1, rowK-i+1):
                        if (inBoardBounds(i+k, j-k) and boardSquares[i+k][j-k].piece != Piece.EMPTY and boardSquares[i+k][j-k].piece != Piece.KING):
                            king = False
                            break
                        if (inBoardBounds(i+k, j-k) and boardSquares[i+k][j-k].piece == Piece.KING and boardSquares[i+k][j-k].pieceColor == "black"):
                            king = True

                    if(king):
                        return 1

                    #[-, -], up left   
                    king = False
                    for k in range(1, i-rowK+1):
                        if (inBoardBounds(i-k, j-k) and boardSquares[i-k][j-k].piece != Piece.EMPTY and boardSquares[i-k][j-k].piece != Piece.KING):
                            king = False
                            break
                        if (inBoardBounds(i-k, j-k) and boardSquares[i-k][j-k].piece == Piece.KING and boardSquares[i-k][j-k].pieceColor == "black"):
                            king = True

                    if(king):
                        return 1
                
                if(boardSquares[i][j].piece == Piece.KNIGHT):
                    pass
                if(boardSquares[i][j].piece == Piece.KING):
                    pass



    row, col = findKing("white")
    
    
    return False

# Groups sprite together to be displayed
pieces = pygame.sprite.Group()

# Initializes board with pieces
initializeBoard(pieces)
pieceSelected = False
selectedPos = (-1,-1)

running = True
while running:
    # "X"-ed window out
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif (event.type == pygame.MOUSEBUTTONUP and (not pieceSelected)):
            pos = pygame.mouse.get_pos()

            if(BOARD_START_X <= pos[0] <= BOARD_END_X and BOARD_START_X <= pos[1] <= BOARD_END_X ):
                selectedPos = (int((pos[1] - BOARD_START_X) / SQUARE_SIZE), int((pos[0] - BOARD_START_X) / SQUARE_SIZE))
                print(boardSquares[selectedPos[0]][selectedPos[1]].piece)

                if(boardSquares[selectedPos[0]][selectedPos[1]].piece != Piece.EMPTY):
                    pieceSelected = True
                else:
                    pieceSelected = False
                    selectedPos = (-1,-1) 

        elif (event.type == pygame.MOUSEBUTTONUP and pieceSelected):
            pos = pygame.mouse.get_pos()
            x, y = pos
            oldrow = selectedPos[0]
            oldcol = selectedPos[1]
            newrow = int((y - BOARD_START_X) / SQUARE_SIZE)
            newcol = int((x - BOARD_START_X) / SQUARE_SIZE)

            if(BOARD_START_X <= x <= BOARD_END_X and BOARD_START_X <= y <=BOARD_END_X):
                print(oldrow, oldcol, newrow, newcol, boardSquares[oldrow][oldcol].piece)
                boardSquares[oldrow][oldcol].sprite.move(boardSquares[oldrow][oldcol].piece, boardSquares[oldrow][oldcol].pieceColor, oldrow, oldcol, newrow, newcol)
            else:
                print("out of bounds")

            # checks if the king is in check after movements
            if(inCheck() == 1):
                print("black king in check")
            elif (inCheck() == 2):
                print("white king in check")

            #reset selected piece
            pieceSelected = False
            selectedPos = (-1,-1)


    # Fill the background with white
    screen.fill(BACKGROUND_COLOR)

    # Creates chess board border and blit it to the center of the screen
    surf = pygame.Surface((BOARD_SIZE + 2, BOARD_SIZE + 2))
    surf.fill((DARK_SQUARE_COLOR))
    screen.blit(surf, (BOARD_START_X - 1, BOARD_START_X -1))

    # draws board
    drawBoard()

    # if piece is selected, highlights it with a color
    if(pieceSelected):
        pygame.draw.rect(screen, (0,68,116), pygame.Rect(boardSquares[selectedPos[0]][selectedPos[1]].x, boardSquares[selectedPos[0]][selectedPos[1]].y, SQUARE_SIZE, SQUARE_SIZE) )
               
    # draws pieces to screen
    pieces.draw(screen)

    # updates the screen every frame
    pygame.display.flip()


pygame.quit()
