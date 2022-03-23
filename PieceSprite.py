import pygame
import math
from Piece import Piece as Piece
from square import Square as Square

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500
ROWS = 8
COLS = 8
SQUARE_SIZE = 46
BOARD_SIZE = SQUARE_SIZE * COLS
BOARD_START_X = int(( SCREEN_WIDTH / 2 ) - (BOARD_SIZE / 2))
BOARD_END_X = int(( SCREEN_WIDTH / 2 ) + (BOARD_SIZE / 2))


class PieceSprite(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

    def getImage(self):
        return self.image

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
            print("Same square, not a move.", oldrow, oldcol, newrow, newcol)
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
 