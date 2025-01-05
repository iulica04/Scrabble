import random
import Utils
from constants import letter_scores, special_tiles
import tkinter as tk
from tkinter import messagebox

class Opponent:
    """
    Represents the opponent player in the Scrabble game.

    Attributes:
        game (Game): The game instance.
        total_score (int): The total score of the opponent.
    """

    def __init__(self, game):
        """
        Initializes the Opponent with the given game instance.

        Args:
            game (Game): The game instance.
        """
        self.game = game
        self.total_score = 0

    def make_move(self):
        """
        Makes a move for the opponent by finding and placing a valid word.
        """
        possible_words = self.find_possible_words()
        if not possible_words:
            print("Opponent cannot make a move.")
            self.game.end_game()
            return

        word, position, direction = random.choice(possible_words)
        placed_word = self.place_word(word, position, direction)
        self.calculate_score(placed_word)
        self.game.iteration += 1
        self.game.print_board_matrix()

    def find_possible_words(self):
        """
        Finds all possible words that the opponent can place on the board.

        Returns:
            list: A list of tuples containing the word, position, and direction.
        """
        possible_words = []
        for word in self.game.menu.dictionary:
            positions = self.find_positions_for_word(word)
            for position, direction in positions:
                if self.is_valid_placement(word, position, direction):
                    possible_words.append((word, position, direction))
        return possible_words

    def find_positions_for_word(self, word):
        """
        Finds all possible positions for a given word on the board.

        Args:
            word (str): The word to find positions for.

        Returns:
            list: A list of tuples containing the position and direction.
        """
        positions = []
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                if self.can_place_word(word, (row, col), 'horizontal'):
                    positions.append(((row, col), 'horizontal'))
                if self.can_place_word(word, (row, col), 'vertical'):
                    positions.append(((row, col), 'vertical'))
        return positions

    def can_place_word(self, word, position, direction):
        """
        Checks if a word can be placed at a given position and direction.

        Args:
            word (str): The word to place.
            position (tuple): The position to place the word.
            direction (str): The direction to place the word ('horizontal' or 'vertical').

        Returns:
            bool: True if the word can be placed, False otherwise.
        """
        row, col = position
        if direction == 'horizontal':
            if col + len(word) > self.game.board_size:
                return False
            for i in range(len(word)):
                current_cell = self.game.board_matrix[row][col + i]
                if current_cell is not None and current_cell[0] != word[i]:
                    return False
            return True
        elif direction == 'vertical':
            if row + len(word) > self.game.board_size:
                return False
            for i in range(len(word)):
                current_cell = self.game.board_matrix[row + i][col]
                if current_cell is not None and current_cell[0] != word[i]:
                    return False
            return True
        return False

    def is_valid_placement(self, word, position, direction):
        """
        Checks if a word placement is valid by ensuring it is connected to existing words.

        Args:
            word (str): The word to place.
            position (tuple): The position to place the word.
            direction (str): The direction to place the word ('horizontal' or 'vertical').

        Returns:
            bool: True if the placement is valid, False otherwise.
        """
        row, col = position
        connected = False

        if direction == 'horizontal':
            for i in range(len(word)):
                current_cell = self.game.board_matrix[row][col + i]
                if current_cell is not None:
                    connected = True
                if (
                    (row > 0 and self.game.board_matrix[row - 1][col + i] is not None) or
                    (row < self.game.board_size - 1 and self.game.board_matrix[row + 1][col + i] is not None)
                ):
                    connected = True
                if current_cell is None and (
                    (row > 0 and self.game.board_matrix[row - 1][col + i] is not None) or
                    (row < self.game.board_size - 1 and self.game.board_matrix[row + 1][col + i] is not None)
                ):
                    return False
            if (col > 0 and self.game.board_matrix[row][col - 1] is not None) or \
               (col + len(word) < self.game.board_size and self.game.board_matrix[row][col + len(word)] is not None):
                return False
        elif direction == 'vertical':
            for i in range(len(word)):
                current_cell = self.game.board_matrix[row + i][col]
                if current_cell is not None:
                    connected = True
                if (
                    (col > 0 and self.game.board_matrix[row + i][col - 1] is not None) or
                    (col < self.game.board_size - 1 and self.game.board_matrix[row + i][col + 1] is not None)
                ):
                    connected = True
                if current_cell is None and (
                    (col > 0 and self.game.board_matrix[row + i][col - 1] is not None) or
                    (col < self.game.board_size - 1 and self.game.board_matrix[row + i][col + 1] is not None)
                ):
                    return False
            if (row > 0 and self.game.board_matrix[row - 1][col] is not None) or \
               (row + len(word) < self.game.board_size and self.game.board_matrix[row + len(word)][col] is not None):
                return False

        return connected

    def place_word(self, word, position, direction):
        """
        Places a word on the board at the given position and direction.

        Args:
            word (str): The word to place.
            position (tuple): The position to place the word.
            direction (str): The direction to place the word ('horizontal' or 'vertical').

        Returns:
            list: A list of tuples containing the letter and its position.
        """
        row, col = position
        placed_word = []
        if direction == 'horizontal':
            for i in range(len(word)):
                self.game.board_matrix[row][col + i] = (word[i], self.game.iteration)
                self.game.board.placed_letters[(row, col + i)] = word[i]
                self.game.board.cell_colors[(row, col + i)] = Utils.hex_to_rgb('#b79d9b')
                placed_word.append((word[i], (row, col + i)))
        elif direction == 'vertical':
            for i in range(len(word)):
                self.game.board_matrix[row + i][col] = (word[i], self.game.iteration)
                self.game.board.placed_letters[(row + i, col)] = word[i]
                self.game.board.cell_colors[(row + i, col)] = Utils.hex_to_rgb('#b79d9b')
                placed_word.append((word[i], (row + i, col)))
        return placed_word

    def calculate_score(self, word):
        """
        Calculates the score for the placed word and updates the opponent's total score.

        Args:
            word (list): A list of tuples containing the letter and its position.
        """
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
        self.total_score += word_score
        print(f"Opponent score for this turn: {word_score}")
        print(f"Opponent total score: {self.total_score}")