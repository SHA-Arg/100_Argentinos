# game.py

import random
import pygame
from config import *
from preguntas import PREGUNTAS


class Juego100ARG:
    def __init__(self):
        pygame.init()
        # Inicializar pantalla
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("100 Argentinos dicen")
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.clock = pygame.time.Clock()
        self.resetear_juego()

    def resetear_juego(self):
        self.puntaje = 0
        self.oportunidades = 3
        self.pregunta_actual = None
        self.tiempo_restante = RESPONSE_TIME
        self.bonus_multiplicar = 1
        self.used_hints = {
            "tiempo_extra": False,
            "menos_votada": False,
            "multiplicar_puntos": False
        }

    def seleccionar_preguntar_aleatoriamente(self):
        self.pregunta_actual = random.choice(PREGUNTAS)
        self.tiempo_restante = RESPONSE_TIME

    def mostrar_pregunta(self):
        texto_pregunta = self.font.render(
            self.pregunta_actual["pregunta"], True, BLACK)
        self.screen.blit(texto_pregunta, (50, 50))

    def obtener_input_usuario(self):
        # Obtener entrada del usuario
        pass

    def chequear_respuesta(self, respuesta):
        respuestas = self.pregunta_actual["respuestas"]
        if respuesta in respuestas:
            self.puntaje += respuestas[respuesta] * self.bonus_multiplicar
            self.bonus_multiplicar = 1  # Reset multiplier
            return True
        return False

    def actualizar_estado_juego(self):
        # Actualizar el estado del juego, manejar oportunidades, tiempo restante, etc.
        pass

    def run(self):
        running = True
        self.seleccionar_preguntar_aleatoriamente()

        while running:
            self.screen.fill(WHITE)
            self.mostrar_pregunta()
            self.actualizar_estado_juego()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    pass

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    juego = Juego100ARG()
    juego.run()
