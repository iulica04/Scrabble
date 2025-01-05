import Utils

class Cell:
    """
    Represents a cell on the Scrabble board with potential bonus types.

    Attributes:
        bonus_cells (dict): A dictionary mapping cell positions to their bonus types.
    """

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

    @staticmethod
    def get_cell_color(row, col):
        """
        Returns the color of the cell based on its position and bonus type.

        Args:
            row (int): The row position of the cell.
            col (int): The column position of the cell.

        Returns:
            tuple: The RGB color of the cell.
        """
        if (row, col) in Cell.bonus_cells:
            bonus_type = Cell.bonus_cells[(row, col)]
            if bonus_type == 'TW':
                return Utils.hex_to_rgb('#6B597F')
            elif bonus_type == 'DL':
                return Utils.hex_to_rgb('#92a1c2')
            elif bonus_type == 'DW':
                return Utils.hex_to_rgb('#a2869c')
            elif bonus_type == 'TL':
                return Utils.hex_to_rgb('3f5b8d')
            else:
                return Utils.hex_to_rgb('#d9d9d9')
        else:
            return Utils.hex_to_rgb('#d9d9d9')  # default