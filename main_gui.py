import pygame
import copy
from engine import CheckersEngine
from constants import *
from ai import minimax

class CheckersGUI:
    def __init__(self, win):
        self.win = win
        self.game = CheckersEngine()
        self.selected_pos = None
        self.valid_moves = []
        self.game_mode = None
        self.history = []


    def draw_menu(self):
        self.win.fill(BLACK)
        font = pygame.font.SysFont('Arial', 40)
        txt = font.render("Alege modul de joc:", True, WHITE)
        txt_pvp = font.render("1. Jucător vs Jucător", True, WHITE)
        txt_ai = font.render("2. Jucător vs AI", True, WHITE)
        self.win.blit(txt, (WIDTH//2 - 150, HEIGHT//2 - 150))
        self.win.blit(txt_pvp, (WIDTH//2 - 150, HEIGHT//2 - 50))
        self.win.blit(txt_ai, (WIDTH//2 - 150, HEIGHT//2 + 50))
        pygame.display.update()


    def update(self):
        if self.game_mode == 'AI' and self.game.turn == 'B':
            pygame.time.delay(500) 
            _, move = minimax(self.game, 3, -float('inf'), float('inf'), False)
            if move:
                self.game.make_move(move[0], move[1])
            
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
            self.save_state_to_history()
            self.game.make_move(self.selected_pos, (row, col))
            self.selected_pos = None
            self.valid_moves = []
        else:
            piece = self.game.board[row][col]
            if piece and piece.color == self.game.turn:
                self.selected_pos = (row, col)
                all_moves = self.game.get_legal_moves()
                self.valid_moves = [m for m in all_moves if m[0] == (row, col)]


    def draw_winner_message(self, winner):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 150), [0, 0, WIDTH, HEIGHT])
        self.win.blit(overlay, (0, 0))

        font = pygame.font.SysFont('Arial', 50, bold=True)
        color_name = "ALB" if winner == 'W' else "NEGRU"
        text = font.render(f"Jucătorul {color_name} a câștigat!", True, GOLD)
        
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.win.blit(text, text_rect)
        
        small_font = pygame.font.SysFont('Arial', 20)
        restart_text = small_font.render("Apasă R pentru a juca din nou", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        self.win.blit(restart_text, restart_rect)

    def save_state_to_history(self):
        self.history.append(copy.deepcopy(self.game))
        if len(self.history) > 7:
            self.history.pop(0)

    def undo_move(self):
        if self.history:
            self.game = self.history.pop()
            self.selected_pos = None
            self.valid_moves = []
            print("Undo realizat.")



def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('DAME/CHECKERS - Proiect Python 2025 - Cucu Veronica')
    
    gui = CheckersGUI(win)

    menu = True
    while menu:
        gui.draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    gui.game_mode = 'PVP'
                    menu = False
                if event.key == pygame.K_2:
                    gui.game_mode = 'AI'
                    menu = False
    
    clock = pygame.time.Clock()
    run = True
    winner = None

    while run:
        clock.tick(60)
        if not winner:
            winner = gui.game.check_winner()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not winner:
                gui.handle_click(pygame.mouse.get_pos())
            
            if event.type == pygame.KEYDOWN:
                # R - Restart
                if event.key == pygame.K_r:
                    main()
                    return
                
                # U - Undo
                if event.key == pygame.K_u and not winner:
                    gui.undo_move()

                # S - Save
                if event.key == pygame.K_s:
                    gui.game.save_game()

                # L - Load
                if event.key == pygame.K_l:
                    loaded_game = CheckersEngine.load_game()
                    if loaded_game:
                        gui.game = loaded_game
                        gui.history = []
                        winner = None
        
        gui.update()
        if winner:
            gui.draw_winner_message(winner)
            pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()