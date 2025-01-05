import pygame
import sys
import random
import Utils
from Board import Board
from Menu import Menu
from Cell import Cell
from constants import letters, letter_scores, special_tiles
import tkinter as tk
from tkinter import messagebox

class Game:
    def __init__(self, dictionary_path):
        self.dictionary_path = dictionary_path
        self.board_size = 15
        self.cell_size = 45
        self.margin = 3
        self.menu_height = 80
        self.score_menu = 300
        self.screen_size = self.board_size * (self.cell_size + self.margin) + self.margin
        print("BOARD SIZE: ", self.screen_size)

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_size + self.score_menu, self.screen_size + self.menu_height))
        pygame.display.set_caption("Scrabble with Drag-and-Drop")
        self.font = pygame.font.Font(None, 36)
        self.score_font = pygame.font.Font(None, 20)

        self.board = Board(self.board_size, self.cell_size, self.margin)
        self.menu = Menu(self.screen_size, self.cell_size, self.margin, self.menu_height, dictionary_path, self)

        self.dragged_letter = None
        self.dragged_letter_offset = (0, 0)
        self.dragged_letter_pos = None
        self.letter_from_board = None
        self.locked_letters = set()
        self.total_score = 0
        self.words = []
        self.current_iteration_words = []
        self.iteration = 0
        self.board_matrix = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.previous_placed_letters = set()

    def run(self):
        while True:
            self.screen.fill(Utils.hex_to_rgb('#1a1b21'))
            self.board.draw(self.screen, self.font, self.score_font)
            self.menu.draw(self.screen, self.font, self.score_font)
            self.draw_score()

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

    def validate_new_word(self):
        if not self.current_iteration_words:
            return False, "No new word added"

        for word in self.current_iteration_words:
            word_str = ''.join([letter for letter, _ in word])
            if word_str not in self.menu.dictionary:
                return False, word_str
        return True, None

    def handle_mouse_button_down(self, event):
        mouse_x, mouse_y = event.pos

        button_action = self.menu.handle_button_click(event.pos)
        if button_action == "submit":
            self.find_word()  # Ensure words are found before validation
            valid, invalid_word = self.validate_new_word()
            if not valid:
                root = tk.Tk()
                root.withdraw()  # Hide the root window
                messagebox.showerror("Error", f"The word '{invalid_word}' is not in the dictionary.")
                root.destroy()
                return
            if not self.board.placed_letters or self.board.placed_letters.keys() == self.previous_placed_letters:
                root = tk.Tk()
                root.withdraw()  # Hide the root window
                messagebox.showerror("Error", "No new words have been added.")
                root.destroy()
                return
            self.previous_placed_letters = set(self.board.placed_letters.keys())
            self.locked_letters.update(self.board.placed_letters.keys())
            if self.iteration > 0 and not self.check_words_connected():
                root = tk.Tk()
                root.withdraw()  # Hide the root window
                messagebox.showerror("Error", "Words are not connected!")
                root.destroy()
                self.locked_letters.difference_update(self.board.placed_letters.keys())
                return
            self.calculate_score()
            self.iteration += 1
            self.print_board_matrix()  # Print the matrix after submitting
            for word in self.current_iteration_words:
                print(f"Word added: {''.join([letter for letter, _ in word])}")
            self.menu.replace_letters()  # Generate new letters only when words are connected
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

            if 0 <= row < self.board_size and 0 <= col < self.board_size and not self.board_matrix[row][col]:
                if self.letter_from_board:
                    self.board_matrix[self.letter_from_board[0]][self.letter_from_board[1]] = None  # Remove letter from previous position
                self.board.placed_letters[(row, col)] = self.dragged_letter
                self.board.cell_colors[(row, col)] = Utils.hex_to_rgb('#b79d9b')
                self.board_matrix[row][col] = (self.dragged_letter, self.iteration)
                self.print_board_matrix()  # Print the matrix after placing a letter
            else:
                if self.letter_from_board:
                    self.board_matrix[self.letter_from_board[0]][self.letter_from_board[1]] = None  # Remove letter from previous position
                    self.menu.menu_letters.append(self.dragged_letter)
                else:
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

    def calculate_score(self):
        score = 0
        for word in self.current_iteration_words:
            word_score = 0
            word_multiplier = 1
            for letter, (row, col) in word:
                letter_score = letter_scores[letter]
                if (row, col) in special_tiles:
                    tile_type = special_tiles[(row, col)]
                    if tile_type == 'DL':
                        letter_score *= 2
                    elif tile_type == 'TL':
                        letter_score *= 3
                    elif tile_type == 'DW':
                        word_multiplier *= 2
                    elif tile_type == 'TW':
                        word_multiplier *= 3
                word_score += letter_score
            word_score *= word_multiplier
            score += word_score
        self.total_score += score
        print(f"Score for this turn: {score}")
        print(f"Total score: {self.total_score}")

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.total_score}", True, (255, 255, 255))
        self.screen.blit(score_text, (self.screen_size + 20, 20))

        # Draw special tiles information
        special_tile_info = {
            'DL': ('Double Letter', Utils.hex_to_rgb('#92a1c2')),
            'TL': ('Triple Letter', Utils.hex_to_rgb('3f5b8d')),
            'DW': ('Double Word', Utils.hex_to_rgb('#a2869c')),
            'TW': ('Triple Word', Utils.hex_to_rgb('#6B597F'))
        }

        y_offset = self.screen_size - 160
        for tile_type, (description, color) in special_tile_info.items():
            pygame.draw.rect(self.screen, color, (self.screen_size + 20, y_offset, 100, 30))
            tile_text = self.score_font.render(f"{tile_type}: {description}", True, Utils.hex_to_rgb('#d9d9d9'))
            self.screen.blit(tile_text, (self.screen_size + 130, y_offset + 5))
            y_offset += 40

    def find_word(self):
        checked_positions = set()
        self.words = []
        self.current_iteration_words = []

        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board_matrix[row][col] and (row, col) not in checked_positions:
                    # Check horizontal word
                    word = []
                    start_col = col
                    while start_col > 0 and self.board_matrix[row][start_col - 1]:
                        start_col -= 1
                    while start_col < self.board_size and self.board_matrix[row][start_col]:
                        word.append((self.board_matrix[row][start_col][0], (row, start_col)))
                        checked_positions.add((row, start_col))
                        start_col += 1

                    if len(word) > 1:
                        self.words.append((word, 'horizontal'))
                        if any(self.board_matrix[row][col][1] == self.iteration for _, (row, col) in word):
                            self.current_iteration_words.append(word)
                        print(f"Found horizontal word: {''.join([letter for letter, _ in word])}")

                    # Check vertical word
                    word = []
                    start_row = row
                    while start_row > 0 and self.board_matrix[start_row - 1][col]:
                        start_row -= 1
                    while start_row < self.board_size and self.board_matrix[start_row][col]:
                        word.append((self.board_matrix[start_row][col][0], (start_row, col)))
                        checked_positions.add((start_row, col))
                        start_row += 1

                    if len(word) > 1:
                        self.words.append((word, 'vertical'))
                        if any(self.board_matrix[row][col][1] == self.iteration for _, (row, col) in word):
                            self.current_iteration_words.append(word)
                        print(f"Found vertical word: {''.join([letter for letter, _ in word])}")

    def check_words_connected(self):
        if not self.words:
            return False

        for word, _ in self.words:
            for _, (row, col) in word:
                if self.board_matrix[row][col][1] == self.iteration:
                    # Check adjacent cells for letters from previous iterations
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        adj_row, adj_col = row + dr, col + dc
                        if 0 <= adj_row < self.board_size and 0 <= adj_col < self.board_size:
                            if self.board_matrix[adj_row][adj_col] and self.board_matrix[adj_row][adj_col][1] < self.iteration:
                                return True
        return False

    def print_board_matrix(self):
        for row in self.board_matrix:
            print([f"{cell[0]}({cell[1]})" if cell else "None" for cell in row])

    def validate_words(self):
        for word, _ in self.words:
            word_str = ''.join([letter for letter, _ in word])
            if word_str not in self.menu.dictionary:
                return False, word_str
        return True, None