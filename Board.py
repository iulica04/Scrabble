import pygame
import sys
import random

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

def draw_rounded_rect(surface, color, rect, corner_radius):
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

def get_cell_color(row, col):

    bonus_cells = {
        (0, 0): 'TW', (0, 7): 'TW', (0, 14): 'TW',
        (7, 0): 'TW', (7, 7): 'TW', (7, 14): 'TW',
        (14, 0): 'TW', (14, 7): 'TW', (14, 14): 'TW',
        (3, 0): 'DL', (11, 0): 'DL', (3, 14): 'DL', (11, 14): 'DL',
        (0, 3): 'DL', (0, 11): 'DL', (14, 3): 'DL', (14, 11): 'DL',
        (6, 2): 'DL', (7, 3): 'DL', (8, 2): 'DL', (2, 6): 'DL',
        (3, 7): 'DL', (2, 8): 'DL', (6, 12): 'DL', (7, 11): 'DL',
        (8, 12): 'DL', (12, 6): 'DL', (11, 7): 'DL', (12, 8): 'DL',
        (6, 6): 'DL', (6, 8): 'DL', (8, 6): 'DL', (8, 8): 'DL',
        (5, 5): 'TL', (5, 9): 'TL', (9, 5): 'TL', (9, 9): 'TL',
        (5, 1): 'TL', (9, 1): 'TL', (5, 13): 'TL', (9, 13): 'TL',
        (1, 5): 'TL', (1, 9): 'TL', (13, 5): 'TL', (13, 9): 'TL',
        (1, 1): 'DW', (2, 2): 'DW', (3, 3): 'DW', (4, 4): 'DW',
        (1, 13): 'DW', (2, 12): 'DW', (3, 11): 'DW', (4, 10): 'DW',
        (13, 13): 'DW', (12, 12): 'DW', (11, 11): 'DW', (10, 10): 'DW',
        (13, 1): 'DW', (12, 2): 'DW', (11, 3): 'DW', (10, 4): 'DW',
    }


    if (row, col) in bonus_cells:
        bonus_type = bonus_cells[(row, col)]
        if bonus_type == 'TW':
            return hex_to_rgb('#6B597F')
        elif bonus_type == 'DL':
            return hex_to_rgb('#92a1c2')
        elif bonus_type == 'DW':
            return hex_to_rgb('#a2869c')
        elif bonus_type == 'TL':
            return hex_to_rgb('3f5b8d')
        else:
            return hex_to_rgb('#d9d9d9')
    else:
        return hex_to_rgb('#d9d9d9')  # default

