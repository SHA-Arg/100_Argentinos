import pygame
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
RESPONSE_TIME = 10
# en segundos

# Puntuación necesaria para ganar el premio mayor
WINNING_SCORE = 500

# Radio y ancho del círculo del reloj de cuenta regresiva y del puntaje
RADIUS = 50
WIDTH = 5

# Frames Per Second
FPS = 60


# MUSICA
MUSIC_PATH = 'assets\sounds\CORTINA MUSICAL.mp3'
pygame.mixer.init()
pygame.mixer.music.load(MUSIC_PATH)
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

# ------------------------------------------------------
