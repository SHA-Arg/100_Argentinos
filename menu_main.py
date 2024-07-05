import pygame
import sys
import subprocess
import os
from Packages.config import *
from Packages.utils import *
from Packages.recursos import *
from Packages.instruct import *

# ------------------------------------------------------

# Inicializa Pygame
pygame.init()

# ------------------------------------------------------


def main_menu():
    click = False
    while True:
        # Imágen de fondo
        pantalla.blit(fondo_menu, (0, 0))

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(SCREEN_WIDTH - 300, SCREEN_HEIGHT // 2, 200, 50)
        button_2 = pygame.Rect(
            SCREEN_WIDTH - 300, SCREEN_HEIGHT // 2 + 70, 200, 50)
        button_3 = pygame.Rect(
            SCREEN_WIDTH - 300, SCREEN_HEIGHT // 2 + 140, 200, 50)

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

        pygame.draw.rect(pantalla, BLUE, button_1)
        pygame.draw.rect(pantalla, BLUE, button_2)
        pygame.draw.rect(pantalla, BLUE, button_3)

        escribir_texto('Jugar', font, WHITE, pantalla,
                       button_1.centerx, button_1.centery)
        escribir_texto('Instrucciones', font, WHITE, pantalla,
                       button_2.centerx, button_2.centery)
        escribir_texto('Salir', font, WHITE, pantalla,
                       button_3.centerx, button_3.centery)
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

# ------------------------------------------------------


def jugar():
    # Ejecuta main.py
    subprocess.run(["python", "main.py"])

# ------------------------------------------------------


main_menu()
