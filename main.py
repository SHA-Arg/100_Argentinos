import pygame
import sys
import subprocess
import os
from Packages.config import *
from Packages.utils import *
from Packages.recursos import *
from Packages.instruct import *
from Packages.botones import *
from Packages.juego import *
from Packages.inicializadores import *

# Inicializa Pygame
pygame.init()

# ---------------------------------------------------------


def main_menu():
    """
    Función principal del menú. Muestra los botones y maneja la lógica de clics.
    """
    # Crea botones
    button_1 = crear_boton(SCREEN_WIDTH - 300, SCREEN_HEIGHT // 2, 200, 50)
    button_2 = crear_boton(
        SCREEN_WIDTH - 300, SCREEN_HEIGHT // 2 + 70, 200, 50)
    button_3 = crear_boton(
        SCREEN_WIDTH - 300, SCREEN_HEIGHT // 2 + 140, 200, 50)

    while True:
        # Imágen de fondo
        pantalla.blit(fondo_menu, (0, 0))

        mx, my = pygame.mouse.get_pos()

        # Verificar colisiones y ejecutar acciones
        if button_1.collidepoint((mx, my)):
            if click:
                jugar()
        if button_2.collidepoint((mx, my)):
            if click:
                instrucciones()

        if button_3.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        # Dibujar botones
        dibujar_boton(button_1, 'Jugar')
        dibujar_boton(button_2, 'Instrucciones')
        dibujar_boton(button_3, 'Salir')

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

# ---------------------------------------------------------


def jugar():
    juego = Juego100ARG()
    juego.ejecutar()

# ---------------------------------------------------------


main_menu()
