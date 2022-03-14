import pygame
import enum
pygame.init()

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500
ROWS = 8
COLS = 8

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Chess AI')
boardSquares = [[0 for i in range(COLS)] for j in range(ROWS)]

class Piece(enum.Enum):
    EMPTY = "EMPTY"
    PAWN = "PAWN"
    ROOK = "ROOK"
    KNIGHT = "KNIGHT"
    BISHOP = "BISHOP"
    QUEEN = "QUEEN"
    KING = "KING"


class Square:
    def __init__(self, x = 0, y = 0, piece = Piece.EMPTY):
        self.x = x
        self.y = y
        self.piece = piece

def initializeBoard():
    for y in range(98, 401, 38):
        row = int((y - 98) / 38)
        
        for x in range(98, 401, 38):
            col = int((x - 98) / 38)
            
            if((row == 0 or row == 7) and (col == 0 or col == 7)):
                boardSquares[row][col] = Square(x, y, Piece.ROOK)
            elif((row == 0 or row == 7) and (col == 1 or col == 6)):
                boardSquares[row][col] = Square(x, y, Piece.KNIGHT)
            elif((row == 0 or row == 7) and (col == 2 or col == 5)):
                boardSquares[row][col] = Square(x, y, Piece.BISHOP)
            elif((row == 0 or row == 7) and (col == 3)):
                boardSquares[row][col] = Square(x, y, Piece.QUEEN)
            elif((row == 0 or row == 7) and (col == 4)):
                boardSquares[row][col] = Square(x, y, Piece.KING)
            elif(row == 1 or row == 6):
                boardSquares[row][col] = Square(x, y, Piece.PAWN)
            else:
                boardSquares[row][col] = Square(x, y, Piece.EMPTY)

# draws board
def drawBoard():
    squareSize = 38

    white = False
    color = (255,255,255)

    # 96 is where the board starts, because (500 / 2) - (304 / 2) = 98 
    for y in range(98, 402, squareSize):
        for x in range(98, 402, squareSize):
            square = pygame.Rect(x, y, squareSize, squareSize)
            
            # Alternates color
            if(white):
                color = (0,0,0)
                white = False
            else:
                color = (255,255,255)
                white = True

            pygame.draw.rect(screen, color, square)
        
        # alternates next row color
        if(white):
            white = False
        else:
            white = True

 
initializeBoard()

running = True
while running:
    # "X"-ed window out
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Fill the background with white
    screen.fill((255, 255, 255))

    # Creates chess board border and blit it to the center of the screen
    surf = pygame.Surface((306,306)) #304 is 38 x 8
    surf.fill((0,0,0))
    #border = surf.get_rect()

    screen.blit(surf, (97, 97))

    drawBoard()

    # updates the screen every frame
    pygame.display.flip()


pygame.quit()
