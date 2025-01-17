import pygame
import Utils
from Cell import Cell
from constants import letter_scores

class Board:
    """
    Represents the game board for Scrabble.

    Attributes:
        board_size (int): The size of the board.
        cell_size (int): The size of each cell on the board.
        margin (int): The margin between cells.
        placed_letters (dict): A dictionary of placed letters with their positions.
        cell_colors (dict): A dictionary of cell colors with their positions.
        piece_color (tuple): The color of the pieces.
    """

    def __init__(self, board_size, cell_size, margin):
        """
        Initializes the Board with the given size, cell size, and margin.

        Args:
            board_size (int): The size of the board.
            cell_size (int): The size of each cell on the board.
            margin (int): The margin between cells.
        """
        self.board_size = board_size
        self.cell_size = cell_size
        self.margin = margin
        self.placed_letters = {}
        self.cell_colors = {}
        self.piece_color = Utils.hex_to_rgb('#b79d9b')

        for row in range(self.board_size):
            for col in range(self.board_size):
                self.cell_colors[(row, col)] = Cell.get_cell_color(row, col)

    def count_placed_letters(self):
        """
        Returns the number of letters placed on the board.

        Returns:
            int: The number of placed letters.
        """
        return len(self.placed_letters)

    def draw(self, screen, font, score_font):
        """
        Draws the board and the placed letters on the screen.

        Args:
            screen (pygame.Surface): The screen to draw on.
            font (pygame.font.Font): The font for drawing letters.
            score_font (pygame.font.Font): The font for drawing letter scores.
        """
        for row in range(self.board_size):
            for col in range(self.board_size):
                x = self.margin + col * (self.cell_size + self.margin)
                y = self.margin + row * (self.cell_size + self.margin)

                Utils.draw_rounded_rect(screen, self.cell_colors[(row, col)], (x, y, self.cell_size, self.cell_size), corner_radius=8)

        self.draw_borders(screen)

        for row in range(self.board_size):
            for col in range(self.board_size):
                if (row, col) in self.placed_letters:
                    x = self.margin + col * (self.cell_size + self.margin)
                    y = self.margin + row * (self.cell_size + self.margin)

                    letter = self.placed_letters[(row, col)]
                    letter_text = font.render(letter, True, (0, 0, 0))
                    screen.blit(letter_text, (
                        x + (self.cell_size - letter_text.get_width()) // 2, y + (self.cell_size - letter_text.get_height()) // 2))

                    letter_score = letter_scores[letter]
                    score_text = score_font.render(str(letter_score), True, (0, 0, 0))
                    score_x = x + self.cell_size - score_text.get_width() - 5
                    score_y = y + self.cell_size - score_text.get_height() - 5
                    screen.blit(score_text, (score_x, score_y))

    def draw_borders(self, screen):
        """
        Draws the borders between placed letters on the board.

        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        border_color = Utils.hex_to_rgb('#b79d9b')  # Border color between letters

        def are_neighbors(cell1, cell2):
            r1, c1 = cell1
            r2, c2 = cell2
            return abs(r1 - r2) + abs(c1 - c2) == 1  # Check if they are neighbors

        for (row, col) in self.placed_letters:
            # Current cell coordinates
            x = self.margin + col * (self.cell_size + self.margin)
            y = self.margin + row * (self.cell_size + self.margin)

            # Check neighbors and color the common border
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (row + dr, col + dc)
                if neighbor in self.placed_letters and are_neighbors((row, col), neighbor):
                    # Neighbor coordinates
                    nx = self.margin + neighbor[1] * (self.cell_size + self.margin)
                    ny = self.margin + neighbor[0] * (self.cell_size + self.margin)

                    # Calculate the rectangle between letters
                    if row == neighbor[0]:  # Horizontal neighbor
                        rect_x = min(x, nx) + self.cell_size - self.margin * 2
                        rect_y = y
                        rect_width = self.margin * 5
                        rect_height = self.cell_size
                    else:  # Vertical neighbor
                        rect_x = x
                        rect_y = min(y, ny) + self.cell_size - self.margin * 2
                        rect_width = self.cell_size
                        rect_height = self.margin * 5

                    # Draw the rectangle between letters
                    pygame.draw.rect(screen, border_color, (rect_x, rect_y, rect_width, rect_height))