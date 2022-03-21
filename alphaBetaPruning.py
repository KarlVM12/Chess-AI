# alpha beta pruning

from math import inf
from Piece import Piece as Piece

def alphaBetaSearch(game):
    (value, oldrow, oldcol, newrow, newcol) = MAXValue(game, -2, 2) 
    return (oldrow, oldcol, newrow, newcol)

    
# max player is black, the AI
def MAXValue(game, alpha, beta):

    # values for maxv are
    # -1 lost
    # 0 tie
    # 1 win
    
    # worst value it can be
    v = -2
    maxOldRow = None
    maxOldCol = None
    maxNewRow = None
    maxNewCol = None


    # terminal check which returns utility
    if (game.isTerminal()):
        return game.utility("black")

    # for a in actions
    for row in range(8):
        for col in range(8): 
        
            if(game.boardSquares[row][col].piece != Piece.EMPTY and game.boardSquares[row][col].pieceColor == "black"):

                # gets possible moves of that piece
                possibleMoves = game.piecePossibleMove("black", game.boardSquares[row][col].piece, row, col)

                # goes through the possible moves
                for a in possibleMoves:
                    # moves piece
                    game.boardSquares[row][col].sprite.move(game, game.boardSquares[row][col].piece, "black", row, col, a[0], a[1])

                    # switches to min turn
                    (v2, minOldRow, minOldCol, minNewRow, minNewCol) = MINValue(game, alpha, beta)

                    if (v2 > v):
                        v = v2
                        maxOldRow = row
                        maxOldCol = col
                        maxNewRow = a[0]
                        maxNewCol = a[1]
                        alpha = max(alpha, v)
                    
                    # undo move afterwards
                    game.undoMove(row, col, a[0], a[1])

                    if (v >= beta):
                        return (v, maxOldRow, maxOldCol, maxNewRow, maxNewCol)

    return (v, maxOldRow, maxOldCol, maxNewRow, maxNewCol)

# min player is white, the player
def MINValue(game, alpha, beta):

    # values for minV are
    # -1 win
    # 0 tie
    # 1 loss
    
    # worse value it can be
    v = 2
    minOldRow = None
    minOldCol = None
    minNewRow = None
    minNewCol = None

# terminal check which returns utility
    if (game.isTerminal()):
        return game.utility("white")

    # for a in actions
    for row in range(8):
        for col in range(8): 
        
            if(game.boardSquares[row][col].piece != Piece.EMPTY and game.boardSquares[row][col].pieceColor == "white"):

                # gets possible moves of that piece
                possibleMoves = game.piecePossibleMove("white", game.boardSquares[row][col].piece, row, col)

                # goes through the possible moves
                for a in possibleMoves:
                    # moves piece
                    game.boardSquares[row][col].sprite.move(game, game.boardSquares[row][col].piece, "white", row, col, a[0], a[1])

                    # switches to max turn
                    (v2, maxOldRow, maxOldCol, maxNewRow, maxNewCol) = MAXValue(game, alpha, beta)

                    if (v2 < v):
                        v = v2
                        minOldRow = row
                        minOldCol = col
                        minNewRow = a[0]
                        minNewCol = a[1]
                        beta = min(beta, v)
                    
                    # undo move afterwards
                    game.undoMove(row, col, a[0], a[1])

                    if (v <= alpha):
                        return (v, minOldRow, minOldCol, minNewRow, minNewCol)

    return (v, minOldRow, minOldCol, minNewRow, minNewCol)