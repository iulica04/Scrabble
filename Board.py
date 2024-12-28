import pygame
import Utils
from Cell import Cell
from constants import letter_scores

class Board:
    def __init__(self, board_size, cell_size, margin):
        self.board_size = board_size
        self.cell_size = cell_size
        self.margin = margin
        self.placed_letters = {}
        self.cell_colors = {}
        self.piece_color = Utils.hex_to_rgb('#b79d9b')

        for row in range(self.board_size):
            for col in range(self.board_size):
                self.cell_colors[(row, col)] = Cell.get_cell_color(row, col)

    def draw(self, screen, font, score_font):
        for row in range(self.board_size):
            for col in range(self.board_size):
                x = self.margin + col * (self.cell_size + self.margin)
                y = self.margin + row * (self.cell_size + self.margin)

                Utils.draw_rounded_rect(screen, self.cell_colors[(row, col)], (x, y, self.cell_size, self.cell_size), corner_radius=8)

                if (row, col) in self.placed_letters:
                    letter = self.placed_letters[(row, col)]
                    letter_text = font.render(letter, True, (0, 0, 0))
                    screen.blit(letter_text, (
                        x + (self.cell_size - letter_text.get_width()) // 2, y + (self.cell_size - letter_text.get_height()) // 2))

                    letter_score = letter_scores[letter]
                    score_text = score_font.render(str(letter_score), True, (0, 0, 0))
                    score_x = x + self.cell_size - score_text.get_width() - 5
                    score_y = y + self.cell_size - score_text.get_height() - 5
                    screen.blit(score_text, (score_x, score_y))