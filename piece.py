class Piece:
    def __init__(self, color, row, col):
        self.color = color  # 'W' sau 'B'
        self.row = row
        self.col = col
        self.king = False

    def promote(self):
        self.king = True

    def __repr__(self):
        char = self.color
        return f"{char}K" if self.king else f"{char} "