import sys
import random
import pygame
from .config import *
from .utils import *
from .boton import Boton
from .puntaje import Puntaje
from .fondo import Fondo
from .reloj import Reloj
from .entrada_texto import EntradaTexto
from .comodin import Comodin


class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("100 Argentinos dicen")
        self.font = pygame.font.Font(FONT_PATH1, FONT_SIZE)
        self.clock = pygame.time.Clock()
        self.resetear_juego()

    def resetear_juego(self):
        self.puntaje = Puntaje(self.font, self.pantalla)
        self.oportunidades = 3
        self.pregunta_actual = None
        self.reloj = Reloj(self.font, self.pantalla)
        self.entrada_texto = EntradaTexto(self.font, self.pantalla)
        self.fondo_menu = Fondo("assets/imgs/fondo_menu2.jpg", self.pantalla)
        self.fondo_preguntas = Fondo(
            "assets/imgs/fondo_instrucciones.jpg", self.pantalla)
        self.cruz_roja = Fondo("assets/imgs/cruz_roja.gif", self.pantalla)
        self.comodines = [
            Comodin("Tiempo Extra", (100, 500),
                    BLUE, self.font, self.pantalla),
            Comodin("Menos Votada", (100, 530),
                    BLUE, self.font, self.pantalla),
            Comodin("Multiplicar Puntos", (100, 560),
                    BLUE, self.font, self.pantalla)
        ]

    def seleccionar_preguntar_aleatoriamente(self):
        self.pregunta_actual = random.choice(
            cargar_archivo_json("data/preguntas.json"))
        self.reloj.tiempo_restante = RESPONSE_TIME

    def mostrar_pregunta(self):
        texto_pregunta = self.font.render(
            self.pregunta_actual["pregunta"] + "?", True, WHITE)
        pregunta_rect = texto_pregunta.get_rect(topleft=(100, 300))
        padding = 10
        fondo_pregunta = pygame.Rect(pregunta_rect.x - padding, pregunta_rect.y - padding,
                                     pregunta_rect.width + 2 * padding, pregunta_rect.height + 2 * padding)
        pygame.draw.rect(self.pantalla, BLUE, fondo_pregunta)
        self.pantalla.blit(texto_pregunta, pregunta_rect)

    def chequear_respuesta(self, input_respuesta):
        respuestas = self.pregunta_actual["respuestas"]
        if input_respuesta in respuestas:
            self.puntaje.agregar_puntos(
                respuestas[input_respuesta] * (2 if self.comodines[2].usado else 1))
        elif input_respuesta == "tiempo_extra":
            self.comodines[0].activar()
            self.reloj.tiempo_restante += 10
        elif self.comodines[1].usado:
            self.puntaje.agregar_puntos(
                respuestas[min(respuestas, key=respuestas.get)])
        else:
            self.oportunidades -= 1
            self.cruz_roja.dibujar()
            pygame.display.flip()
            pygame.time.wait(1000)
        self.seleccionar_preguntar_aleatoriamente()
        self.entrada_texto.texto = ""
        self.reloj.tiempo_restante = RESPONSE_TIME

    def mostrar_comodines(self):
        for comodin in self.comodines:
            comodin.dibujar()

    def click_comodin(self, pos):
        for comodin in self.comodines:
            if comodin.colisiona(pos):
                comodin.activar()

    def actualizar_estado_juego(self):
        self.reloj.actualizar(1 / 60)
        if self.reloj.tiempo_restante <= 0:
            self.oportunidades -= 1
            self.seleccionar_preguntar_aleatoriamente()
            self.entrada_texto.texto = ""
            self.reloj.tiempo_restante = RESPONSE_TIME
            if self.oportunidades <= 0:
                self.mostrar_game_over()
                pygame.time.wait(1000)
                self.resetear_juego()

    def mostrar_game_over(self):
        texto_game_over = self.font.render("¡Juego Terminado!", True, BLACK)
        self.pantalla.blit(texto_game_over, (SCREEN_WIDTH //
                           2 - 100, SCREEN_HEIGHT // 2))

    def run(self):
        running = True
        self.seleccionar_preguntar_aleatoriamente()

        while running:
            self.fondo_preguntas.dibujar()
            self.mostrar_pregunta()
            self.reloj.dibujar()
            self.puntaje.dibujar()
            self.entrada_texto.dibujar()
            self.actualizar_estado_juego()
            self.mostrar_comodines()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    input_respuesta = self.entrada_texto.manejar_evento(event)
                    if input_respuesta:
                        self.chequear_respuesta(input_respuesta)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click_comodin(event.pos)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
