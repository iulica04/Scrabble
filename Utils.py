import pygame

def hex_to_rgb(hex_color):
    """
    Converts a hex color string to an RGB tuple.

    Args:
        hex_color (str): The hex color string (e.g., '#FFFFFF').

    Returns:
        tuple: A tuple representing the RGB color (e.g., (255, 255, 255)).
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

def draw_rounded_rect(surface, color, rect, corner_radius):
    """
    Draws a rounded rectangle on the given surface.

    Args:
        surface (pygame.Surface): The surface to draw on.
        color (tuple): The color of the rectangle (RGB tuple).
        rect (pygame.Rect): The rectangle to draw.
        corner_radius (int): The radius of the corners.
    """
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)