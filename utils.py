import pygame
import json


def cargar_imagen(path, width, height):
    imagen = pygame.image.load(path)
    return pygame.transform.scale(imagen, (width, height))


def renderizar_texto(pantalla, texto, font, color, posicion, padding=10):
    texto_render = font.render(texto, True, color)
    texto_rect = texto_render.get_rect()
    texto_rect.topleft = posicion
    fondo = pygame.Rect(texto_rect.x - padding, texto_rect.y - padding,
                        texto_rect.width + 2 * padding, texto_rect.height + 2 * padding)
    pygame.draw.rect(pantalla, (0, 0, 255), fondo)  # Fondo azul
    pantalla.blit(texto_render, texto_rect)


def cargar_archivo_json(ruta_archivo):
    with open("preguntas.json", "r",  encoding="utf-8") as preguntas_json:
        pregunta = json.load(preguntas_json)
        return pregunta
