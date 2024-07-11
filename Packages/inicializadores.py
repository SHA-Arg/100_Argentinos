import pygame
from .config import *
from .utils import *

# ----------------------------------------------------


def inicializar_pygame():
    """
Esta función debe ser llamada al inicio del programa para inicializar
    todas las funcionalidades de Pygame necesarias para el juego.
"""
    pygame.init()


# ----------------------------------------------------
def cargar_sonidos():
    """

    Esta función carga y devuelve dos objetos de sonido: uno para el efecto de sonido
    de respuesta correcta y otro para el efecto de sonido de respuesta incorrecta.

    Retorna:
    - audio_correcto: Objeto de sonido para el efecto de respuesta correcta.
    - audio_incorrecto: Objeto de sonido para el efecto de respuesta incorrecta.
"""
    audio_correcto = pygame.mixer.Sound("assets/sounds/correcto.mp3")
    audio_incorrecto = pygame.mixer.Sound("assets/sounds/error.mp3")
    audio_comodin = pygame.mixer.Sound("assets/sounds/ButtonClick.mp3")
    return audio_correcto, audio_incorrecto, audio_comodin


# ----------------------------------------------------
def inicializar_pantalla():

    pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("100 Argentinos dicen")
    return pantalla


# ----------------------------------------------------
def cargar_fuente():
    """
Carga la fuente utilizada para renderizar texto en el juego.

    Retorna:
    - pygame.font.Font: Objeto de fuente cargado desde el archivo especificado.
"""
    return pygame.font.Font(FONT_PATH1, FONT_SIZE)


# ----------------------------------------------------
def cargar_imagenes():
    """
sta función carga varias imágenes necesarias para diferentes fondos y elementos del juego.

    Retorna:
    - fondo_menu: Imagen de fondo para el menú principal del juego.
    - fondo_preguntas: Imagen de fondo para la pantalla de juego de preguntas.
    - fondo_game_over: Imagen de fondo para la pantalla de juego terminado.
    - cruz_roja_gif: Imagen animada de una cruz roja utilizada en el juego.
"""
    fondo_menu = cargar_imagen(
        "assets/imgs/fondo_menu2.jpg", SCREEN_WIDTH, SCREEN_HEIGHT)
    fondo_preguntas = cargar_imagen(
        "assets/imgs/Fondo_Juego_100Arg.png", SCREEN_WIDTH, SCREEN_HEIGHT)
    fondo_game_over = cargar_imagen(
        "assets/imgs/Fondo_de_Pantalla_con_Frase_e_Imagen_.jpg", SCREEN_WIDTH, SCREEN_HEIGHT)
    cruz_roja_gif = cargar_imagen("assets/imgs/cruz_roja.gif", 100, 100)
    return fondo_menu, fondo_preguntas, fondo_game_over, cruz_roja_gif


# ----------------------------------------------------
def inicializar_variables():
    """
Esta función devuelve un diccionario con las variables iniciales necesarias para
    iniciar el juego, como el texto de entrada, puntaje, rondas jugadas, etc.

    Retorna:
    - dict: Diccionario con las variables iniciales del juego.
"""
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
