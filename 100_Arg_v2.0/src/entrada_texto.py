import pygame


class EntradaTexto:
    def __init__(self, font, pantalla):
        self.font = font
        self.pantalla = pantalla
        self.texto = ""

    def manejar_evento(self, evento):
        if evento.key == pygame.K_RETURN:
            respuesta = self.texto
            self.texto = ""
            return respuesta
        elif evento.key == pygame.K_BACKSPACE:
            self.texto = self.texto[:-1]
        else:
            self.texto += evento.unicode
        return None

    def dibujar(self):
        input_respuesta = pygame.Rect(110, 350, 580, 50)
        pygame.draw.rect(self.pantalla, (255, 255, 255), input_respuesta, 2)
        texto_input = self.font.render(self.texto, True, (255, 255, 255))
        self.pantalla.blit(
            texto_input, (input_respuesta.x + 5, input_respuesta.y + 5))
