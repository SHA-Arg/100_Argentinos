import pygame


class Boton:
    def __init__(self, texto, posicion, color, font, pantalla):
        self.texto = texto
        self.rect = pygame.Rect(posicion, (200, 30))
        self.color = color
        self.font = font
        self.pantalla = pantalla

    def dibujar(self):
        pygame.draw.rect(self.pantalla, self.color, self.rect)
        texto_renderizado = self.font.render(self.texto, True, (255, 255, 255))
        self.pantalla.blit(texto_renderizado, self.rect)

    def colisiona(self, pos):
        return self.rect.collidepoint(pos)
