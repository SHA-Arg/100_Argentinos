import pygame
import sys
import subprocess
import os
from config import *


# Inicializa Pygame
pygame.init()

# Fuente
font = pygame.font.Font(FONT_PATH, FONT_SIZE)

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('100 Argentinos dicen')

# Cargar imágenes de fondo
fondo_menu = pygame.image.load("assets/imgs/fondo_menu2.jpg")
fondo_preguntas = pygame.image.load("assets/imgs/fondo_menu.jpg")
fondo_instrucciones = pygame.image.load("assets/imgs/fondo_instrucciones.jpg")
fondo_menu = pygame.transform.scale(
    fondo_menu, (WIDTH, HEIGHT))
fondo_preguntas = pygame.transform.scale(
    fondo_preguntas, (WIDTH, HEIGHT))
fondo_instrucciones = pygame.transform.scale(
    fondo_instrucciones, (WIDTH, HEIGHT))


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


main_font = pygame.font.SysFont("cambria", 50)


def main_menu():
    while True:
        # Imágen de fondo
        screen.blit(fondo_menu, (0, 0))

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(WIDTH - 300, HEIGHT // 2, 200, 50)
        button_2 = pygame.Rect(WIDTH - 300, HEIGHT // 2 + 70, 200, 50)
        button_3 = pygame.Rect(WIDTH - 300, HEIGHT // 2 + 140, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                play_game()
        if button_2.collidepoint((mx, my)):
            if click:
                show_instructions()
        if button_3.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        pygame.draw.rect(screen, BLUE, button_1)
        pygame.draw.rect(screen, BLUE, button_2)
        pygame.draw.rect(screen, BLUE, button_3)

        draw_text('Jugar', font, WHITE, screen,
                  button_1.centerx, button_1.centery)
        draw_text('Instrucciones', font, WHITE, screen,
                  button_2.centerx, button_2.centery)
        draw_text('Salir', font, WHITE, screen,
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


def play_game():
    # Ejecuta main.py
    subprocess.run(["python", "main.py"])


def show_instructions():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(fondo_instrucciones, (0, 0))
        draw_text('Instrucciones del juego', font,
                  BLACK, screen, WIDTH // 2, HEIGHT // 4)
        draw_text('1. Selecciona una temática al azar.', font,
                  BLACK, screen, WIDTH // 2, HEIGHT // 4 + 150)
        draw_text('2. Ingresa tu respuesta antes de que se acabe el tiempo.',
                  font, BLACK, screen, WIDTH // 2, HEIGHT // 4 + 200)
        draw_text('3. Gana puntos según las respuestas de los argentinos.',
                  font, BLACK, screen, WIDTH // 2, HEIGHT // 4 + 250)
        draw_text('4. Acumula 500 puntos para ganar el premio mayor.',
                  font, BLACK, screen, WIDTH // 2, HEIGHT // 4 + 300)
        draw_text('Presiona ESC para volver al menú', font,
                  BLACK, screen, WIDTH // 2, HEIGHT // 4 + 350)
        # ------------------------- Texto en blanco -------------------------
        draw_text('Instrucciones del juego', font,
                  WHITE, screen, WIDTH // 2, HEIGHT // 4)
        draw_text('1. Selecciona una temática al azar.', font,
                  WHITE, screen, WIDTH // 2, HEIGHT // 4 + 155)
        draw_text('2. Ingresa tu respuesta antes de que se acabe el tiempo.',
                  font, WHITE, screen, WIDTH // 2, HEIGHT // 4 + 205)
        draw_text('3. Gana puntos según las respuestas de los argentinos.',
                  font, WHITE, screen, WIDTH // 2, HEIGHT // 4 + 255)
        draw_text('4. Acumula 500 puntos para ganar el premio mayor.',
                  font, WHITE, screen, WIDTH // 2, HEIGHT // 4 + 305)
        draw_text('Presiona ESC para volver al menú', font,
                  WHITE, screen, WIDTH // 2, HEIGHT // 4 + 355)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        pygame.display.update()


main_menu()
