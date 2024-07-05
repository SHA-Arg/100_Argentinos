import pygame
import sys
from .recursos import *
from .config import *

"""
    Muestra las instrucciones del juego en la pantalla.

    Espera a que el usuario presione ESC para volver al menú principal.
"""


def instrucciones():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pantalla.blit(fondo_instrucciones, (290, 230))

        # Instrucciones con fondo legible
        instrucciones_texto = [
            '',
            '1-El juego seleccionara una temática al azar con su respectiva pregunta.',
            '2-El jugador debe ingresar su respuesta ',
            '"antes de que se acabe el tiempo, tiene 3 errores como maximo".',
            '3-Ganara un punto por la cantidad de argentinos que',
            'coninciden con las respuestas.',
            '4-Al acumular 500 puntos gana el premio mayor.',
            'Presiona ESC para volver al menú'
        ]

        # Posiciones dinámicas para los textos
        for i, linea in enumerate(instrucciones_texto):
            escribir_texto(linea, font_instrucciones, WHITE, pantalla,
                           SCREEN_WIDTH // 1.5, SCREEN_HEIGHT // 4 + 50 * (i + 1))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        pygame.display.update()
# ------------------------------------------------------
