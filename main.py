import sys
import random
import pygame
from config import *
from Modulos import *
from utils import *


class Juego100ARG:
    def __init__(self):
        pygame.init()

        self.pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("100 Argentinos dicen")
        self.font = pygame.font.Font(FONT_PATH1, FONT_SIZE)
        self.clock = pygame.time.Clock()
        self.resetear_juego()
        self.fondo_menu = cargar_imagen(
            "assets/imgs/fondo_menu2.jpg", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.fondo_preguntas = cargar_imagen(
            "assets/imgs/fondo_instrucciones.jpg", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.cruz_roja = cargar_imagen(
            "assets/imgs/cruz_roja.gif", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.input_respuesta = ""

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


# ------------------------------------------------------

    def seleccionar_preguntar_aleatoriamente(self):
        self.pregunta_actual = random.choice(
            cargar_archivo_jason("preguntas.json"))
        self.tiempo_restante = RESPONSE_TIME

# ------------------------------------------------------

    def mostrar_pregunta(self):
        texto_pregunta = self.font.render(
            self.pregunta_actual["pregunta"] + "?", True, WHITE)

        pregunta_rect = texto_pregunta.get_rect()

        pregunta_rect.topleft = (100, 350)

        padding = 10
        fondo_pregunta = pygame.Rect(pregunta_rect.x - padding, pregunta_rect.y - padding,
                                     pregunta_rect.width + 2 * padding, pregunta_rect.height + 2 * padding)

        pygame.draw.rect(self.pantalla, BLUE, fondo_pregunta)

        self.pantalla.blit(texto_pregunta, pregunta_rect)

# ------------------------------------------------------

    def mostrar_reloj(self):
        texto_reloj = self.font.render(
            f"{int(self.tiempo_restante)}s", True, WHITE)
        texto_reloj_rect = texto_reloj.get_rect()
        texto_reloj_rect.topleft = (SCREEN_WIDTH - 760, 410)
        circle_center = (texto_reloj_rect.x + texto_reloj_rect.width //
                         2, texto_reloj_rect.y + texto_reloj_rect.height // 2)

        pygame.draw.circle(self.pantalla, BLACK, circle_center, RADIUS)
        pygame.draw.circle(self.pantalla, YELLOW, circle_center, RADIUS, WIDTH)

        self.pantalla.blit(texto_reloj, texto_reloj_rect)

# ------------------------------------------------------

    def mostrar_input(self):
        input_respuesta = pygame.Rect(100, 400, 600, 50)
        pygame.draw.rect(self.pantalla, WHITE, input_respuesta, 2)

        texto_input = self.font.render(self.input_respuesta, True, WHITE)
        self.pantalla.blit(
            texto_input, (input_respuesta.x + 5, input_respuesta.y + 5))

# ------------------------------------------------------

    def chequear_respuesta(self, input_respuesta):
        respuestas = self.pregunta_actual["respuestas"]
        if input_respuesta in respuestas:
            self.puntaje += respuestas[input_respuesta]
        else:
            self.oportunidades -= 1
            respuesta_menor_valor = min(respuestas, key=respuestas.get)
            self.mostrar_respuestas()

        self.seleccionar_preguntar_aleatoriamente()
        self.input_respuesta = ""
        self.tiempo_restante = RESPONSE_TIME

# ------------------------------------------------------

    def mostrar_respuestas(self):
        y_offset = 450
        x_offset_left = 100
        x_offset_right = 400
        column = 0  # Variable para alternar entre columnas

        for respuesta, puntaje in self.pregunta_actual["respuestas"].items():
            texto_respuesta = self.font.render(
                f"{respuesta}: {puntaje}", True, WHITE)
            texto_respuesta_rect = texto_respuesta.get_rect()

            if column == 0:
                texto_respuesta_rect.topleft = (x_offset_left, y_offset)
                column = 1
            else:
                texto_respuesta_rect.topleft = (x_offset_right, y_offset)
                column = 0
                y_offset += 50  # Incrementar y_offset solo cuando se pasa a la siguiente fila

            padding = 10
            fondo_respuesta = pygame.Rect(texto_respuesta_rect.x - padding, texto_respuesta_rect.y - padding,
                                          texto_respuesta_rect.width + 2 * padding, texto_respuesta_rect.height + 2 * padding)
            pygame.draw.rect(self.pantalla, BLUE, fondo_respuesta)
            self.pantalla.blit(texto_respuesta, texto_respuesta_rect)

        if column == 1:
            y_offset += 50  # Incrementar y_offset para la siguiente fila si hay un elemento en la columna izquierda

# Esta funcion muestra las respuestas en una sola columna
    # def mostrar_respuestas(self):
    #     y_offset = 450
    #     for respuesta, puntaje in self.pregunta_actual["respuestas"].items():
    #         texto_respuesta = self.font.render(
    #             f"{respuesta}: {puntaje}", True, WHITE)
    #         texto_respuesta_rect = texto_respuesta.get_rect()
    #         texto_respuesta_rect.topleft = (100, y_offset)
    #         padding = 10
    #         fondo_respuesta = pygame.Rect(texto_respuesta_rect.x - padding, texto_respuesta_rect.y - padding,
    #                                       texto_respuesta_rect.width + 2 * padding, texto_respuesta_rect.height + 2 * padding)
    #         pygame.draw.rect(self.pantalla, BLUE, fondo_respuesta)

    #         self.pantalla.blit(texto_respuesta, texto_respuesta_rect)
    #         y_offset += 30

# ------------------------------------------------------

    def mostrar_puntaje(self):
        texto_puntaje = self.font.render(
            f"Puntos: {self.puntaje}", True, WHITE)
        texto_puntaje_rect = texto_puntaje.get_rect()
        texto_puntaje_rect.topright = (SCREEN_WIDTH - 6, 410)
        circle_center = (texto_puntaje_rect.x + texto_puntaje_rect.width //
                         2, texto_puntaje_rect.y + texto_puntaje_rect.height // 2)
        pygame.draw.circle(self.pantalla, BLACK, circle_center, RADIUS)
        pygame.draw.circle(self.pantalla, YELLOW, circle_center, RADIUS, WIDTH)

        self.pantalla.blit(texto_puntaje, texto_puntaje_rect)

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
            self.mostrar_pregunta()
            self.mostrar_reloj()
            self.mostrar_puntaje()
            self.mostrar_input()
            self.actualizar_estado_juego()
            self.mostrar_respuestas()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.chequear_respuesta(self.input_respuesta)
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_respuesta = self.input_respuesta[:-1]
                    else:
                        self.input_respuesta += event.unicode

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    juego = Juego100ARG()
    juego.run()
