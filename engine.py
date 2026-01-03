import copy
import pickle
from piece import Piece

class CheckersEngine:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.turn = 'W'
        self.move_history = []
        self.must_jump_piece = None
        self.setup_board()


    #tabla
    def setup_board(self):
        for r in range(8):
            for c in range(8):
                if (r + c) % 2 != 0:
                    if r < 3: self.board[r][c] = Piece('B', r, c)
                    elif r > 4: self.board[r][c] = Piece('W', r, c)


    #directiile posibile in functie de tipul piesei, considerand ca albele sunt jos si negrele sus
    def get_directions(self, piece):
        if piece.king:
            return [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        if piece.color == 'W':
            return [(-1, 1), (-1, -1)]
        else: return [(1, 1), (1, -1)]


    #afisare in consola
    def display(self):
        print("  0 1 2 3 4 5 6 7")
        for i, row in enumerate(self.board):
            row_str = f"{i} " + " ".join([str(p) if p else "_" for p in row])
            print(row_str)
        print(f"\nTurn: {self.turn}")


    #analiza miscarilor posibile
    def get_legal_moves(self):
        # saritura multipla (nu ai voie sa te opresti pana nu faci toate sariturile)
        if self.must_jump_piece:
            return self.get_piece_jumps(self.must_jump_piece)
        
        all_jumps = self.get_all_jumps()
        if all_jumps:
            return all_jumps
        
        all_slides = []
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece.color == self.turn:
                    all_slides.extend(self.get_piece_slides(piece))
        return all_slides
    

    #pasi posibili (dreapta/stanga pe diagonala)
    def get_piece_slides(self, piece):
        slides = []
        directions = self.get_directions(piece)
        for dr, dc in directions:
            nr, nc = piece.row + dr, piece.col + dc
            if 0 <= nr < 8 and 0 <= nc < 8 and self.board[nr][nc] is None:
                slides.append(((piece.row, piece.col), (nr, nc)))
        return slides

    #sariturile posibile
    def get_all_jumps(self):
        jumps = []
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece.color == self.turn:
                    piece_jumps = self.get_piece_jumps(piece)
                    if piece_jumps:
                        jumps.extend(piece_jumps)
        return jumps

    def get_piece_jumps(self, piece):
        jumps = []
        directions = self.get_directions(piece)
        for dr, dc in directions:
            mid_r, mid_c = piece.row + dr, piece.col + dc
            end_r, end_c = piece.row + (dr * 2), piece.col + (dc * 2)
            
            if 0 <= end_r < 8 and 0 <= end_c < 8:
                mid_piece = self.board[mid_r][mid_c]
                if mid_piece and mid_piece.color != piece.color and self.board[end_r][end_c] is None:
                    jumps.append(((piece.row, piece.col), (end_r, end_c), (mid_r, mid_c)))
        return jumps


    #miscarea propriu-zisa
    def make_move(self, start, end):
        legal_moves = self.get_legal_moves()
        move = next((m for m in legal_moves if m[0] == start and m[1] == end), None)

        if not move:
            return False

        r1, c1 = start
        r2, c2 = end
        piece = self.board[r1][c1]
        
        # mutare
        self.board[r2][c2] = piece
        self.board[r1][c1] = None
        piece.row, piece.col = r2, c2

        #verificare daca o piesa este "mancata" de adversar
        if len(move) == 3:
            mid_r, mid_c = move[2]
            self.board[mid_r][mid_c] = None
            
            # verificare daca se mai poate sari o data cu aceeasi piesa
            if self.get_piece_jumps(piece):
                self.must_jump_piece = piece
                self.move_history.append(move)
                return True 

        # promovare King
        if (piece.color == 'W' and r2 == 0) or (piece.color == 'B' and r2 == 7):
            piece.promote()

        self.move_history.append(move)
        self.must_jump_piece = None
        self.turn = 'B' if self.turn == 'W' else 'W'
        return True
    

    def is_game_over(self):
       return len(self.get_all_valid_moves('W')) == 0 or len(self.get_all_valid_moves('B')) == 0
    

    def check_winner(self):
        white_moves = self.get_all_valid_moves('W')
        black_moves = self.get_all_valid_moves('B')

        if not white_moves:
            return 'B'
        if not black_moves:
            return 'W'
            
        return None
    

    #pentru AI
    def evaluate(self):
        score = 0
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece:
                    value = 10 + (2 if piece.king else 0) # King valorează mai mult
                    if piece.color == 'W':
                        score += value
                    else:
                        score -= value
        return score

    def get_all_valid_moves(self, color): #toate posibilitatile pentru o culoare
        temp_turn = self.turn
        self.turn = color
        moves = self.get_legal_moves()
        self.turn = temp_turn
        return moves

    def simulate_move(self, start, end): #face miscare intr-o simulare (copie)
        clone = copy.deepcopy(self)
        clone.make_move(start, end)
        return clone
    

    #pentru save/load
    def save_game(self, filename="savegame.dat"):
        try:
            with open(filename, "wb") as f:
                pickle.dump(self, f)
            print("Joc salvat cu succes!")
        except Exception as e:
            print(f"Eroare la salvare: {e}")

    @staticmethod
    def load_game(filename="savegame.dat"):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            print("Nu s-a găsit nicio salvare.")
            return None