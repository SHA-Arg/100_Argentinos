import sys
import random
import pygame
from config import *
from utils import cargar_imagen, cargar_archivo_json


class Juego100ARG:
    def __init__(self):
        pygame.init()
        self.audio_correcto = pygame.mixer.Sound("assets/sounds/correcto.mp3")
        self.audio_incorrecto = pygame.mixer.Sound("assets/sounds/error.mp3")
        self.pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("100 Argentinos dicen")
        self.font = pygame.font.Font(FONT_PATH1, FONT_SIZE)
        self.clock = pygame.time.Clock()
        self.fondo_menu = cargar_imagen(
            "assets/imgs/fondo_menu2.jpg", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.fondo_preguntas = cargar_imagen(
            "assets/imgs/Fondo_Juego_100Arg.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.fondo_game_over = cargar_imagen(
            "assets/imgs/Fondo_violeta.jpg", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.cruz_roja_gif = cargar_imagen(
            "assets/imgs/cruz_roja.gif", 100, 100)
        self.input_respuesta = ""
        self.puntaje = 0
        self.comodin_usado = False
        self.oportunidades = 3
        self.preguntas = cargar_archivo_json("preguntas.json")
        self.respuestas_ingresadas = []
        self.resetear_juego()

    def resetear_juego(self):
        self.puntaje = 0
        self.oportunidades = 3
        self.tiempo_restante = RESPONSE_TIME
        self.bonus_multiplicar = 1
        self.used_hints = {
            "tiempo_extra": False,
            "menos_votada": False,
            "multiplicar_puntos": False
        }
        self.seleccionar_pregunta_aleatoriamente()
        self.respuestas_ingresadas = []

    def seleccionar_pregunta_aleatoriamente(self):
        if not self.preguntas:
            raise ValueError(
                "No hay preguntas disponibles en el archivo JSON.")
        self.pregunta_actual = random.choice(self.preguntas)
        self.tiempo_restante = RESPONSE_TIME

    def mostrar_pregunta(self):
        if self.pregunta_actual is None:
            raise ValueError("No se ha seleccionado ninguna pregunta.")
        texto_pregunta = self.font.render(
            self.pregunta_actual["pregunta"] + "?", True, WHITE)
        pregunta_rect = texto_pregunta.get_rect()
        pregunta_rect.topleft = (20, 60)
        padding = 10
        fondo_pregunta = pygame.Rect(pregunta_rect.x - padding, pregunta_rect.y - padding,
                                     pregunta_rect.width + 2 * padding, pregunta_rect.height + 2 * padding)
        pygame.draw.rect(self.pantalla, BLUE, fondo_pregunta)
        self.pantalla.blit(texto_pregunta, pregunta_rect)

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

    def mostrar_respuestas_ingresadas(self):
        y_offset = 200
        for respuesta, puntos in self.respuestas_ingresadas:
            texto_respuesta = self.font.render(
                f"{respuesta}: {puntos}", True, WHITE)
            texto_respuesta_rect = texto_respuesta.get_rect()
            texto_respuesta_rect.topleft = (100, y_offset)

            pygame.draw.rect(self.pantalla, BLUE, texto_respuesta_rect)
            self.pantalla.blit(texto_respuesta, texto_respuesta_rect)

            y_offset += 50

    def mostrar_input(self):
        input_respuesta_rect = pygame.Rect(70, 110, 500, 50)
        pygame.draw.rect(self.pantalla, WHITE, input_respuesta_rect, 2)
        texto_input = self.font.render(self.input_respuesta, True, WHITE)
        self.pantalla.blit(
            texto_input, (input_respuesta_rect.x + 5, input_respuesta_rect.y + 5))

        pygame.display.update(input_respuesta_rect)

    def chequear_respuesta(self, input_respuesta):
        respuestas = self.pregunta_actual["respuestas"]
        if input_respuesta in respuestas:
            self.audio_correcto.play()
            self.puntaje += respuestas[input_respuesta] * \
                self.bonus_multiplicar
            self.respuestas_ingresadas.append(
                (input_respuesta, respuestas[input_respuesta]))
        else:
            self.mostrar_animacion_cruz()
            self.audio_incorrecto.play()
            self.oportunidades -= 1
        self.input_respuesta = ""
        if self.oportunidades == 0:
            self.mostrar_game_over()
            pygame.time.wait(1000)
            self.resetear_juego()

    def mostrar_animacion_cruz(self):
        cruz_rect = self.cruz_roja_gif.get_rect()
        cruz_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.pantalla.blit(self.cruz_roja_gif, cruz_rect)
        pygame.display.update()
        pygame.time.delay(1000)

    def mostrar_comodines(self):
        texto_comodin_tiempo_extra = self.font.render(
            "Tiempo Extra", True, WHITE)
        texto_comodin_menos_votada = self.font.render(
            "Menos Votada", True, WHITE)
        texto_comodin_multiplicar_puntos = self.font.render(
            "Multiplicar Puntos", True, WHITE)

        self.comodin_tiempo_extra_rect = texto_comodin_tiempo_extra.get_rect()
        self.comodin_menos_votada_rect = texto_comodin_menos_votada.get_rect()
        self.comodin_multiplicar_puntos_rect = texto_comodin_multiplicar_puntos.get_rect()

        self.comodin_tiempo_extra_rect.topleft = (500, 450)
        self.comodin_menos_votada_rect.topleft = (500, 500)
        self.comodin_multiplicar_puntos_rect.topleft = (500, 550)

        pygame.draw.rect(self.pantalla, BLUE, self.comodin_tiempo_extra_rect)
        pygame.draw.rect(self.pantalla, BLUE, self.comodin_menos_votada_rect)
        pygame.draw.rect(self.pantalla, BLUE,
                         self.comodin_multiplicar_puntos_rect)

        if not self.used_hints["tiempo_extra"]:
            self.pantalla.blit(texto_comodin_tiempo_extra,
                               self.comodin_tiempo_extra_rect)
        if not self.used_hints["menos_votada"]:
            self.pantalla.blit(texto_comodin_menos_votada,
                               self.comodin_menos_votada_rect)
        if not self.used_hints["multiplicar_puntos"]:
            self.pantalla.blit(texto_comodin_multiplicar_puntos,
                               self.comodin_multiplicar_puntos_rect)

    def usar_comodin(self, tipo):
        if tipo == "tiempo_extra" and not self.used_hints[tipo]:
            self.tiempo_restante += 10
            self.used_hints[tipo] = True
        elif tipo == "menos_votada" and not self.used_hints[tipo]:
            respuestas = self.pregunta_actual["respuestas"]
            menos_votada = min(respuestas, key=respuestas.get)
            self.respuestas_ingresadas.append(
                (menos_votada, respuestas[menos_votada]))
            self.used_hints[tipo] = True
        elif tipo == "multiplicar_puntos" and not self.used_hints[tipo]:
            self.bonus_multiplicar = 2
            self.used_hints[tipo] = True

    def manejar_eventos(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.resetear_juego()
            elif event.key == pygame.K_BACKSPACE:
                self.input_respuesta = self.input_respuesta[:-1]
            elif event.key == pygame.K_RETURN:
                self.chequear_respuesta(self.input_respuesta)
            else:
                self.input_respuesta += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.comodin_tiempo_extra_rect.collidepoint(mouse_pos):
                self.usar_comodin("tiempo_extra")
            if self.comodin_menos_votada_rect.collidepoint(mouse_pos):
                self.usar_comodin("menos_votada")
            if self.comodin_multiplicar_puntos_rect.collidepoint(mouse_pos):
                self.usar_comodin("multiplicar_puntos")

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

    def mostrar_oportunidades(self):
        texto_oportunidades = self.font.render(
            f"Oportunidades: {self.oportunidades}", True, BLACK, GREEN)
        texto_oportunidades_rect = texto_oportunidades.get_rect()
        texto_oportunidades_rect.topleft = (SCREEN_WIDTH - 800, 10)
        self.pantalla.blit(texto_oportunidades, texto_oportunidades_rect)

    def mostrar_game_over(self):
        self.fondo_game_over()
        game_over_text = self.font.render("Game Over", True, RED)
        self.pantalla.blit(game_over_text, (SCREEN_WIDTH //
                           2 - 100, SCREEN_HEIGHT // 2))

    def actualizar_reloj(self):
        self.tiempo_restante -= 1 / FPS
        if self.tiempo_restante <= 0:
            self.oportunidades -= 1
            self.tiempo_restante = RESPONSE_TIME
            if self.oportunidades > 0:
                self.seleccionar_pregunta_aleatoriamente()
                self.mostrar_pregunta()

        if self.oportunidades == 0:
            self.mostrar_game_over()
            pygame.time.wait(2000)
            self.resetear_juego()

    def ejecutar(self):
        while True:
            self.pantalla.blit(self.fondo_preguntas, (0, 0))
            self.mostrar_pregunta()
            self.mostrar_reloj()
            self.mostrar_input()
            self.mostrar_puntaje()
            self.mostrar_oportunidades()
            self.mostrar_comodines()
            self.mostrar_respuestas_ingresadas()

            for event in pygame.event.get():
                self.manejar_eventos(event)

            self.actualizar_reloj()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    juego = Juego100ARG()
    juego.ejecutar()
# ---------------------------------------------------------------------------------------------------#

# ---------------------------------------------------------------------------------------------------#

# import sys
# import random
# import pygame
# from config import *
# from Modulos import *
# from utils import cargar_archivo_json, cargar_imagen


# class Juego100ARG:
#     def __init__(self):
#         pygame.init()
#         self.audio_correcto = pygame.mixer.Sound("assets/sounds/correcto.mp3")
#         self.audio_incorrecto = pygame.mixer.Sound("assets/sounds/error.mp3")
#         self.pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#         pygame.display.set_caption("100 Argentinos dicen")
#         self.font = pygame.font.Font(FONT_PATH1, FONT_SIZE)
#         self.clock = pygame.time.Clock()
#         self.resetear_juego()
#         self.fondo_menu = cargar_imagen(
#             "assets/imgs/fondo_menu2.jpg", SCREEN_WIDTH, SCREEN_HEIGHT)
#         self.fondo_preguntas = cargar_imagen(
#             "assets/imgs/Fondo_Juego_100Arg.png", SCREEN_WIDTH, SCREEN_HEIGHT)
#         self.cruz_roja_gif = cargar_imagen(
#             "assets/imgs/cruz_roja.gif", SCREEN_WIDTH, SCREEN_HEIGHT)
#         self.cruz_error = cargar_imagen("assets/imgs/cruz_error.png", 100, 100)
#         self.input_respuesta = ""

#         self.puntaje = 0
#         self.oportunidades = 3

#     def resetear_juego(self):
#         self.puntaje = 0
#         self.oportunidades = 3
#         self.pregunta_actual = None
#         self.tiempo_restante = RESPONSE_TIME
#         self.bonus_multiplicar = 1
#         self.used_hints = {
#             "tiempo_extra": True,
#             "menos_votada": True,
#             "multiplicar_puntos": True
#         }

#     def mostrar_cruz_roja(self):
#         self.pantalla.blit(self.cruz_error, (100, 180))
#         pygame.display.flip()
#         pygame.time.wait(1000)

#     def seleccionar_pregunta_aleatoriamente(self):
#         self.pregunta_actual = random.choice(
#             cargar_archivo_json("preguntas.json"))
#         self.tiempo_restante = RESPONSE_TIME

#     def mostrar_pregunta(self):
#         texto_pregunta = self.font.render(
#             self.pregunta_actual["pregunta"] + "?", True, WHITE)
#         pregunta_rect = texto_pregunta.get_rect()
#         pregunta_rect.topleft = (20, 60)
#         padding = 10
#         fondo_pregunta = pygame.Rect(pregunta_rect.x - padding, pregunta_rect.y - padding,
#                                      pregunta_rect.width + 2 * padding, pregunta_rect.height + 2 * padding)
#         pygame.draw.rect(self.pantalla, BLUE, fondo_pregunta)
#         self.pantalla.blit(texto_pregunta, pregunta_rect)

#     def mostrar_reloj(self):
#         texto_reloj = self.font.render(
#             f"{int(self.tiempo_restante)}s", True, WHITE)
#         texto_reloj_rect = texto_reloj.get_rect()
#         texto_reloj_rect.topleft = (SCREEN_WIDTH - 780, 120)
#         circle_center = (texto_reloj_rect.x + texto_reloj_rect.width //
#                          2, texto_reloj_rect.y + texto_reloj_rect.height // 2)

#         pygame.draw.circle(self.pantalla, BLACK, circle_center, RADIUS_Time)
#         pygame.draw.circle(self.pantalla, YELLOW,
#                            circle_center, RADIUS_Time, WIDTH)
#         self.pantalla.blit(texto_reloj, texto_reloj_rect)

#         if self.tiempo_restante <= 5:
#             pygame.draw.circle(self.pantalla, RED,
#                                circle_center, RADIUS_Time, WIDTH)

#     def mostrar_input(self):
#         input_respuesta = pygame.Rect(70, 110, 500, 50)
#         pygame.draw.rect(self.pantalla, WHITE, input_respuesta, 2)
#         texto_input = self.font.render(self.input_respuesta, True, WHITE)
#         self.pantalla.blit(
#             texto_input, (input_respuesta.x + 5, input_respuesta.y + 5))

#     def chequear_respuesta(self, input_respuesta):
#         respuestas = self.pregunta_actual["respuestas"]
#         if input_respuesta in respuestas:
#             self.audio_correcto.play()
#             self.puntaje += respuestas[input_respuesta] * \
#                 self.bonus_multiplicar
#             self.input_respuesta = ""
#             if self.used_hints["tiempo_extra"]:
#                 self.comodin_tiempo_extra()
#             elif self.used_hints["menos_votada"]:
#                 self.mostrar_menos_votada()
#             elif self.used_hints["multiplicar_puntos"]:
#                 self.comodin_multiplicar_puntos()

#             self.seleccionar_pregunta_aleatoriamente()
#         else:
#             self.oportunidades -= 1
#             self.audio_incorrecto.play()
#             self.input_respuesta = ""
#             if self.oportunidades <= 0:
#                 self.mostrar_game_over()
#                 pygame.time.wait(1000)
#                 self.resetear_juego()

#     def mostrar_comodines(self):
#         texto_comodin_tiempo_extra = self.font.render(
#             "Tiempo Extra", True, WHITE)
#         texto_comodin_menos_votada = self.font.render(
#             "Menos Votada", True, WHITE)
#         texto_comodin_multiplicar_puntos = self.font.render(
#             "Multiplicar Puntos", True, WHITE)

#         texto_comodin_tiempo_extra_rect = texto_comodin_tiempo_extra.get_rect()
#         texto_comodin_menos_votada_rect = texto_comodin_menos_votada.get_rect()
#         texto_comodin_multiplicar_puntos_rect = texto_comodin_multiplicar_puntos.get_rect()

#         texto_comodin_tiempo_extra_rect.topleft = (500, 450)
#         texto_comodin_menos_votada_rect.topleft = (500, 500)
#         texto_comodin_multiplicar_puntos_rect.topleft = (500, 550)

#         pygame.draw.rect(self.pantalla, BLUE, texto_comodin_tiempo_extra_rect)
#         pygame.draw.rect(self.pantalla, BLUE, texto_comodin_menos_votada_rect)
#         pygame.draw.rect(self.pantalla, BLUE,
#                          texto_comodin_multiplicar_puntos_rect)

#         self.pantalla.blit(texto_comodin_tiempo_extra,
#                            texto_comodin_tiempo_extra_rect)
#         self.pantalla.blit(texto_comodin_menos_votada,
#                            texto_comodin_menos_votada_rect)
#         self.pantalla.blit(texto_comodin_multiplicar_puntos,
#                            texto_comodin_multiplicar_puntos_rect)

#         if self.used_hints["tiempo_extra"]:
#             pygame.draw.rect(self.pantalla, GREEN,
#                              texto_comodin_tiempo_extra_rect)
#         if self.used_hints["menos_votada"]:
#             pygame.draw.rect(self.pantalla, GREEN,
#                              texto_comodin_menos_votada_rect)
#         if self.used_hints["multiplicar_puntos"]:
#             pygame.draw.rect(self.pantalla, GREEN,
#                              texto_comodin_multiplicar_puntos_rect)

#         return texto_comodin_tiempo_extra_rect, texto_comodin_menos_votada_rect, texto_comodin_multiplicar_puntos_rect

#     def click_comodin(self, pos):
#         comodin_tiempo_extra, comodin_menos_votada, comodin_multiplicar_puntos = self.mostrar_comodines()
#         if comodin_tiempo_extra.collidepoint(pos) and self.used_hints["tiempo_extra"]:
#             self.comodin_tiempo_extra()
#         if comodin_menos_votada.collidepoint(pos) and self.used_hints["menos_votada"]:
#             self.mostrar_menos_votada()
#         if comodin_multiplicar_puntos.collidepoint(pos) and self.used_hints["multiplicar_puntos"]:
#             self.comodin_multiplicar_puntos()

#     def comodin_tiempo_extra(self):
#         if self.used_hints["tiempo_extra"]:
#             self.tiempo_restante += 10
#             self.used_hints["tiempo_extra"] = False

#     def comodin_multiplicar_puntos(self):
#         if self.used_hints["multiplicar_puntos"]:
#             self.bonus_multiplicar = 2
#             self.used_hints["multiplicar_puntos"] = False

#     def mostrar_respuestas(self):
#         y_offset = 200
#         for respuesta, puntaje in self.pregunta_actual["respuestas"].items():
#             texto_respuesta = self.font.render(
#                 f"{respuesta}: {puntaje}", True, (255, 255, 255))
#             texto_respuesta_rect = texto_respuesta.get_rect()
#             texto_respuesta_rect.topleft = (100, y_offset)
#             pygame.draw.rect(self.pantalla, (0, 0, 255), texto_respuesta_rect)
#             self.pantalla.blit(texto_respuesta, texto_respuesta_rect)
#             y_offset += 50

#     def mostrar_menos_votada(self):
#         respuestas = self.pregunta_actual["respuestas"]
#         menos_votada = min(respuestas, key=respuestas.get)
#         texto_menos_votada = self.font.render(
#             f"Menos Votada: {menos_votada}", True, (255, 255, 255))
#         self.pantalla.blit(texto_menos_votada, (100, 300))

#     def mostrar_puntaje(self):
#         texto_puntaje = self.font.render(
#             f"Puntos: {self.puntaje}", True, WHITE)
#         texto_puntaje_rect = texto_puntaje.get_rect()
#         texto_puntaje_rect.topright = (SCREEN_WIDTH - 400, 500)
#         circle_center = (texto_puntaje_rect.x + texto_puntaje_rect.width //
#                          2, texto_puntaje_rect.y + texto_puntaje_rect.height // 2)
#         pygame.draw.circle(self.pantalla, BLACK, circle_center, RADIUS_Puntaje)
#         pygame.draw.circle(self.pantalla, YELLOW,
#                            circle_center, RADIUS_Puntaje, WIDTH)
#         self.pantalla.blit(texto_puntaje, texto_puntaje_rect)

#     def actualizar_estado_juego(self):
#         self.tiempo_restante -= 1 / 60
#         if self.tiempo_restante <= 0:
#             self.oportunidades -= 1
#             self.seleccionar_pregunta_aleatoriamente()
#             self.input_respuesta = ""
#             self.tiempo_restante = RESPONSE_TIME
#             if self.oportunidades <= 0:
#                 self.mostrar_game_over()
#                 pygame.time.wait(1000)
#                 self.resetear_juego()

#     def mostrar_game_over(self):
#         texto_game_over = self.font.render(
#             "¡Juego Terminado!", True, WHITE, RED)
#         self.pantalla.blit(texto_game_over, (SCREEN_WIDTH //
#                            2 - 100, SCREEN_HEIGHT // 2))
#         self.pantalla.blit(self.cruz_roja_gif, (100, 100))

#     def run(self):
#         running = True
#         self.seleccionar_pregunta_aleatoriamente()
#         while running:
#             self.pantalla.blit(self.fondo_preguntas, (0, 0))
#             self.mostrar_pregunta()
#             self.mostrar_reloj()
#             self.mostrar_puntaje()
#             self.mostrar_input()
#             self.actualizar_estado_juego()
#             self.mostrar_comodines()
#             # self.mostrar_respuestas()
#             # self.mostrar_menos_votada()

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_RETURN:
#                         self.chequear_respuesta(self.input_respuesta)
#                     elif event.key == pygame.K_BACKSPACE:
#                         self.input_respuesta = self.input_respuesta[:-1]
#                     else:
#                         self.input_respuesta += event.unicode
#                 if event.type == pygame.MOUSEBUTTONDOWN:
#                     pos = pygame.mouse.get_pos()
#                     self.click_comodin(pos)

#             pygame.display.flip()
#             self.clock.tick(60)

#         pygame.quit()
#         sys.exit()


# if __name__ == "__main__":
#     juego = Juego100ARG()
#     juego.run()
