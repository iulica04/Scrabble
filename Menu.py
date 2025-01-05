import pygame
import random
from constants import letters, letter_scores
import Utils

class Menu:
    """
    Represents the menu for the Scrabble game.

    Attributes:
        cell_size (int): The size of each cell in the menu.
        screen_size (int): The size of the screen.
        margin (int): The margin between cells.
        menu_height (int): The height of the menu.
        dictionary (set): The set of words loaded from the dictionary file.
        menu_letters (list): The list of letters in the menu.
        used_words (set): The set of words that have been used.
        game (Game): The game instance.
        submit_button_rect (pygame.Rect): The rectangle for the submit button.
        shuffle_button_rect (pygame.Rect): The rectangle for the shuffle button.
    """

    def __init__(self, screen_size, cell_size, margin, menu_height, dictionary_path, game):
        """
        Initializes the Menu with the given parameters.

        Args:
            screen_size (int): The size of the screen.
            cell_size (int): The size of each cell in the menu.
            margin (int): The margin between cells.
            menu_height (int): The height of the menu.
            dictionary_path (str): The path to the dictionary file.
            game (Game): The game instance.
        """
        self.cell_size = cell_size
        self.screen_size = screen_size
        self.margin = margin
        self.menu_height = menu_height
        self.dictionary = self.load_dictionary(path=dictionary_path)
        self.menu_letters = []
        self.used_words = set()
        self.game = game
        self.initialize_menu()

        # Define button positions and sizes
        self.submit_button_rect = pygame.Rect(screen_size - 150, screen_size + 20, 100, 40)
        self.shuffle_button_rect = pygame.Rect(screen_size - 650, screen_size + 20, 100, 40)

    def load_dictionary(self, path):
        """
        Loads the dictionary file and returns a set of words.

        Args:
            path (str): The path to the dictionary file.

        Returns:
            set: A set of words from the dictionary file.
        """
        with open(path, 'r') as file:
            words = file.read().splitlines()
        return set(word.upper() for word in words)

    def initialize_menu(self):
        """
        Initializes the menu with valid letters.
        """
        self.menu_letters = self.get_valid_letters()
        self.update_letter_positions()

    def get_valid_letters(self):
        """
        Gets valid letters for the menu.

        Returns:
            list: A list of valid letters.
        """
        valid_words = [word for word in self.dictionary if len(word) == 7 and word not in self.used_words]
        if valid_words:
            selected_word = random.choice(valid_words)
            self.used_words.add(selected_word)
            return list(selected_word)
        return random.choices(letters, k=5)  # Fallback to random letters if no valid word is found

    def update_letter_positions(self):
        """
        Updates the positions of the letters in the menu.
        """
        total_menu_width = len(self.menu_letters) * (self.cell_size + self.margin * 2) - self.margin * 2
        start_x = (self.screen_size - total_menu_width) // 2
        self.menu_letter_positions = [
            (start_x + i * (self.cell_size + self.margin * 2), self.screen_size + (self.menu_height - self.cell_size) // 2)
            for i in range(len(self.menu_letters))
        ]

    def draw(self, screen, font, score_font):
        """
        Draws the menu on the screen.

        Args:
            screen (pygame.Surface): The screen to draw on.
            font (pygame.font.Font): The font for drawing letters.
            score_font (pygame.font.Font): The font for drawing letter scores.
        """
        menu_y = screen.get_height() - self.menu_height
        pygame.draw.rect(screen, (50, 50, 50), (0, menu_y, screen.get_width(), self.menu_height))

        for i, (letter, pos) in enumerate(zip(self.menu_letters, self.menu_letter_positions)):
            x, y = pos
            letter_text = font.render(letter, True, (0, 0, 0))
            letter_score = letter_scores[letter]
            score_text = score_font.render(str(letter_score), True, (0, 0, 0))

            Utils.draw_rounded_rect(screen, Utils.hex_to_rgb('#b79d9b'), (x, y, self.cell_size, self.cell_size), corner_radius=8)

            screen.blit(letter_text, (
                x + (self.cell_size - letter_text.get_width()) // 2, y + (self.cell_size - letter_text.get_height()) // 2))

            score_x = x + self.cell_size - score_text.get_width() - 5
            score_y = y + self.cell_size - score_text.get_height() - 5
            screen.blit(score_text, (score_x, score_y))

        # Draw buttons
        pygame.draw.rect(screen, Utils.hex_to_rgb('#92a1c2'), self.submit_button_rect)
        submit_text = font.render("Submit", True, (0, 0, 0))
        screen.blit(submit_text, (self.submit_button_rect.x + 8, self.submit_button_rect.y + 7))

        pygame.draw.rect(screen, Utils.hex_to_rgb('#6B597F'), self.shuffle_button_rect)
        shuffle_text = font.render("Shuffle", True, (255, 255, 255))
        screen.blit(shuffle_text, (self.shuffle_button_rect.x + 10, self.shuffle_button_rect.y + 7))

    def handle_button_click(self, pos):
        """
        Handles button clicks in the menu.

        Args:
            pos (tuple): The position of the mouse click.

        Returns:
            str: The action to be performed ("submit" or "shuffle").
        """
        if self.submit_button_rect.collidepoint(pos):
            return "submit"
        elif self.shuffle_button_rect.collidepoint(pos):
            self.shuffle_letters()
            return "shuffle"
        return None

    def replace_letters(self):
        """
        Replaces the letters in the menu with new letters.
        """
        available_letters = self.get_available_letters()
        valid_words = [word for word in self.dictionary if any(letter in available_letters for letter in word)]
        if valid_words:
            selected_word = random.choice(valid_words)
            self.menu_letters = list(selected_word[:7])
            random.shuffle(self.menu_letters)
            if len(self.menu_letters) < 7:
                self.menu_letters.extend(random.choices(letters, k=7 - len(self.menu_letters)))
        else:
            self.menu_letters = random.choices(letters, k=7)
        self.update_letter_positions()

    def get_available_letters(self):
        """
        Gets the available letters from the board and menu.

        Returns:
            set: A set of available letters.
        """
        available_letters = set(self.menu_letters)
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                if self.game.board_matrix[row][col] is not None:
                    if self.count_neighbors(row, col) <= 2:
                        available_letters.add(self.game.board_matrix[row][col][0])
        return available_letters

    def count_neighbors(self, row, col):
        """
        Counts the number of neighboring cells with letters.

        Args:
            row (int): The row position of the cell.
            col (int): The column position of the cell.

        Returns:
            int: The number of neighboring cells with letters.
        """
        neighbors = 0
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            adj_row, adj_col = row + dr, col + dc
            if 0 <= adj_row < self.game.board_size and 0 <= adj_col < self.game.board_size:
                if self.game.board_matrix[adj_row][adj_col] is not None:
                    neighbors += 1
        return neighbors

    @staticmethod
    def get_random_letter():
        """
        Gets a random letter from the set of letters.

        Returns:
            str: A random letter.
        """
        return random.choice(letters)

    def shuffle_letters(self):
        """
        Shuffles the letters in the menu.
        """
        random.shuffle(self.menu_letters)
        self.update_letter_positions()