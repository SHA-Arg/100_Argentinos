import pygame
from .config import *


class Reloj:
    def __init__(self, font, pantalla):
        self.font = font
        self.pantalla = pantalla
        self.tiempo_restante = RESPONSE_TIME

    def actualizar(self, delta_tiempo):
        self.tiempo_restante -= delta_tiempo

    def dibujar(self):
        texto_reloj = self.font.render(
            f"{int(self.tiempo_restante)}s", True, (255, 255, 255))
        texto_reloj_rect = texto_reloj.get_rect(topleft=(800 - 760, 350))
        circle_center = (texto_reloj_rect.x + texto_reloj_rect.width //
                         2, texto_reloj_rect.y + texto_reloj_rect.height // 2)
        pygame.draw.circle(self.pantalla, (0, 0, 0), circle_center, 30)
        pygame.draw.circle(self.pantalla, (255, 255, 0), circle_center, 30, 5)
        self.pantalla.blit(texto_reloj, texto_reloj_rect)