def create_scrabble_board_with_drag_and_drop():
    board_size = 15
    cell_size = 45
    margin = 3
    menu_height = 80
    screen_size = board_size * (cell_size + margin) + margin

    pygame.init()
    screen = pygame.display.set_mode((screen_size, screen_size + menu_height))
    pygame.display.set_caption("Scrabble with Drag-and-Drop")
    font = pygame.font.Font(None, 36)
    score_font = pygame.font.Font(None, 20)

    letter_scores = {
        'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1,
        'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1,
        'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10
    }

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    menu_letters = random.choices(letters, k=5)

    total_menu_width = len(menu_letters) * (cell_size + margin * 2) - margin * 2
    start_x = (screen_size - total_menu_width) // 2
    menu_letter_positions = [
        (start_x + i * (cell_size + margin * 2), screen_size + (menu_height - cell_size) // 2)
        for i in range(len(menu_letters))
    ]

    placed_letters = {}
    cell_colors = {}

    dragged_letter = None
    dragged_letter_offset = (0, 0)
    dragged_letter_pos = None
    letter_from_board = None

    piece_color =  hex_to_rgb('#b79d9b')



    for row in range(board_size):
        for col in range(board_size):
            cell_colors[(row, col)] = get_cell_color(row, col)
    while True:
        screen.fill(hex_to_rgb('#1a1b21'))

        for row in range(board_size):
            for col in range(board_size):
                x = margin + col * (cell_size + margin)
                y = margin + row * (cell_size + margin)

                draw_rounded_rect(screen, cell_colors[(row, col)], (x, y, cell_size, cell_size), corner_radius=8)

                if (row, col) in placed_letters:
                    letter = placed_letters[(row, col)]
                    letter_text = font.render(letter, True, (0, 0, 0))
                    screen.blit(letter_text, (
                    x + (cell_size - letter_text.get_width()) // 2, y + (cell_size - letter_text.get_height()) // 2))

                    letter_score = letter_scores[letter]
                    score_text = score_font.render(str(letter_score), True, (0, 0, 0))
                    score_x = x + cell_size - score_text.get_width() - 5
                    score_y = y + cell_size - score_text.get_height() - 5
                    screen.blit(score_text, (score_x, score_y))

        menu_y = screen_size
        pygame.draw.rect(screen, (50, 50, 50), (0, menu_y, screen_size, menu_height))

        for i, (letter, pos) in enumerate(zip(menu_letters, menu_letter_positions)):
            x, y = pos
            letter_text = font.render(letter, True, (0, 0, 0))
            letter_score = letter_scores[letter]
            score_text = score_font.render(str(letter_score), True, (0, 0, 0))

            draw_rounded_rect(screen, piece_color, (x, y, cell_size, cell_size), corner_radius=8)

            screen.blit(letter_text, (
            x + (cell_size - letter_text.get_width()) // 2, y + (cell_size - letter_text.get_height()) // 2))

            score_x = x + cell_size - score_text.get_width() - 5
            score_y = y + cell_size - score_text.get_height() - 5
            screen.blit(score_text, (score_x, score_y))

        if dragged_letter:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dragged_x, dragged_y = dragged_letter_pos

            draw_rounded_rect(screen, piece_color, (
            mouse_x - dragged_letter_offset[0], mouse_y - dragged_letter_offset[1], cell_size, cell_size),
                              corner_radius=8)
            letter_text = font.render(dragged_letter, True, (255, 255, 255))
            screen.blit(letter_text, (mouse_x - dragged_letter_offset[0] + (cell_size - letter_text.get_width()) // 2,
                                      mouse_y - dragged_letter_offset[1] + (cell_size - letter_text.get_height()) // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                for i, (letter, pos) in enumerate(zip(menu_letters, menu_letter_positions)):
                    x, y = pos
                    if x <= mouse_x <= x + cell_size and y <= mouse_y <= y + cell_size:
                        dragged_letter = letter
                        dragged_letter_pos = (x, y)
                        dragged_letter_offset = (mouse_x - x, mouse_y - y)

                        menu_letters.pop(i)
                        menu_letter_positions.pop(i)

                for (row, col), letter in list(placed_letters.items()):
                    x = margin + col * (cell_size + margin)
                    y = margin + row * (cell_size + margin)
                    if x <= mouse_x <= x + cell_size and y <= mouse_y <= y + cell_size:
                        dragged_letter = letter
                        dragged_letter_pos = (x, y)
                        letter_from_board = (row, col)
                        del placed_letters[(row, col)]
                        cell_colors[(row, col)] = get_cell_color(row, col)

            elif event.type == pygame.MOUSEMOTION:
                if dragged_letter:
                    pass

            elif event.type == pygame.MOUSEBUTTONUP:
                if dragged_letter:
                    mouse_x, mouse_y = event.pos
                    col = (mouse_x - margin) // (cell_size + margin)
                    row = (mouse_y - margin) // (cell_size + margin)

                    if 0 <= row < board_size and 0 <= col < board_size:
                        placed_letters[(row, col)] = dragged_letter

                        cell_colors[(row, col)] = piece_color
                    else:

                        if letter_from_board:
                            cell_colors[(row, col)] = get_cell_color(letter_from_board[0], letter_from_board[1])

                        menu_letters.append(dragged_letter)

                        total_menu_width = len(menu_letters) * (cell_size + margin * 2) - margin * 2
                        start_x = (screen_size - total_menu_width) // 2
                        menu_letter_positions = [
                            (start_x + i * (cell_size + margin * 2), screen_size + (menu_height - cell_size) // 2)
                            for i in range(len(menu_letters))
                        ]
                    dragged_letter = None
                    dragged_letter_pos = None
                    dragged_letter_offset = (0, 0)
                    letter_from_board = None

        pygame.display.flip()

if __name__ == "__main__":
    create_scrabble_board_with_drag_and_drop()
