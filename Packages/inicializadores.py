import pygame
from .config import *
from .utils import *


def inicializar_pygame():
    pygame.init()


def cargar_sonidos():
    audio_correcto = pygame.mixer.Sound("assets/sounds/correcto.mp3")
    audio_incorrecto = pygame.mixer.Sound("assets/sounds/error.mp3")
    return audio_correcto, audio_incorrecto


def inicializar_pantalla():
    pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("100 Argentinos dicen")
    return pantalla


def cargar_fuente():
    return pygame.font.Font(FONT_PATH1, FONT_SIZE)


def cargar_imagenes():
    fondo_menu = cargar_imagen(
        "assets/imgs/fondo_menu2.jpg", SCREEN_WIDTH, SCREEN_HEIGHT)
    fondo_preguntas = cargar_imagen(
        "assets/imgs/Fondo_Juego_100Arg.png", SCREEN_WIDTH, SCREEN_HEIGHT)
    fondo_game_over = cargar_imagen(
        "assets/imgs/Fondo_de_Pantalla_con_Frase_e_Imagen_.jpg", SCREEN_WIDTH, SCREEN_HEIGHT)
    cruz_roja_gif = cargar_imagen("assets/imgs/cruz_roja.gif", 100, 100)
    return fondo_menu, fondo_preguntas, fondo_game_over, cruz_roja_gif


def inicializar_variables():
    return {
        'input_respuesta': "",
        'puntaje': 0,
        'contador_rondas': 0,
        'rondas_jugadas': 0,
        'max_rondas': 1,
        'comodin_usado': False,
        'oportunidades': 3,
        'preguntas': cargar_archivo_json("json\preguntas.json"),
        'respuestas_ingresadas': [],
        'puntajes_acumulados': [],
        'partidas_jugadas': 0
    }
