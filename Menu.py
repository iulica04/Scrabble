import pygame
import random
import Utils
from constants import letters, letter_scores

class Menu:
    def __init__(self, screen_size, cell_size, margin, menu_height):
        self.cell_size = cell_size
        self.screen_size = screen_size
        self.margin = margin
        self.menu_height = menu_height
        self.menu_letters = random.choices(letters, k=5)
        self.initialize_menu()

        # Define button positions and sizes
        self.submit_button_rect = pygame.Rect(screen_size - 150, screen_size + 20, 100, 40)
        self.shuffle_button_rect = pygame.Rect(screen_size - 650, screen_size + 20, 100, 40)

    def initialize_menu(self):
        total_menu_width = len(self.menu_letters) * (self.cell_size + self.margin * 2) - self.margin * 2
        start_x = (self.screen_size - total_menu_width) // 2
        self.menu_letter_positions = [
            (start_x + i * (self.cell_size + self.margin * 2), self.screen_size + (self.menu_height - self.cell_size) // 2)
            for i in range(len(self.menu_letters))
        ]

    def draw(self, screen, font, score_font):
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
        pygame.draw.rect(screen, (0, 255, 0), self.submit_button_rect)
        submit_text = font.render("Submit", True, (0, 0, 0))
        screen.blit(submit_text, (self.submit_button_rect.x + 10, self.submit_button_rect.y + 5))

        pygame.draw.rect(screen, (0, 0, 255), self.shuffle_button_rect)
        shuffle_text = font.render("Shuffle", True, (255, 255, 255))
        screen.blit(shuffle_text, (self.shuffle_button_rect.x + 10, self.shuffle_button_rect.y + 5))

    def handle_button_click(self, pos):
        if self.submit_button_rect.collidepoint(pos):
            self.replace_letters()
            return "submit"
        elif self.shuffle_button_rect.collidepoint(pos):
            self.shuffle_letters()
            return "shuffle"
        return None

    def replace_letters(self):
        # Replace used letters with new ones
        print(f"Number of letters left in the menu: {len(self.menu_letters)}")
        num_new_letters = 5 - len(self.menu_letters)
        self.menu_letters.extend([self.get_random_letter() for _ in range(num_new_letters)])
        self.initialize_menu()

    @staticmethod
    def get_random_letter():
        # Generate a random letter (you can customize this method as needed)
        return random.choice(letters)

    def shuffle_letters(self):
        random.shuffle(self.menu_letters)
        self.initialize_menu()