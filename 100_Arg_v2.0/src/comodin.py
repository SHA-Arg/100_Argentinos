import pygame


class Comodin:
    def __init__(self, nombre, posicion, color, font, pantalla):
        self.nombre = nombre
        self.rect = pygame.Rect(posicion, (200, 30))
        self.color = color
        self.font = font
        self.pantalla = pantalla
        self.usado = False

    def dibujar(self):
        color_actual = (0, 255, 0) if self.usado else self.color
        pygame.draw.rect(self.pantalla, color_actual, self.rect)
        texto_renderizado = self.font.render(
            self.nombre, True, (255, 255, 255))
        self.pantalla.blit(texto_renderizado, self.rect)

    def colisiona(self, pos):
        return self.rect.collidepoint(pos)

    def activar(self):
        self.usado = True
