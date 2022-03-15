import os.path
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
    def __init__(self, x = 0, y = 0, piece = Piece.EMPTY, sprite = None):
        self.x = x
        self.y = y
        self.piece = piece
        self.sprite = sprite

class PieceSprite(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

def initializeBoard(pieces):
    for y in range(BOARD_START_X, BOARD_END_X, SQUARE_SIZE):
        row = int((y - BOARD_START_X) / SQUARE_SIZE)
        
        for x in range(BOARD_START_X, BOARD_END_X, SQUARE_SIZE):
            col = int((x - BOARD_START_X) / SQUARE_SIZE)
            
            # puts the correct pieces in the correct places on the boards
            # additions to sprite coords to center sprite
            if(row == 0):
                if(col == 0 or col == 7):
                    boardSquares[row][col] = Square(x, y, Piece.ROOK, PieceSprite((x+1,y+2), ROOK_B_SPRITE))
                elif(col == 1 or col == 6):
                    boardSquares[row][col] = Square(x, y, Piece.KNIGHT, PieceSprite((x+1,y+2), KNIGHT_B_SPRITE))
                elif(col == 2 or col == 5):
                    boardSquares[row][col] = Square(x, y, Piece.BISHOP, PieceSprite((x+1,y+2), BISHOP_B_SPRITE))
                elif(col == 3):
                    boardSquares[row][col] = Square(x, y, Piece.QUEEN, PieceSprite((x+1,y+2), QUEEN_B_SPRITE))
                elif(col == 4):
                    boardSquares[row][col] = Square(x, y, Piece.KING, PieceSprite((x+1,y+2), KING_B_SPRITE))
            elif(row == 1):
                boardSquares[row][col] = Square(x, y, Piece.PAWN, PieceSprite((x+1,y+2), PAWN_B_SPRITE))
            elif(row == 6):
                boardSquares[row][col] = Square(x, y, Piece.PAWN, PieceSprite((x+1,y+2), PAWN_W_SPRITE))
            elif(row == 7):
                if(col == 0 or col == 7):
                    boardSquares[row][col] = Square(x, y, Piece.ROOK, PieceSprite((x+1,y+2), ROOK_W_SPRITE))
                elif(col == 1 or col == 6):
                    boardSquares[row][col] = Square(x, y, Piece.KNIGHT, PieceSprite((x+1,y+2), KNIGHT_W_SPRITE))
                elif(col == 2 or col == 5):
                    boardSquares[row][col] = Square(x, y, Piece.BISHOP, PieceSprite((x+1,y+2), BISHOP_W_SPRITE))
                elif(col == 3):
                    boardSquares[row][col] = Square(x, y, Piece.QUEEN, PieceSprite((x+1,y+2), QUEEN_W_SPRITE))
                elif(col == 4):
                    boardSquares[row][col] = Square(x, y, Piece.KING, PieceSprite((x+1,y+2), KING_W_SPRITE))
            else:
                boardSquares[row][col] = Square(x, y, Piece.EMPTY, None)

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

# Groups sprite together to be displayed
pieces = pygame.sprite.Group()

# Initializes board with pieces
initializeBoard(pieces)

running = True
while running:
    # "X"-ed window out
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        """ elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                boardSquares[0][0].sprite.move(0, SQUARE_SIZE) """


    # Fill the background with white
    screen.fill(BACKGROUND_COLOR)

    # Creates chess board border and blit it to the center of the screen
    surf = pygame.Surface((BOARD_SIZE + 2, BOARD_SIZE + 2))
    surf.fill((DARK_SQUARE_COLOR))
    screen.blit(surf, (BOARD_START_X - 1, BOARD_START_X -1))

    # draws board
    drawBoard()

    # draws pieces to screen
    pieces.draw(screen)

    # updates the screen every frame
    pygame.display.flip()


pygame.quit()
