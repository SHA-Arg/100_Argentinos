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
        self.font = pygame.font.Font(FONT_PATH1, FONT_SIZE)
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

    def mostrar_input_usuario_reloj(self):
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

        # Respuestas
        input_respuesta = pygame.Rect(90, 400, 600, 50)
        pygame.draw.rect(self.pantalla, WHITE, input_respuesta, 1)
        texto_input = self.font.render(self.input_text, True, WHITE)
        self.pantalla.blit(
            texto_input, (input_respuesta.x + 5, input_respuesta.y + 5))


# ------------------------------------------------------

    def obtener_input_usuario(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                respuesta = self.input_text.strip().lower()
                self.input_text = ""
                return respuesta
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                self.input_text += event.unicode
        return None

# ------------------------------------------------------

    def chequear_respuesta(self, respuesta):
        puntos = 0
        respuesta_ingresada = respuesta.lower()
        for respuesta_ingresada in self.pregunta_actual["respuestas"].items():
            if respuesta_ingresada in self.pregunta_actual["respuestas"]:
                puntos += self.pregunta_actual["respuestas"][respuesta_ingresada]
                self.puntaje += puntos
                return True

    def mostrar_respuestas(self):
        y_offset = 500
        for respuesta, puntos in self.pregunta_actual["respuestas"].items():
            texto_respuesta = self.font.render(
                f"{respuesta}: {puntos}", True, WHITE)
            self.pantalla.blit(texto_respuesta, (100, y_offset))
            y_offset += 40
        return puntos


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
            self.mostrar_input_usuario_reloj()
            self.mostrar_puntaje()
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
