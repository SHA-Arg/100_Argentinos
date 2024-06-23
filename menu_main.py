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

# ------------------------------------------------------


def draw_text(text, font, color, surface, x, y):
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

        draw_text('Jugar', font, WHITE, pantalla,
                  button_1.centerx, button_1.centery)
        draw_text('Instrucciones', font, WHITE, pantalla,
                  button_2.centerx, button_2.centery)
        draw_text('Salir', font, WHITE, pantalla,
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

        draw_text('1.Selecciona una temática al azar.', font,
                  BLACK, pantalla, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 150)
        draw_text('2.Ingresa tu respuesta antes de que se acabe el tiempo.',
                  font, BLACK, pantalla, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 200)
        draw_text('3.Gana puntos según las respuestas de los argentinos.',
                  font, BLACK, pantalla, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 250)
        draw_text('4.Acumula 500 puntos para ganar el premio mayor.',
                  font, BLACK, pantalla, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 300)
        draw_text('Presiona ESC para volver al menú', font,
                  BLACK, pantalla, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 350)
        # ------------------------- Texto en blanco -------------------------

        draw_text('1.Selecciona una temática al azar.', font,
                  WHITE, pantalla, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 155)
        draw_text('2.Ingresa tu respuesta antes de que se acabe el tiempo.',
                  font, WHITE, pantalla, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 205)
        draw_text('3.Gana puntos según las respuestas de los argentinos.',
                  font, WHITE, pantalla, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 255)
        draw_text('4.Acumula 500 puntos para ganar el premio mayor.',
                  font, WHITE, pantalla, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 305)
        draw_text('Presiona ESC para volver al menú', font,
                  WHITE, pantalla, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 355)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        pygame.display.update()

# ------------------------------------------------------


main_menu()
