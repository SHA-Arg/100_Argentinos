import pygame
import sys
import subprocess
import os
from config import *


# Inicializa Pygame
pygame.init()

# Fuente
font = pygame.font.Font(FONT_PATH, FONT_SIZE)

# Dimensiones de la pantalla
pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('100 Argentinos dicen')

# Cargar imágenes de fondo
fondo_menu = pygame.image.load("assets/imgs/fondo_menu2.jpg")
fondo_preguntas = pygame.image.load("assets/imgs/fondo_menu.jpg")
fondo_instrucciones = pygame.image.load("assets/imgs/fondo_instrucciones.jpg")
fondo_menu = pygame.transform.scale(fondo_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))
fondo_preguntas = pygame.transform.scale(
    fondo_preguntas, (SCREEN_WIDTH, SCREEN_HEIGHT))
fondo_instrucciones = pygame.transform.scale(
    fondo_instrucciones, (SCREEN_WIDTH, SCREEN_HEIGHT))
fondo_instrucciones.fill(BLUE)

# ------------------------------------------------------


def escribir_texto(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# ------------------------------------------------------


def main_menu():
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


def instrucciones():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pantalla.blit(fondo_instrucciones, (0, 0))

        # Instrucciones con fondo legible
        instrucciones_texto = [
            'El juego seleccionara una temática al azar.',
            'El jugador debe ingresar su respuesta ',
            'antes de que se acabe el tiempo.',
            'Gana un punto por cada vez que',
            'conincide con las respuestas de los 100 argentinos.',
            'Al acumular 500 puntos gana el premio mayor.',
            '',
            'Presiona ESC para volver al menú'
        ]

        # Posiciones dinámicas para los textos
        for i, linea in enumerate(instrucciones_texto):
            escribir_texto(linea, font, WHITE, pantalla,
                           SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 50 * (i + 1))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        pygame.display.update()

# ------------------------------------------------------


main_menu()
