import random
import Utils

class Opponent:
    def __init__(self, game):
        self.game = game

    def make_move(self):
        possible_words = self.find_possible_words()
        if not possible_words:
            print("Opponent cannot make a move.")
            return

        word, position, direction = random.choice(possible_words)
        self.place_word(word, position, direction)
        self.game.calculate_score()
        self.game.iteration += 1
        self.game.print_board_matrix()

    def find_possible_words(self):
        possible_words = []
        for word in self.game.menu.dictionary:
            positions = self.find_positions_for_word(word)
            for position, direction in positions:
                if self.is_valid_placement(word, position, direction):
                    possible_words.append((word, position, direction))
        return possible_words

    def find_positions_for_word(self, word):
        positions = []
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                if self.can_place_word(word, (row, col), 'horizontal'):
                    positions.append(((row, col), 'horizontal'))
                if self.can_place_word(word, (row, col), 'vertical'):
                    positions.append(((row, col), 'vertical'))
        return positions

    def can_place_word(self, word, position, direction):
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

        return connected

    def place_word(self, word, position, direction):
        row, col = position
        if direction == 'horizontal':
            for i in range(len(word)):
                self.game.board_matrix[row][col + i] = (word[i], self.game.iteration)
                self.game.board.placed_letters[(row, col + i)] = word[i]
                self.game.board.cell_colors[(row, col + i)] = Utils.hex_to_rgb('#b79d9b')
        elif direction == 'vertical':
            for i in range(len(word)):
                self.game.board_matrix[row + i][col] = (word[i], self.game.iteration)
                self.game.board.placed_letters[(row + i, col)] = word[i]
                self.game.board.cell_colors[(row + i, col)] = Utils.hex_to_rgb('#b79d9b')
