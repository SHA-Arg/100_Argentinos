# resources.py
import pygame
from .config import SCREEN_WIDTH, SCREEN_HEIGHT, FONT_PATH1, FONT_PATH2, FONT_SIZE, FONT_INSTRUCCIONES, BLUE, WHITE


# Inicializar Pygame
pygame.init()

# Fuente
font = pygame.font.Font(FONT_PATH1, FONT_SIZE)
font_instrucciones = pygame.font.Font(FONT_PATH2, FONT_INSTRUCCIONES)

# Dimensiones de la pantalla
pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('100 Argentinos dicen')

# Cargar imágenes de fondo
fondo_menu = pygame.image.load("assets/imgs/fondo_menu2.jpg")
fondo_menu = pygame.transform.scale(fondo_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))

fondo_instrucciones = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
fondo_instrucciones.fill(BLUE)

# ------------------------------------------------------------
