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
            "assets/imgs/Fondo_Juego_100Arg.png", SCREEN_WIDTH, SCREEN_HEIGHT)
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

        pregunta_rect.topleft = (20, 60)

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
        texto_reloj_rect.topleft = (SCREEN_WIDTH - 780, 120)
        circle_center = (texto_reloj_rect.x + texto_reloj_rect.width //
                         2, texto_reloj_rect.y + texto_reloj_rect.height // 2)

        pygame.draw.circle(self.pantalla, BLACK, circle_center, RADIUS_Time)
        pygame.draw.circle(self.pantalla, YELLOW,
                           circle_center, RADIUS_Time, WIDTH)

        self.pantalla.blit(texto_reloj, texto_reloj_rect)

        if self.tiempo_restante <= 5:
            pygame.draw.circle(self.pantalla, RED,
                               circle_center, RADIUS_Time, WIDTH)

# ------------------------------------------------------

    def mostrar_input(self):
        input_respuesta = pygame.Rect(70, 110, 500, 50)
        pygame.draw.rect(self.pantalla, WHITE, input_respuesta, 2)

        texto_input = self.font.render(self.input_respuesta, True, WHITE)
        self.pantalla.blit(
            texto_input, (input_respuesta.x + 5, input_respuesta.y + 5))

# ------------------------------------------------------

    def chequear_respuesta(self, input_respuesta):
        respuestas = self.pregunta_actual["respuestas"]
        if input_respuesta in self.pregunta_actual["respuestas"]:
            if self.used_hints["multiplicar_puntos"]:
                self.puntaje += respuestas[input_respuesta] * 2
            else:
                self.puntaje += respuestas[input_respuesta]
        elif input_respuesta == "tiempo_extra":
            self.used_hints["tiempo_extra"] = True
            self.tiempo_restante += 10
        elif self.used_hints["menos_votada"]:
            self.puntaje += respuestas[min(
                respuestas, key=respuestas.get)]
        else:
            self.oportunidades -= 1
            self.pantalla.blit(self.cruz_roja, (0, 0))
            pygame.display.flip()
            pygame.time.wait(1000)

        self.seleccionar_preguntar_aleatoriamente()
        self.input_respuesta = ""
        self.tiempo_restante = RESPONSE_TIME

# ------------------------------------------------------

    def mostrar_comodines(self):
        texto_comodin_tiempo_extra = self.font.render(
            f"Tiempo Extra", True, WHITE)
        texto_comodin_menos_votada = self.font.render(
            f"Menos Votada", True, WHITE)
        texto_comodin_multiplicar_puntos = self.font.render(
            f"Multiplicar Puntos", True, WHITE)

        texto_comodin_tiempo_extra_rect = texto_comodin_tiempo_extra.get_rect()
        texto_comodin_menos_votada_rect = texto_comodin_menos_votada.get_rect()
        texto_comodin_multiplicar_puntos_rect = texto_comodin_multiplicar_puntos.get_rect()

        texto_comodin_tiempo_extra_rect.topleft = (500, 450)
        texto_comodin_menos_votada_rect.topleft = (500, 500)
        texto_comodin_multiplicar_puntos_rect.topleft = (500, 550)

        pygame.draw.rect(self.pantalla, BLUE, texto_comodin_tiempo_extra_rect)
        pygame.draw.rect(self.pantalla, BLUE, texto_comodin_menos_votada_rect)
        pygame.draw.rect(self.pantalla, BLUE,
                         texto_comodin_multiplicar_puntos_rect)

        self.pantalla.blit(texto_comodin_tiempo_extra,
                           texto_comodin_tiempo_extra_rect)
        self.pantalla.blit(texto_comodin_menos_votada,
                           texto_comodin_menos_votada_rect)
        self.pantalla.blit(texto_comodin_multiplicar_puntos,
                           texto_comodin_multiplicar_puntos_rect)

        if self.used_hints["tiempo_extra"]:
            pygame.draw.rect(self.pantalla, GREEN,
                             texto_comodin_tiempo_extra_rect)
        if self.used_hints["menos_votada"]:
            pygame.draw.rect(self.pantalla, GREEN,
                             texto_comodin_menos_votada_rect)
        if self.used_hints["multiplicar_puntos"]:
            pygame.draw.rect(self.pantalla, GREEN,
                             texto_comodin_multiplicar_puntos_rect)

        return texto_comodin_tiempo_extra_rect, texto_comodin_menos_votada_rect, texto_comodin_multiplicar_puntos_rect

    def click_comodin(self, pos):
        comodin_tiempo_extra, comodin_menos_votada, comodin_multiplicar_puntos = self.mostrar_comodines()

        if comodin_tiempo_extra.collidepoint(pos):
            self.used_hints["tiempo_extra"] = True
        elif comodin_menos_votada.collidepoint(pos):
            self.used_hints["menos_votada"] = True
        elif comodin_multiplicar_puntos.collidepoint(pos):
            self.used_hints["multiplicar_puntos"] = True

    def usar_comodin(self, comodin):
        if not self.used_hints[comodin]:
            self.used_hints[comodin] = True
            return True

# ------------------------------------------------------

    def mostrar_respuestas(self):
        y_offset = 200
        for respuesta, puntaje in self.pregunta_actual["respuestas"].items():
            texto_respuesta = self.font.render(
                f"{respuesta}: {puntaje}", True, WHITE)
            texto_respuesta_rect = texto_respuesta.get_rect()
            texto_respuesta_rect.topleft = (100, y_offset)
            pygame.draw.rect(self.pantalla, BLUE, texto_respuesta_rect)
            self.pantalla.blit(texto_respuesta, texto_respuesta_rect)
            y_offset += 50


# ------------------------------------------------------


    def mostrar_puntaje(self):
        texto_puntaje = self.font.render(
            f"Puntos: {self.puntaje}", True, WHITE)
        texto_puntaje_rect = texto_puntaje.get_rect()
        texto_puntaje_rect.topright = (SCREEN_WIDTH - 400, 500)
        circle_center = (texto_puntaje_rect.x + texto_puntaje_rect.width //
                         2, texto_puntaje_rect.y + texto_puntaje_rect.height // 2)
        pygame.draw.circle(self.pantalla, BLACK, circle_center, RADIUS_Puntaje)
        pygame.draw.circle(self.pantalla, YELLOW,
                           circle_center, RADIUS_Puntaje, WIDTH)

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
        texto_game_over = self.font.render(
            "¡Juego Terminado!", True, WHITE, RED)
        self.pantalla.blit(texto_game_over, (SCREEN_WIDTH //
                                             2 - 100, SCREEN_HEIGHT // 2))
        self.pantalla.blit(self.cruz_roja, (100, 100))

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
            self.mostrar_comodines()

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
