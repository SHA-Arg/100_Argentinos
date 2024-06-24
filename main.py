import sys
import random
import pygame
from config import *
from preguntas import *
from Modulos import *


class Juego100ARG:
    def __init__(self):
        pygame.init()
        # Inicializar pantalla
        self.pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("100 Argentinos dicen")
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.clock = pygame.time.Clock()
        self.resetear_juego()

        # Cargar imágenes de fondo
        self.fondo_menu = pygame.image.load("assets/imgs/fondo_menu2.jpg")
        self.fondo_preguntas = pygame.image.load(
            "assets/imgs/fondo_instrucciones.jpg")
        self.fondo_menu = pygame.transform.scale(
            self.fondo_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.fondo_preguntas = pygame.transform.scale(
            self.fondo_preguntas, (SCREEN_WIDTH, SCREEN_HEIGHT))
# ------------------------------------------------------

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

# ------------------------------------------------------

    def seleccionar_preguntar_aleatoriamente(self):
        self.pregunta_actual = random.choice(PREGUNTAS)
        self.tiempo_restante = RESPONSE_TIME
# ------------------------------------------------------

    def mostrar_pregunta(self):
        # Renderizar el texto de la temática y obtener su tamaño
        texto_tematica = self.font.render(
            self.pregunta_actual["tematica"] + ":", True, WHITE)
        texto_pregunta = self.font.render(
            self.pregunta_actual["pregunta"] + "?", True, WHITE)

        # Obtener el tamaño del texto renderizado para centrarlo
        tematica_rect = texto_tematica.get_rect()
        pregunta_rect = texto_pregunta.get_rect()

        # Posición de los textos
        tematica_rect.topleft = (100, 290)
        pregunta_rect.topleft = (100, 350)

        # Dibujar un fondo azul sólido según el tamaño del texto
        padding = 10  # Espacio adicional alrededor del texto
        fondo_tematica = pygame.Rect(tematica_rect.x - padding, tematica_rect.y - padding,
                                     tematica_rect.width + 2 * padding, tematica_rect.height + 2 * padding)
        fondo_pregunta = pygame.Rect(pregunta_rect.x - padding, pregunta_rect.y - padding,
                                     pregunta_rect.width + 2 * padding, pregunta_rect.height + 2 * padding)

        pygame.draw.rect(self.pantalla, BLUE, fondo_tematica)
        pygame.draw.rect(self.pantalla, BLUE, fondo_pregunta)

        # Dibujar el texto sobre el fondo azul
        self.pantalla.blit(texto_tematica, tematica_rect)
        self.pantalla.blit(texto_pregunta, pregunta_rect)

# ------------------------------------------------------

    def mostrar_input_usuario(self):
        input_respuesta = pygame.Rect(90, 400, 600, 50)
        pygame.draw.rect(self.pantalla, WHITE, input_respuesta, 1)
        texto_input = self.font.render(self.input_text, True, WHITE)
        self.pantalla.blit(
            texto_input, (input_respuesta.x + 5, input_respuesta.y + 5))

# ------------------------------------------------------

    def obtener_input_usuario(self, event):
        pass


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
                pygame.time.wait(1000)
                self.resetear_juego()

# ------------------------------------------------------

    def mostrar_game_over(self):
        texto_game_over = self.font.render("¡Juego Terminado!", True, BLACK)
        self.pantalla.blit(texto_game_over, (SCREEN_WIDTH //
                                             2 - 100, SCREEN_HEIGHT // 2))

# ------------------------------------------------------

    def run(self):
        running = True
        self.seleccionar_preguntar_aleatoriamente()

        while running:
            self.pantalla.blit(self.fondo_preguntas, (0, 0))
            # self.mostrar_tematica()
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
        sys.exit()


if __name__ == "__main__":
    juego = Juego100ARG()
    juego.run()
