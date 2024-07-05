import pygame
import random
from .utils import *
# Dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fuente
FONT_PATH1 = 'assets/fonts/Roboto-Bold.ttf'
FONT_SIZE = 21
FONT_PATH2 = 'assets/fonts/Roboto-Bold.ttf'
FONT_INSTRUCCIONES = 15
RADIUS_Time = 30
RADIUS_Puntaje = 60

# Tiempo de respuesta
RESPONSE_TIME = 30
# en segundos

# Puntuación necesaria para ganar el premio mayor
WINNING_SCORE = 500

# Radio y ancho del círculo del reloj de cuenta regresiva y del puntaje
RADIUS = 50
WIDTH = 5

# Frames Per Second
FPS = 60


# # MUSICA
# MUSIC_PATH = 'assets\sounds\se-acabo-todo.mp3'
# pygame.mixer.init()
# pygame.mixer.music.load(MUSIC_PATH)
# pygame.mixer.music.set_volume(0.5)
# pygame.mixer.music.play(-1)

# ------------------------------------------------------
# Variables globales

# audio_correcto = pygame.mixer.Sound("assets\sounds\correcto.mp3")
# audio_incorrecto = pygame.mixer.Sound("assets\sounds\error.mp3")
# pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("100 Argentinos dicen")
# # font = pygame.font.Font(FONT_PATH1, FONT_SIZE)
# clock = pygame.time.Clock()
# font_instrucciones = pygame.font.Font(FONT_PATH2, FONT_INSTRUCCIONES)
# # # ------------------------------------------------------
# # # Dimensiones de la pantalla
# pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption('100 Argentinos dicen')
# # # ------------------------------------------------------

# puntaje = 0
# tiempo_restante = RESPONSE_TIME
# bonus_multiplicar = 1
# used_hints = {
#     "tiempo_extra": False,
#     "menos_votada": False,
#     "multiplicar_puntos": False
# }
# input_respuesta = ""
# contador_rondas = 0
# rondas_jugadas = 0
# max_rondas = 5
# comodin_usado = False
# oportunidades = 3
# preguntas = cargar_archivo_json("preguntas.json")
# respuestas_ingresadas = []
# puntajes_acumulados = []
# partidas_jugadas = 0
# pregunta_actual = random.choice(preguntas)
# respuestas = pregunta_actual["respuestas"]
