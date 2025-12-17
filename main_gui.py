import pygame
from engine import CheckersEngine
from constants import *

class CheckersGUI:
    def __init__(self, win):
        self.win = win
        self.game = CheckersEngine()
        self.selected_pos = None
        self.valid_moves = []

    def update(self):
        self.draw_board()
        self.draw_pieces()
        self.highlight_moves()
        pygame.display.update()

    def draw_board(self):
        self.win.fill(BLACK)
        for r in range(ROWS):
            for c in range((r % 2), COLS, 2):
                pygame.draw.rect(self.win, GREY, (r * SQUARE_SIZE, c * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self):
        for r in range(ROWS):
            for c in range(COLS):
                piece = self.game.board[r][c]
                if piece:
                    color = WHITE if piece.color == 'W' else RED
                    center = (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2)
                    pygame.draw.circle(self.win, color, center, SQUARE_SIZE // 2 - 10)
                    
                    if piece.king:
                        pygame.draw.circle(self.win, GOLD, center, SQUARE_SIZE // 4)

    def highlight_moves(self):
        if self.selected_pos:
            for move in self.valid_moves:
                _, (r, c) = move[0], move[1]
                center = (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2)
                pygame.draw.circle(self.win, BLUE, center, 15)

    def handle_click(self, pos):
        x, y = pos
        row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
        
        move = next((m for m in self.valid_moves if m[1] == (row, col)), None)
        
        if move:
            self.game.make_move(self.selected_pos, (row, col))
            self.selected_pos = None
            self.valid_moves = []
        else:
            piece = self.game.board[row][col]
            if piece and piece.color == self.game.turn:
                self.selected_pos = (row, col)
                all_moves = self.game.get_legal_moves()
                self.valid_moves = [m for m in all_moves if m[0] == (row, col)]



def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('DAME/CHECKERS - Proiect Python 2025 - Cucu Veronica')
    
    gui = CheckersGUI(win)
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                gui.handle_click(pygame.mouse.get_pos())
        
        gui.update()

    pygame.quit()

if __name__ == "__main__":
    main()