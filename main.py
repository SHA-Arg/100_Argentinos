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
        # Renderizar el texto de la temática
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

    def mostrar_reloj(self):
        # Mostrar cuenta regresiva
        texto_reloj = self.font.render(
            f"{int(self.tiempo_restante)}s", True, WHITE)
        texto_reloj_rect = texto_reloj.get_rect()
        texto_reloj_rect.topleft = (SCREEN_WIDTH - 750, 410)
        circle_center = (texto_reloj_rect.x + texto_reloj_rect.width //
                         2, texto_reloj_rect.y + texto_reloj_rect.height // 2)

        # Dibujar el círculo en la misma posición que el texto
        pygame.draw.circle(self.pantalla, BLACK, circle_center, RADIUS)
        pygame.draw.circle(self.pantalla, YELLOW, circle_center, RADIUS, WIDTH)

        self.pantalla.blit(texto_reloj, texto_reloj_rect)

    def mostrar_input(self, event):
        # Respuestas
        input_respuesta = pygame.Rect(90, 400, 600, 50)
        pygame.draw.rect(self.pantalla, WHITE, input_respuesta, 1)
        texto_input = self.font.render(self.input_respuesta, True, WHITE)
        self.pantalla.blit(
            texto_input, (input_respuesta.x + 5, input_respuesta.y + 5))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                respuesta = self.input_respuesta.strip().lower()
                self.input_respuesta = ""
                return respuesta
            elif event.key == pygame.K_BACKSPACE:
                self.input_respuesta = self.input_respuesta[:-1]
            else:
                self.input_respuesta += event.unicode
        return None


# ------------------------------------------------------


# ------------------------------------------------------

    def chequear_respuesta(self, input_respuesta):
        if input_respuesta == self.pregunta_actual["respuestas"]:
            self.puntaje += 1
            self.seleccionar_preguntar_aleatoriamente()
            self.tiempo_restante = RESPONSE_TIME
        elif input_respuesta != self.pregunta_actual["respuestas"]:
            self.oportunidades -= 1
            self.seleccionar_preguntar_aleatoriamente()
            self.tiempo_restante = RESPONSE_TIME

    def mostrar_respuestas(self):
        cargar_archivo_jason("preguntas.json")
        for respuesta in cargar_archivo_jason("preguntas.json"):
            texto_respuesta = self.font.render(
                respuesta["respuestas"], True, WHITE)
            texto_respuesta_rect = texto_respuesta.get_rect()
            texto_respuesta_rect.topleft = (100, 410 + 50)
            self.pantalla.blit(texto_respuesta, texto_respuesta_rect)


# ------------------------------------------------------


    def mostrar_puntaje(self):
        texto_puntaje = self.font.render(
            f"Puntos: {self.puntaje}", True, WHITE)
        texto_puntaje_rect = texto_puntaje.get_rect()
        texto_puntaje_rect.topright = (SCREEN_WIDTH - 2, 410)
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
            self.actualizar_estado_juego()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    self.input_text = self.mostrar_input(event)
                    self.chequear_respuesta(self.input_text)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":

    juego = Juego100ARG()
    juego.run()
