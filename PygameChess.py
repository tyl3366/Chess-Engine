import pygame
import chess
import math
import engine
import os

X = 800
Y = 800
screen = pygame.display.set_mode((X, Y))
pygame.init()

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)

b = chess.Board()

# More efficient way to do this?
pieces = {'p': pygame.image.load('images/bp.png'),
          'n': pygame.image.load('images/bN.png'),
          'b': pygame.image.load('images/bB.png'),
          'r': pygame.image.load('images/bR.png'),
          'q': pygame.image.load('images/bQ.png'),
          'k': pygame.image.load('images/bK.png'),
          'P': pygame.image.load('images/wp.png'),
          'N': pygame.image.load('images/wN.png'),
          'B': pygame.image.load('images/wB.png'),
          'R': pygame.image.load('images/wR.png'),
          'Q': pygame.image.load('images/wQ.png'),
          'K': pygame.image.load('images/wK.png'),
          }

def update(screen,board):
    for i in range(64):
        piece = board.piece_at(i)
        if piece == None:
            pass
        else:
            screen.blit(pieces[str(piece)],((i%8)*100, 700-(i//8)*100))
    
    for i in range(7):
        i += 1
        pygame.draw.line(screen, WHITE, (0,i*100), (800,i*100))
        pygame.draw.line(screen, WHITE, (i*100,0), (i*100,800))

    pygame.display.flip()
    
def color_squares(screen):
    global colors
    colors = [WHITE, GREY]
    for row in range(8):
        for column in range(8):
            color = colors[((row + column) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(column * 100, row * 100, 100, 100))

def main(board, engine, engine_color):
    
    screen.fill(WHITE)
    color_squares(screen)
    pygame.display.set_caption('PhoenixEngine')

    index_moves = []
    
    while True:
        update(screen, board)
     
        if board.turn == engine_color:
            move, depth, evaluation = engine.getBestMove(board)
            board.push(move)
            print(move)
            

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    screen.fill(pygame.Color("white"))
                    color_squares(screen)
                    pos = pygame.mouse.get_pos()

                    square = (math.floor(pos[0]/100), math.floor(pos[1]/100))
                    index = (7-square[1])*8+(square[0])

                    if index in index_moves: 
                        move = moves[index_moves.index(index)]

                        board.push(move)
                        index=None
                        index_moves = []
                        
                    else:
                        
                        piece = board.piece_at(index)
                        
                        if piece == None:
                            pass
                        
                        else:
                            all_moves = list(board.legal_moves)
                            moves = []
                            
                            for m in all_moves:
                                if m.from_square == index:
                                    moves.append(m)
                                    t = m.to_square

                                    TX1 = 100*(t%8)
                                    TY1 = 100*(7-t//8)

                                    pygame.draw.rect(screen,BLUE,pygame.Rect(TX1,TY1,100,100),5)
                                    
                            index_moves = [a.to_square for a in moves]

        if board.outcome() != None:
            print(board.outcome())
            break

    pygame.quit()
    
board = chess.Board()

main(board, engine, chess.BLACK)