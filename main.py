import os.path
import math
from string import whitespace
import pygame
import copy
import enum
from Piece import Piece as Piece
from game import game as game
import alphaBetaPruning as ab
import monteCarlo as MC

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


chess = game()
chess.newGame()

# game is running and it is not a terminal state
running = True
while running:
    # "X"-ed window out

    if(chess.isTerminal()):
        chess.newGame()

    
    #=============================#
    #= Black Move, AI
    #=============================#

    if(chess.playerTurn == "black"):
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
            
        #===========#
        #  AI moves #
        #===========#
        
        # Alpha Beta
        #(value, oldrow, oldcol, newrow, newcol) = ab.alphaBetaSearch(chess, 3)
        
        #Monte Carlo
        # switched row and column because thats what san chess notation does
        (oldcol, oldrow, newcol, newrow) = MC.MonteCarloSearch(chess, "black", 5)
        validMove = chess.boardSquares[oldrow][oldcol].sprite.move(chess, chess.boardSquares[oldrow][oldcol].piece, chess.boardSquares[oldrow][oldcol].pieceColor, oldrow, oldcol, newrow, newcol)
        
        if(validMove):
            print("AI: [",oldrow,",",oldcol,"] -> [",newrow,",",newcol,"]")
            chess.playerTurn = "white"
        else:
            print("AI invalid move")

        if(chess.inCheck() == 1 and chess.blackCheck):
            print("Invalid move, black king still in check")
            if(validMove):
                chess.undoMove(oldrow, oldcol, newrow, newcol)

            chess.playerTurn = "black"

        # if it switched over to white and black is in check, black put itself into check, invalid
        elif(chess.inCheck() == 1 and chess.playerTurn == "white"):
            print("Invalid move, black can't put itself into check")
            if(validMove):
                chess.undoMove(oldrow, oldcol, newrow, newcol)

            chess.playerTurn = "black"


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


    #----------------------------------#
    # Event Loop for white player moves
    #----------------------------------#
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

    # displaying score of the game
    font = pygame.font.Font('freesansbold.ttf', 16)
    score= font.render("Score:", True, (0,0,0))
    white = font.render("White: " + str(chess.whiteScore), True, (0,0,0))
    black = font.render("Black: " + str(chess.blackScore), True, (0,0,0))
  
    scoreRect = score.get_rect()
    scoreRect.topleft = (66, 436)
    whiteRect = white.get_rect()
    whiteRect.topleft = (66, 456)
    blackRect = black.get_rect()
    blackRect.topleft = (66, 476)
    
    screen.blit(score, scoreRect)
    screen.blit(white, whiteRect)
    screen.blit(black, blackRect)



    # updates the screen every frame
    pygame.display.flip()


pygame.quit()
