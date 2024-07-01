import json
import pygame


def cargar_imagen(ruta, ancho, alto):
    imagen = pygame.image.load(ruta)
    return pygame.transform.scale(imagen, (ancho, alto))


def cargar_archivo_json(ruta_archivo):
    with open("preguntas.json", "r",  encoding="utf-8") as preguntas_json:
        pregunta = json.load(preguntas_json)
        return pregunta


if __name__ == "__main__":
    ruta_archivo = "preguntas.json"
