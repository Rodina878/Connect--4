
import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import math
from copy import deepcopy
ROWS = 6
COLS = 7
EMPTY = 0
PLAYER_PIECE = 1  # Blue (human)
AI_PIECE = -1     # Red (AI)

CELL_SIZE = 90
PADDING = 8

DISPLAY = {
    EMPTY: " ",
    PLAYER_PIECE: "🔵",
    AI_PIECE: "🔴"
}

class Board:
    def _init_(self):
        self.grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

    def reset(self):
        self.grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

    def copy(self):
        b = Board()
        b.grid = deepcopy(self.grid)
        return b

    def print(self):
        letters = "    " + "   ".join(str(i) for i in range(COLS)) + "   \n    " + "   ".join(chr(ord('A')+i) for i in range(COLS))
        print("\n" + letters)
        print("  +" + "---+"*COLS)
        for r in range(ROWS):
            row_display = "|".join(f" {DISPLAY[self.grid[r][c]]} " for c in range(COLS))
            print(f"{r} |{row_display}|")
            print("  +" + "---+"*COLS)

    def is_valid_location(self, col):
        return 0 <= col < COLS and self.grid[0][col] == EMPTY

    def get_next_open_row(self, col):
        for r in range(ROWS-1, -1, -1):
            if self.grid[r][col] == EMPTY:
                return r
        return None

    def drop_piece(self, col, piece):
        row = self.get_next_open_row(col)
        if row is None:
            raise ValueError("Column is full")
        self.grid[row][col] = piece
        return (row, col)

    def undo_move(self, col):
        for r in range(ROWS):
            if self.grid[r][col] != EMPTY:
                self.grid[r][col] = EMPTY
                return

    def get_valid_locations(self):
        return [c for c in range(COLS) if self.is_valid_location(c)]

    def is_full(self):
        return all(self.grid[0][c] != EMPTY for c in range(COLS))

    def winning_move(self, piece):
        b = self.grid
        # horizontal
        for r in range(ROWS):
            for c in range(COLS-3):
                if all(b[r][c+i] == piece for i in range(4)):
                    return True
        # vertical
        for c in range(COLS):
            for r in range(ROWS-3):
                if all(b[r+i][c] == piece for i in range(4)):
                    return True
        # positive diagonal (down-right)
        for r in range(ROWS-3):
            for c in range(COLS-3):
                if all(b[r+i][c+i] == piece for i in range(4)):
                    return True
        # negative diagonal (down-left)
        for r in range(ROWS-3):
            for c in range(3, COLS):
                if all(b[r+i][c-i] == piece for i in range(4)):
                    return True
        return False

    # Heuristic helpers
    def _evaluate_window(self, window, piece):
        score = 0
        opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
        count_piece = window.count(piece)
        count_empty = window.count(EMPTY)
        count_opp = window.count(opp_piece)

        if count_piece == 4:
            score += 1000
        elif count_piece == 3 and count_empty == 1:
            score += 50
        elif count_piece == 2 and count_empty == 2:
            score += 10

        if count_opp == 3 and count_empty == 1:
            score -= 80

        return score
       def score_position(self, piece):
        score = 0
        b = self.grid

        center_col = COLS // 2
        center_count = [b[r][center_col] for r in range(ROWS)].count(piece)
        score += center_count * 6

        # horizontal
        for r in range(ROWS):
            row_array = [b[r][c] for c in range(COLS)]
            for c in range(COLS-3):
                window = row_array[c:c+4]
                score += self._evaluate_window(window, piece)

        for c in range(COLS):
            col_array = [b[r][c] for r in range(ROWS)]
            for r in range(ROWS-3):
                window = col_array[r:r+4]
                score += self._evaluate_window(window, piece)

        for r in range(ROWS-3):
            for c in range(COLS-3):
                window = [b[r+i][c+i] for i in range(4)]
                score += self._evaluate_window(window, piece)

        for r in range(ROWS-3):
            for c in range(COLS-3):
                window = [b[r+3-i][c+i] for i in range(4)]
                score += self._evaluate_window(window, piece)

        return score
    
        def score_position(self, piece):
        score = 0
        b = self.grid

        center_col = COLS // 2
        center_count = [b[r][center_col] for r in range(ROWS)].count(piece)
        score += center_count * 6

        # horizontal
        for r in range(ROWS):
            row_array = [b[r][c] for c in range(COLS)]
            for c in range(COLS-3):
                window = row_array[c:c+4]
                score += self._evaluate_window(window, piece)

        for c in range(COLS):
            col_array = [b[r][c] for r in range(ROWS)]
            for r in range(ROWS-3):
                window = col_array[r:r+4]
                score += self._evaluate_window(window, piece)

        for r in range(ROWS-3):
            for c in range(COLS-3):
                window = [b[r+i][c+i] for i in range(4)]
                score += self._evaluate_window(window, piece)

        for r in range(ROWS-3):
            for c in range(COLS-3):
                window = [b[r+3-i][c+i] for i in range(4)]
                score += self._evaluate_window(window, piece)

        return score
    
    class AI:
    def  _init_(self, depth=4):
        self.depth = max(1, min(depth, 6))

    def minimax(self, board: Board, depth, alpha, beta, maximizingPlayer):
        valid_locations = board.get_valid_locations()
        is_terminal = board.winning_move(PLAYER_PIECE) or board.winning_move(AI_PIECE) or board.is_full()

        if depth == 0 or is_terminal:
            if is_terminal:
                if board.winning_move(AI_PIECE):
                    return (None, 10**6)
                elif board.winning_move(PLAYER_PIECE):
                    return (None, -10**6)
                else:  # draw
                    return (None, 0)
            else:
                return (None, board.score_position(AI_PIECE))

        if maximizingPlayer:
            value = -math.inf
            best_col = random.choice(valid_locations) if valid_locations else None
            for col in valid_locations:
                board.drop_piece(col, AI_PIECE)
                new_score = self.minimax(board, depth-1, alpha, beta, False)[1]
                board.undo_move(col)
                if new_score > value:
                    value = new_score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_col, value
        else:
            value = math.inf
            best_col = random.choice(valid_locations) if valid_locations else None
            for col in valid_locations:
                board.drop_piece(col, PLAYER_PIECE)
                new_score = self.minimax(board, depth-1, alpha, beta, True)[1]
                board.undo_move(col)
                if new_score < value:
                    value = new_score
                    best_col = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_col, value

    def pick_best_move(self, board: Board):
        col, score = self.minimax(board, self.depth, -math.inf, math.inf, True)
        return col


