import sys
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
        self.input_text = ""

    def seleccionar_preguntar_aleatoriamente(self):
        self.pregunta_actual = random.choice(PREGUNTAS)
        self.tiempo_restante = RESPONSE_TIME

    def mostrar_pregunta(self):
        texto_pregunta = self.font.render(
            self.pregunta_actual["pregunta"], True, BLACK)
        self.screen.blit(texto_pregunta, (50, 50))

    def mostrar_input_usuario(self):
        input_box = pygame.Rect(50, 100, 700, 50)
        pygame.draw.rect(self.screen, BLACK, input_box, 2)
        texto_input = self.font.render(self.input_text, True, BLACK)
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

    def chequear_respuesta(self, respuesta):
        respuestas = self.pregunta_actual["respuestas"]
        if respuesta in [resp.lower() for resp in respuestas]:
            self.puntaje += respuestas[respuesta.capitalize()] * \
                self.bonus_multiplicar
            self.bonus_multiplicar = 1  # Reset multiplier
            return True
        return False

    def actualizar_estado_juego(self):
        # Actualizar el estado del juego, manejar oportunidades, tiempo restante, etc.
        self.tiempo_restante -= 1 / 60
        if self.tiempo_restante <= 0:
            self.oportunidades -= 1
            self.seleccionar_preguntar_aleatoriamente()
            self.input_text = ""
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
            self.screen.fill(WHITE)
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
                    else:
                        self.oportunidades -= 1
                        if self.oportunidades <= 0:
                            self.mostrar_game_over()
                            pygame.time.wait(3000)
                            self.resetear_juego()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    juego = Juego100ARG()
    juego.run()


# import pygame
# import sys

# # Inicializa Pygame
# pygame.init()

#     # Colores
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# BLUE = (0, 0, 255)

# # Dimensiones de la pantalla
# WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption('Juego 100 Argentinos dicen')

# # Fuente
# font = pygame.font.Font(None, 36)


# def draw_text(text, font, color, surface, x, y):
#     textobj = font.render(text, True, color)
#     textrect = textobj.get_rect()
#     textrect.center = (x, y)
#     surface.blit(textobj, textrect)


# def main_menu():
#     while True:
#         screen.fill(WHITE)

#         draw_text('Juego 100 Argentinos dicen', font, BLACK,
#                   screen, WIDTH // 2, HEIGHT // 4)

#         mx, my = pygame.mouse.get_pos()

#         button_1 = pygame.Rect(WIDTH // 3, HEIGHT // 2, 200, 50)
#         button_2 = pygame.Rect(WIDTH // 3, HEIGHT // 2 + 70, 200, 50)
#         button_3 = pygame.Rect(WIDTH // 3, HEIGHT // 2 + 140, 200, 50)

#         if button_1.collidepoint((mx, my)):
#             if click:
#                 game()
#         if button_2.collidepoint((mx, my)):
#             if click:
#                 instructions()
#         if button_3.collidepoint((mx, my)):
#             if click:
#                 pygame.quit()
#                 sys.exit()

#         pygame.draw.rect(screen, BLUE, button_1)
#         pygame.draw.rect(screen, BLUE, button_2)
#         pygame.draw.rect(screen, BLUE, button_3)

#         draw_text('Jugar', font, WHITE, screen,
#                   button_1.centerx, button_1.centery)
#         draw_text('Instrucciones', font, WHITE, screen,
#                   button_2.centerx, button_2.centery)
#         draw_text('Salir', font, WHITE, screen,
#                   button_3.centerx, button_3.centery)

#         click = False
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 1:
#                     click = True

#         pygame.display.update()


# def game():
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#         screen.fill(WHITE)
#         draw_text('El juego a comenzado', font, BLACK,
#                   screen, WIDTH // 2, HEIGHT // 2)

#         pygame.display.update()


# def instructions():
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#         screen.fill(WHITE)
#         draw_text('Instrucciones del juego', font,
#                   BLACK, screen, WIDTH // 2, HEIGHT // 2)
#         draw_text('Presiona ESC para volver al menú', font,
#                   BLACK, screen, WIDTH // 2, HEIGHT // 2 + 50)

#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_ESCAPE]:
#             running = False

#         pygame.display.update()


# main_menu()
