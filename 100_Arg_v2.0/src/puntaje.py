import pygame


class Puntaje:
    def __init__(self, font, pantalla):
        self.font = font
        self.pantalla = pantalla
        self.puntaje = 0

    def agregar_puntos(self, puntos):
        self.puntaje += puntos

    def resetear(self):
        self.puntaje = 0

    def dibujar(self):
        texto_puntaje = self.font.render(
            f"Puntos: {self.puntaje}", True, (255, 255, 255))
        texto_puntaje_rect = texto_puntaje.get_rect(topright=(800 - 6, 350))
        circle_center = (texto_puntaje_rect.x + texto_puntaje_rect.width //
                         2, texto_puntaje_rect.y + texto_puntaje_rect.height // 2)
        pygame.draw.circle(self.pantalla, (0, 0, 0), circle_center, 30)
        pygame.draw.circle(self.pantalla, (255, 255, 0), circle_center, 30, 5)
        self.pantalla.blit(texto_puntaje, texto_puntaje_rect)
