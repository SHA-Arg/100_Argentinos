import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import pygame
from Packages.instruct import *
from Packages.botones import *
from Packages.juego import *
from Packages.inicializadores import *

# Inicializa Pygame
pygame.init()

# ---------------------------------------------------------


def main_menu():
    """
    Menú principal con diseño estético: título centrado y botones con hover.
    """
    AMARILLO = (255, 215, 0)
    GRIS = (170, 170, 170)
    VERDE = (80, 200, 120)
    ROJO = (220, 60, 60)

    font_titulo = pygame.font.Font(FONT_PATH1, 38)
    font_sub = pygame.font.Font(FONT_PATH1, 15)
    font_btn = pygame.font.Font(FONT_PATH1, 21)

    BTN_W, BTN_H = 270, 54
    btn_x = SCREEN_WIDTH // 2 - BTN_W // 2

    botones = [
        pygame.Rect(btn_x, 230, BTN_W, BTN_H),
        pygame.Rect(btn_x, 305, BTN_W, BTN_H),
        pygame.Rect(btn_x, 380, BTN_W, BTN_H),
    ]
    labels = ['JUGAR', 'INSTRUCCIONES', 'SALIR']
    colores_btn = [VERDE, AMARILLO, ROJO]
    acciones = [jugar, instrucciones, lambda: (pygame.quit(), sys.exit())]

    clock = pygame.time.Clock()
    while True:
        pantalla.blit(fondo_menu, (0, 0))

        # Overlay oscuro para legibilidad
        ov = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 120))
        pantalla.blit(ov, (0, 0))

        # Panel título
        pan_w, pan_h = 700, 115
        pan_x = (SCREEN_WIDTH - pan_w) // 2
        pan_surf = pygame.Surface((pan_w, pan_h), pygame.SRCALPHA)
        pan_surf.fill((10, 10, 30, 210))
        pantalla.blit(pan_surf, (pan_x, 55))
        pygame.draw.rect(pantalla, AMARILLO, (pan_x, 55, pan_w, pan_h), 2, border_radius=10)

        t_main = font_titulo.render("100 ARGENTINOS DICEN", True, AMARILLO)
        pantalla.blit(t_main, t_main.get_rect(center=(SCREEN_WIDTH // 2, 100)))

        pygame.draw.line(pantalla, AMARILLO, (pan_x + 30, 126), (pan_x + pan_w - 30, 126), 1)

        t_sub = font_sub.render("El clasico juego de la television argentina", True, GRIS)
        pantalla.blit(t_sub, t_sub.get_rect(center=(SCREEN_WIDTH // 2, 148)))

        # Botones con hover
        mx, my = pygame.mouse.get_pos()
        for rect, label, color in zip(botones, labels, colores_btn):
            hover = rect.collidepoint(mx, my)
            fill = color if hover else (15, 15, 40)
            pygame.draw.rect(pantalla, fill, rect, border_radius=8)
            pygame.draw.rect(pantalla, color, rect, 2, border_radius=8)
            txt_color = (10, 10, 10) if hover else WHITE
            lbl = font_btn.render(label, True, txt_color)
            pantalla.blit(lbl, lbl.get_rect(center=rect.center))

        # Créditos
        cr = font_sub.render("Desarrollado con Python & Pygame", True, (90, 90, 90))
        pantalla.blit(cr, cr.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 18)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, accion in zip(botones, acciones):
                    if rect.collidepoint(event.pos):
                        accion()

        pygame.display.update()
        clock.tick(60)

# ---------------------------------------------------------


def jugar():
    juego = Juego100ARG()
    juego.ejecutar()

# ---------------------------------------------------------


main_menu()
