# game.py

import sys
import random
import pygame
from config import *
from preguntas import PREGUNTAS
import sys
from Modulos import *


class Juego100ARG:
    def __init__(self):
        pygame.init()
        # Inicializar pantalla
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("100 Argentinos dicen")
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.clock = pygame.time.Clock()
        self.resetear_juego()

        # Cargar imágenes de fondo
        self.fondo_menu = pygame.image.load("assets/imgs/fondo_menu2.jpg")
        self.fondo_preguntas = pygame.image.load("assets/imgs/fondo_menu.jpg")
        self.fondo_menu = pygame.transform.scale(
            self.fondo_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.fondo_preguntas = pygame.transform.scale(
            self.fondo_preguntas, (SCREEN_WIDTH, SCREEN_HEIGHT))

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
        self.input_text = ""

    def seleccionar_preguntar_aleatoriamente(self):
        self.pregunta_actual = random.choice(PREGUNTAS)
        self.tiempo_restante = RESPONSE_TIME
# ------------------------------------------------------

    def mostrar_pregunta(self):
        texto_pregunta = self.font.render(
            self.pregunta_actual["pregunta"], True, WHITE)
        self.screen.blit(texto_pregunta, (50, 50))

    def mostrar_input_usuario(self):
        input_box = pygame.Rect(50, 100, 700, 50)
        pygame.draw.rect(self.screen, WHITE, input_box, 2)
        texto_input = self.font.render(self.input_text, True, WHITE)
        self.screen.blit(texto_input, (input_box.x + 5, input_box.y + 5))

    def obtener_input_usuario(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return self.input_text.lower().strip()
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                self.input_text += event.unicode
        return None

        while ingresando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        ingresando = False
                    elif event.key == pygame.K_BACKSPACE:
                        respuesta_usuario = respuesta_usuario[:-1]
                    else:
                        respuesta_usuario += event.unicode

            self.screen.fill(WHITE)
            self.mostrar_pregunta()
            draw_text(self.screen, respuesta_usuario,
                      self.font, BLACK, 50, 150)
            pygame.display.flip()
            self.clock.tick(30)

        respuesta_usuario = normalizar_respuesta(respuesta_usuario)
        return respuesta_usuario

# ------------------------------------------------------
    def chequear_respuesta(self, respuesta):
        respuestas = self.pregunta_actual["respuestas"]
        if respuesta in respuestas:
            self.puntaje += respuestas[respuesta] * self.bonus_multiplicar
            self.bonus_multiplicar = 1  # Reset multiplier
            return True
        return False
# ------------------------------------------------------

    def actualizar_estado_juego(self):
        self.tiempo_restante -= 1 / 60
        if self.tiempo_restante <= 0:
            self.oportunidades -= 1
            self.seleccionar_preguntar_aleatoriamente()
            self.input_text = ""
            self.tiempo_restante = RESPONSE_TIME
            if self.oportunidades <= 0:
                self.mostrar_game_over()
                pygame.time.wait(3000)
                self.resetear_juego()

    def mostrar_game_over(self):
        texto_game_over = self.font.render("¡Juego Terminado!", True, BLACK)
        self.screen.blit(texto_game_over, (SCREEN_WIDTH //
                         2 - 100, SCREEN_HEIGHT // 2))

    def run(self):
        running = True
        self.seleccionar_preguntar_aleatoriamente()

        while running:
            self.screen.blit(self.fondo_preguntas, (0, 0))
            self.mostrar_pregunta()
            self.mostrar_input_usuario()
            self.actualizar_estado_juego()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                respuesta = self.obtener_input_usuario(event)
                if respuesta:
                    if self.chequear_respuesta(respuesta):
                        self.seleccionar_preguntar_aleatoriamente()
                        self.input_text = ""
                        self.tiempo_restante = RESPONSE_TIME
                    else:
                        self.oportunidades -= 1
                        if self.oportunidades <= 0:
                            self.mostrar_game_over()
                            pygame.time.wait(3000)
                            self.resetear_juego()
                        else:
                            self.tiempo_restante = RESPONSE_TIME

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    juego = Juego100ARG()
    juego.run()


# # Inicializa Pygame
# pygame.init()

# # Colores
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)

# # Dimensiones de la pantalla
# WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption('Juego de Barassi')

# # Fuente
# font = pygame.font.Font(None, 36)


# def draw_text(text, font, color, surface, x, y):
#     textobj = font.render(text, True, color)
#     textrect = textobj.get_rect()
#     textrect.center = (x, y)
#     surface.blit(textobj, textrect)


# def game():
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#         screen.fill(WHITE)
#         draw_text('Aquí va el juego', font, BLACK,
#                   screen, WIDTH // 2, HEIGHT // 2)

#         pygame.display.update()


# game()
