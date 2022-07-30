import pygame
from checkers.constants import WHITE, WIDTH, HEIGHT, SQUARE_SIZE, RED
from checkers.game import Game
from minimax.algorithm import minimax, minimax_AB

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")

#takes position of mouse returns what row and col we are in
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y//SQUARE_SIZE
    col = x//SQUARE_SIZE

    return row, col
    

def main():
    pygame.init()
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            #value, new_board = minimax(game.get_board(), 3, True, game)
            value, new_board = minimax_AB(game.get_board(), 3, float('-inf'), float('inf'), True, game)
            if new_board == None:
                game.winner_display("Red")
                run = False
                break
            game.ai_move(new_board)

        #bad styling!
        winner = game.winner()
        if  winner != None:
            game.winner_display(winner)
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                #if game.turn == RED:
                game.select(row, col)

        game.update()
           
        
    pygame.quit()

main()