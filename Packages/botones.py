import pygame
from .config import *
from .recursos import *

# -----------------------------------------
"""
Crea un rectángulo de Pygame en las coordenadas especificadas.

Args:
    x (int): Coordenada x de la esquina superior izquierda del rectángulo.
    y (int): Coordenada y de la esquina superior izquierda del rectángulo.
    width (int): Ancho del rectángulo.
    height (int): Altura del rectángulo.

Returns:
    pygame.Rect: El rectángulo creado.
"""


def crear_boton(x, y, width, height):
    return pygame.Rect(x, y, width, height)


# -----------------------------------------
"""
    Dibuja un rectángulo en la pantalla y le agrega un texto centrado.

    Args:
        boton (pygame.Rect): El rectángulo del botón.
        texto (str): El texto a mostrar en el botón.
    """


def dibujar_boton(boton, texto):
    pygame.draw.rect(pantalla, BLUE, boton)
    escribir_texto(texto, font, WHITE, pantalla, boton.centerx, boton.centery)
