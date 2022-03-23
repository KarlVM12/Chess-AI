from cmath import inf
import math
from game import game as game
from Piece import Piece as Piece
import chess
import random

#transfer the game into a state
def gameToState(game):
    state = [[0 for i in range(8)] for j in range(8)]

    for i in range(8):
        for j in range(8):
            state[i][j] = (game.boardSquares[i][j].piece, ("w" if game.boardSquares[i][j].pieceColor == "white" else "b"))

    boardString = ''
    for i in range(8):
        for j in range(8):
            if(state[i][j][0] == Piece.PAWN and state[i][j][1] == "w"):
                boardString += 'P'
            elif(state[i][j][0] == Piece.PAWN and state[i][j][1] == "b"):
                boardString += 'p'
            elif(state[i][j][0] == Piece.BISHOP and state[i][j][1] == "w"):
                boardString += 'B'
            elif(state[i][j][0] == Piece.BISHOP and state[i][j][1] == "b"):
                boardString += 'b'
            elif(state[i][j][0] == Piece.KNIGHT and state[i][j][1] == "w"):
                boardString += 'N'
            elif(state[i][j][0] == Piece.KNIGHT and state[i][j][1] == "b"):
                boardString += 'n'    
            elif(state[i][j][0] == Piece.ROOK and state[i][j][1] == "w"):
                boardString += 'R'
            elif(state[i][j][0] == Piece.ROOK and state[i][j][1] == "b"):
                boardString += 'r'        
            elif(state[i][j][0] == Piece.QUEEN and state[i][j][1] == "w"):
                boardString += 'Q'
            elif(state[i][j][0] == Piece.QUEEN and state[i][j][1] == "b"):
                boardString += 'q'    
            elif(state[i][j][0] == Piece.KING and state[i][j][1] == "w"):
                boardString += 'K'
            elif(state[i][j][0] == Piece.KING and state[i][j][1] == "b"):
                boardString += 'k'
            elif(state[i][j][0] == Piece.EMPTY):
                #print(boardString)
                if(len(boardString) > 0 and boardString[-1].isnumeric()):
                    num = int(boardString[-1])
                    num += 1
                    boardString = boardString[:-1] + str(num)
                else:
                    boardString += '1'    


        if(i!=7):
            boardString +='/'
    
    if (game.playerTurn == "white"):
        boardString += ' w - - 0 1'
    else:
        boardString += ' b - - 0 1'

    chessState = chess.Board(boardString)

    return chessState

# transfer the san move to a number row col move
def moveToNum(move):
    rowCol = [0 for i in range(4)]
    
    moveString = str(move)
    for i in range(0,4):
        if(moveString[i] == 'a'):
            rowCol[i] = 0
        elif(moveString[i] == 'b'):
            rowCol[i] = 1
        elif(moveString[i] == 'c'):
            rowCol[i] = 2
        elif(moveString[i] == 'd'):
            rowCol[i] = 3
        elif(moveString[i] == 'e'):
            rowCol[i] = 4
        elif(moveString[i] == 'f'):
            rowCol[i] = 5
        elif(moveString[i] == 'g'):
            rowCol[i] = 6
        elif(moveString[i] == 'h'):
            rowCol[i] = 7
        else:
            rowCol[i] = 8 - int(moveString[i])
    
    return rowCol


class State():
    def __init__(self):
        self.state = chess.Board()
        self.children = set()
        self.parent = None
        self.N = 0  #number of times parent visited
        self.n = 0  #number of times child visited
        self.u = 0  #current utility of state

# exploit and explore balance test
def UBC1Test(state):
    c = 2
    exploit = state.u+c
    explore = (math.sqrt(math.log(state.N+math.e+(10**-6))/(state.n+(10**-10))))
    
    result = exploit*explore
    return result

#expand children
def expand(state, playerTurn):
    # if nothing to expand
    if(len(state.children) == 0):
        return state

    MAXUCB = -inf
    if(playerTurn == "black"):
        MAXUCB = -inf
        successorState = None
        
        for child in state.children:
            childUtility = UBC1Test(child)

            if (childUtility > MAXUCB):
                MAXUCB = childUtility
                successorState = child
        
        return expand(successorState, playerTurn)
    
    else:
        MINUCB = inf
        successorState = None
        
        for child in state.children:
            childUtility = UBC1Test(child)

            if (childUtility < MINUCB):
                MINUCB = childUtility
                successorState = child
        
        return expand(successorState, playerTurn)

# playout of a simulation
def playout(game, stateIn):
    if(stateIn.state.is_game_over()):
        end = stateIn.state

        if(end.result() == '1-0'):
            return (1, stateIn)
        elif(end.result() == '0-1'):
            return (-1, stateIn)
        else:
            return (0, stateIn)

    # gets all children of current state
    possibleMoves = [stateIn.state.san(i) for i in list(stateIn.state.legal_moves)]

    # getting all possible moves as child of current state
    for a in possibleMoves:
        
        newState = State()
        newState.state = chess.Board(stateIn.state.fen())
        newState.state.push_san(a)
        
        child = State()
        child.state = newState.state
        child.parent = stateIn
        stateIn.children.add(child)
    
    # random picks a child and then continues to playout that child till the end of the game
    randomState = random.choice(list(stateIn.children))

    return playout(game, randomState)
    
# back propogates back up the tree, adding the time we have visited the children and parent, along with that child's utility     
def backProp(result, state):
    state.n += 1
    state.u += result

    while(state.parent != None):
        state.N += 1
        state = state.parent

    return state

def MonteCarloSearch(game, playerTurn, simulations):
    
    if(game.isTerminal()):
        return (-1,-1,-1,-1)

    
    
    state = State()
    state.state = gameToState(game)

    possibleMoves = [state.state.san(i) for i in list(state.state.legal_moves)]

    mapOfMoves = dict()

    # getting all possible moves as child of current state
    for a in possibleMoves:
        
        newState = State()
        newState.state = chess.Board(state.state.fen())
        move = newState.state.push_san(a)
        
        child = State()
        child.state = newState.state
        child.parent = state
        state.children.add(child)

        rowCol = moveToNum(move)

        mapOfMoves[child] = (rowCol[0], rowCol[1], rowCol[2], rowCol[3])
    
    
    # simulations to select next state
    while(simulations != 0):
        if(playerTurn == "black"):
            MAXUCB = -inf
            successorState = None
            
            for child in state.children:
                childUtility = UBC1Test(child)

                if (childUtility > MAXUCB):
                    MAXUCB = childUtility
                    successorState = child

            #expand and playout
            expandedChild = expand(successorState, playerTurn)
            value, playedOut = playout(game, expandedChild)
            state = backProp(value, state)
            simulations -= 1

        else:
            MINUCB = inf
            successorState = None
            
            for child in state.children:
                childUtility = UBC1Test(child)

                if (childUtility < MINUCB):
                    MINUCB = childUtility
                    successorState = child

            #expand and playout
            expandedChild = expand(successorState, playerTurn)
            value, playedOut = playout(expandedChild)
            state = backProp(value, state)
            simulations -= 1
    

    # selecting the best move for black
    if(playerTurn == "black"):
        MAXValue = -inf
        childIndex = -1
        action = None
        for child in state.children:
            childUtility = UBC1Test(child)
            
            if(childUtility > MAXValue):
                MAXValue = childUtility
                action = mapOfMoves[child]
        
        return action
    # selecting the best move for white
    else:
        MINValue = inf
        childIndex = -1
        action = None

        for child in state.children:
            childUtility = UBC1Test(child)
            
            if(childUtility < MINValue):
                MINValue = childUtility
                action = mapOfMoves[child]
        
        return action