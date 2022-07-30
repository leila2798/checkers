import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE, WIDTH, HEIGHT 
from .board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win =win
    
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}


    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
   
    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None 
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)

            self.change_turn()
        else:
            return False
        return True

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def draw_valid_moves(self, moves):
        #looping through the keys of the dictionary, which are tuples representing position
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row* SQUARE_SIZE + SQUARE_SIZE //2), 15)

    def winner(self):
        if self.turn == RED:
            red_pieces = self.board.get_all_pieces(RED)
            lost_game = True
            for piece in red_pieces:
                if len(self.board.get_valid_moves(piece)) >0:
                    lost_game = False
                    break
            if lost_game:
                return "WHITE"
        return self.board.winner() 

    def get_board(self):
        return self.board

    def ai_move(self, new_board):
        self.board = new_board
        self.change_turn()

    def winner_display(self, color):
        self.win.fill(WHITE)
        font = pygame.font.SysFont("Arial", 50)
        text = font.render("The winner is " + color, True, RED)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.win.blit(text, text_rect)
        pygame.display.flip()
        pygame.event.pump()
        pygame.time.delay(5 * 1000)

