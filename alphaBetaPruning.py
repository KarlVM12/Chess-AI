# alpha beta pruning

from math import inf
import copy
from Piece import Piece as Piece
from game import game as game


def gameToState(game):
    state = [[0 for i in range(8)] for j in range(8)]

    for i in range(8):
        for j in range(8):
            state[i][j] = game.boardSquares[i][j].piece

    return state

def alphaBetaSearch(gameIn, depth):
    #gameIn.copy(chess)
    #game = gameIn
    state = gameToState(gameIn)
    #print(state)
    #print(gameIn)

    (value, oldrow, oldcol, newrow, newcol) = MAXValue(gameIn, state, -1000, 1000, depth, -1, -1, -1, -1) 
    return (value, oldrow, oldcol, newrow, newcol)

    
# max player is black, the AI
def MAXValue(game, state, alpha, beta, depth, maxOldRow, maxOldCol, maxNewRow, maxNewCol):

    # values for maxv are
    # -1 lost
    # 0 tie
    # 1 win
    
    # worst value it can be
    v = -1000

    # terminal check which returns utility
    if (game.isCutoff(depth)):
        return game.eval("black", maxOldRow, maxOldCol, maxNewRow, maxNewCol)

    # for a in actions
    for row in range(8):
        for col in range(8): 
        
            if(game.boardSquares[row][col].piece != Piece.EMPTY and game.boardSquares[row][col].pieceColor == "black"):

                # gets possible moves of that piece
                possibleMoves = game.piecePossibleMoves("black", game.boardSquares[row][col].piece, row, col)
                if(game.boardSquares[row][col].piece == Piece.KING and game.inCheck()):
                    possibleMoves = game.piecePossibleMoves("white", Piece.KING, row, col)
                    print(game.boardSquares[row][col].pieceColor, "King", possibleMoves)

                # goes through the possible moves
                for a in possibleMoves:
                    # moves piece
                    #print("black", game.boardSquares[row][col].piece, "at", row, col,  possibleMoves)
                    first = False
                    if(game.boardSquares[row][col].firstMove):
                        first = True

                    validMove = game.boardSquares[row][col].sprite.move(game, game.boardSquares[row][col].piece, "black", row, col, a[0], a[1])
                    #print(validMove, a[0], a[1])

                    if(validMove):
                        # switches to min turn
                        state = gameToState(game)

                        game.undoMove(row, col, a[0], a[1])
                        game.boardSquares[row][col].firstMove = first
                        
                        (v2, minOldRow, minOldCol, minNewRow, minNewCol) = MINValue(game, state, alpha, beta, depth-1, row, col, a[0], a[1])
                        if (v2 > v):
                            v = v2
                            maxOldRow = row
                            maxOldCol = col
                            maxNewRow = a[0]
                            maxNewCol = a[1]
                            alpha = max(alpha, v)
                        
                        # undo move afterwards
                        #game.undoMove(row, col, a[0], a[1])

                        if (v >= beta):
                            return (v, maxOldRow, maxOldCol, maxNewRow, maxNewCol)

    return (v, maxOldRow, maxOldCol, maxNewRow, maxNewCol)

# min player is white, the player
def MINValue(game, state, alpha, beta, depth, minOldRow, minOldCol, minNewRow, minNewCol):

    # values for minV are
    # -1 win
    # 0 tie
    # 1 loss
    
    # worse value it can be
    v = 1000

# terminal check which returns utility
    if (game.isCutoff(depth)):
        return game.eval("white", minOldRow, minOldCol, minNewRow, minNewCol)

    # for a in actions
    for row in range(8):
        for col in range(8): 
        
            if(game.boardSquares[row][col].piece != Piece.EMPTY and game.boardSquares[row][col].pieceColor == "white"):

                # gets possible moves of that piece
                possibleMoves = game.piecePossibleMoves("white", game.boardSquares[row][col].piece, row, col)
                if(game.boardSquares[row][col].piece == Piece.KING and game.inCheck()):
                    possibleMoves = game.piecePossibleMoves("white", Piece.KING, row, col) 
                    print(game.boardSquares[row][col].pieceColor, "King", possibleMoves)

                # goes through the possible moves
                for a in possibleMoves:
                    # moves piece

                    #print("white", game.boardSquares[row][col].piece, "at", row, col,  possibleMoves)
                    first = False
                    if(game.boardSquares[row][col].firstMove == True):
                        first = True

                    validMove = game.boardSquares[row][col].sprite.move(game, game.boardSquares[row][col].piece, "white", row, col, a[0], a[1])
                    #print(validMove, a[0], a[1])
                    
                    if(validMove):
                        # switches to max turn

                        state = gameToState(game)
                        
                        game.undoMove(row, col, a[0], a[1])
                        game.boardSquares[row][col].firstMove = first
                        (v2, maxOldRow, maxOldCol, maxNewRow, maxNewCol) = MAXValue(game, state, alpha, beta, depth-1, row, col, a[0], a[1])
                        

                        if (v2 < v):
                            v = v2
                            minOldRow = row
                            minOldCol = col
                            minNewRow = a[0]
                            minNewCol = a[1]
                            beta = min(beta, v)
                        

                        if (v <= alpha):
                            return (v, minOldRow, minOldCol, minNewRow, minNewCol)

    return (v, minOldRow, minOldCol, minNewRow, minNewCol)