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
        self.fondo_preguntas = pygame.image.load("assets/imgs/fondo_instrucciones.jpg")
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
        texto_tematica = self.font.render(
            self.pregunta_actual["tematica"], True, WHITE)
        self.pantalla.blit(texto_tematica, (150, 290))
        texto_pregunta = self.font.render(
            self.pregunta_actual["pregunta"], True, WHITE)
        self.pantalla.blit(texto_pregunta, (150, 320))

# ------------------------------------------------------

    def mostrar_input_usuario(self):
        input_respuesta = pygame.Rect(150, 360, 600, 50)
        pygame.draw.rect(self.pantalla, WHITE, input_respuesta, 2)
        texto_input = self.font.render(self.input_text, True, WHITE)
        self.pantalla.blit(
            texto_input, (input_respuesta.x + 5, input_respuesta.y + 5))

# ------------------------------------------------------

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

            self.pantalla.fill(WHITE)
            self.mostrar_pregunta()
            draw_text(self.pantalla, respuesta_usuario,
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

# ------------------------------------------------------
# intefaz del juego
# ------------------------------------------------------

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def respuestas(self):
        while True:
            # Imágen de fondo
            self.pantalla.blit(self.fondo_menu, (0, 0))

            mx, my = pygame.mouse.get_pos()

            respuesta_A = pygame.Rect(
                SCREEN_WIDTH - 300, SCREEN_HEIGHT // 2, 200, 50)
            respuesta_B = pygame.Rect(
                SCREEN_WIDTH - 300, SCREEN_HEIGHT // 2 + 70, 200, 50)
            respuesta_C = pygame.Rect(
                SCREEN_WIDTH - 300, SCREEN_HEIGHT // 2 + 140, 200, 50)
            respuesta_D = pygame.Rect(
                SCREEN_WIDTH - 300, SCREEN_HEIGHT // 2 + 210, 200, 50)

            if respuesta_A.collidepoint((mx, my)):
                if click:
                    self.respuesta_a()
            if respuesta_B.collidepoint((mx, my)):
                if click:
                    self.respuesta_b()
            if respuesta_C.collidepoint((mx, my)):
                if click:
                    self.respuesta_c()
            if respuesta_D.collidepoint((mx, my)):
                if click:
                    self.respuesta_d()

            pygame.draw.rect(self.pantalla, BLUE, respuesta_A)
            pygame.draw.rect(self.pantalla, BLUE, respuesta_B)
            pygame.draw.rect(self.pantalla, BLUE, respuesta_C)
            pygame.draw.rect(self.pantalla, BLUE, respuesta_D)

            self.draw_text('A', self.font, WHITE, self.pantalla,
                           respuesta_A.centerx, respuesta_A.centery)
            self.draw_text('B', self.font, WHITE,
                           self.pantalla, respuesta_B.centerx, respuesta_B.centery)
            self.draw_text('C', self.font, WHITE, self.pantalla,
                           respuesta_C.centerx, respuesta_C.centery)
            self.draw_text('D', self.font, WHITE,
                           self.pantalla, respuesta_D.centerx, respuesta_D.centery)

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == respuesta_A:
                        click = True
                    if event.button == respuesta_B:
                        click = True
                    if event.button == respuesta_C:
                        click = True
                    if event.button == respuesta_D:
                        click = True

            pygame.display.update()


if __name__ == "__main__":
    juego = Juego100ARG()
    juego.run()
