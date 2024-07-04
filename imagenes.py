# Cargar imagenes
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT


def cargar_imagenes(self):
    self.fondo_menu = self.cargar_imagen(
        "assets/imgs/fondo_menu2.jpg", SCREEN_WIDTH, SCREEN_HEIGHT)
    self.fondo_preguntas = self.cargar_imagen(
        "assets/imgs/Fondo_Juego_100Arg.png", SCREEN_WIDTH, SCREEN_HEIGHT)
    self.cruz_roja_gif = self.cargar_imagen(
        "assets/imgs/cruz_roja.gif", SCREEN_WIDTH, SCREEN_HEIGHT)
    self.cruz_error = self.cargar_imagen(
        "assets/imgs/cruz_error.png", 100, 100)


def cargar_imagen(self, ruta, ancho, alto):
    imagen = pygame.image.load(ruta)
    imagen = pygame.transform.scale(imagen, (ancho, alto))
    return imagen
