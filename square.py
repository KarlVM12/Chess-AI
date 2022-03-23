import copy
from Piece import Piece as Piece

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500
ROWS = 8
COLS = 8
SQUARE_SIZE = 46
BOARD_SIZE = SQUARE_SIZE * COLS
BOARD_START_X = int(( SCREEN_WIDTH / 2 ) - (BOARD_SIZE / 2))
BOARD_END_X = int(( SCREEN_WIDTH / 2 ) + (BOARD_SIZE / 2))


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
        square = Square()
        square.x = self.x
        square.y = self.y
        square.row = self.row 
        square.col = self.col 
        square.piece = self.piece
        square.firstMove = self.firstMove
        square.pieceColor = self.pieceColor
        #print(self.sprite.image.__str__())
        #square.sprite = PieceSprite((self.x+1, self.y+2), None)
        #square.sprite.image = copy.deepcopy(self.sprite.image)

        square.sprite = copy.copy(self.sprite)
        print(square.sprite, self.sprite)
        #square.sprite.rect = self.sprite.rect.copy()
    
    def __str__(self) -> str:
        return "( " + str(self.y) + ", " + str(self.x) + ") [ " + str(self.row) + ", " + str(self.col) + "] " + str(self.piece) + " " + str(self.sprite)
