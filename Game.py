import pygame
import sys
import random
import Utils
from Board import Board
from Menu import Menu
from Cell import Cell
from constants import letters, letter_scores

class Game:
    def __init__(self):
        self.board_size = 15
        self.cell_size = 45
        self.margin = 3
        self.menu_height = 80
        self.screen_size = self.board_size * (self.cell_size + self.margin) + self.margin
        print("BOARD SIZE: ", self.screen_size)

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size + self.menu_height))
        pygame.display.set_caption("Scrabble with Drag-and-Drop")
        self.font = pygame.font.Font(None, 36)
        self.score_font = pygame.font.Font(None, 20)

        self.board = Board(self.board_size, self.cell_size, self.margin)
        self.menu = Menu(self.screen_size, self.cell_size, self.margin, self.menu_height)

        self.dragged_letter = None
        self.dragged_letter_offset = (0, 0)
        self.dragged_letter_pos = None
        self.letter_from_board = None
        self.locked_letters = set()

    def run(self):
        while True:
            self.screen.fill(Utils.hex_to_rgb('#1a1b21'))

            self.board.draw(self.screen, self.font, self.score_font)
            self.menu.draw(self.screen, self.font, self.score_font)

            if self.dragged_letter:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                Utils.draw_rounded_rect(self.screen, Utils.hex_to_rgb('#b79d9b'), (
                    mouse_x - self.dragged_letter_offset[0], mouse_y - self.dragged_letter_offset[1], self.cell_size, self.cell_size),
                    corner_radius=8)
                letter_text = self.font.render(self.dragged_letter, True, (255, 255, 255))
                self.screen.blit(letter_text, (mouse_x - self.dragged_letter_offset[0] + (self.cell_size - letter_text.get_width()) // 2,
                                               mouse_y - self.dragged_letter_offset[1] + (self.cell_size - letter_text.get_height()) // 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_button_down(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_mouse_button_up(event)

            pygame.display.flip()

    def handle_mouse_button_down(self, event):
        mouse_x, mouse_y = event.pos

        button_action = self.menu.handle_button_click(event.pos)
        if button_action == "submit":
            self.locked_letters.update(self.board.placed_letters.keys())
        elif button_action == "shuffle":
            self.menu.shuffle_letters()
            return

        for i, (letter, pos) in enumerate(zip(self.menu.menu_letters, self.menu.menu_letter_positions)):
            x, y = pos
            if x <= mouse_x <= x + self.cell_size and y <= mouse_y <= y + self.cell_size:
                self.dragged_letter = letter
                self.dragged_letter_pos = (x, y)
                self.dragged_letter_offset = (mouse_x - x, mouse_y - y)
                self.menu.menu_letters.pop(i)
                self.menu.menu_letter_positions.pop(i)
                return

        for (row, col), letter in list(self.board.placed_letters.items()):
            if (row, col) in self.locked_letters:
                continue
            x = self.margin + col * (self.cell_size + self.margin)
            y = self.margin + row * (self.cell_size + self.margin)
            if x <= mouse_x <= x + self.cell_size and y <= mouse_y <= y + self.cell_size:
                self.dragged_letter = letter
                self.dragged_letter_pos = (x, y)
                self.dragged_letter_offset = (mouse_x - x, mouse_y - y)
                self.letter_from_board = (row, col)
                del self.board.placed_letters[(row, col)]
                self.board.cell_colors[(row, col)] = Cell.get_cell_color(row, col)
                return

    def handle_mouse_button_up(self, event):
        if self.dragged_letter:
            mouse_x, mouse_y = event.pos
            col = (mouse_x - self.margin) // (self.cell_size + self.margin)
            row = (mouse_y - self.margin) // (self.cell_size + self.margin)

            if 0 <= row < self.board_size and 0 <= col < self.board_size:
                self.board.placed_letters[(row, col)] = self.dragged_letter
                self.board.cell_colors[(row, col)] = Utils.hex_to_rgb('#b79d9b')
            else:
                if self.letter_from_board:
                    self.board.cell_colors[(row, col)] = Cell.get_cell_color(self.letter_from_board[0], self.letter_from_board[1])

                self.menu.menu_letters.append(self.dragged_letter)
                total_menu_width = len(self.menu.menu_letters) * (self.cell_size + self.margin * 2) - self.margin * 2
                start_x = (self.screen_size - total_menu_width) // 2
                self.menu.menu_letter_positions = [
                    (start_x + i * (self.cell_size + self.margin * 2), self.screen_size + (self.menu_height - self.cell_size) // 2)
                    for i in range(len(self.menu.menu_letters))
                ]

            self.dragged_letter = None
            self.dragged_letter_pos = None
            self.dragged_letter_offset = (0, 0)
            self.letter_from_board = None