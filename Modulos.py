import json
import pygame
import csv


# ------------------------------------------------------
# Renderizamos el texto, obtenemos el rectangulo del mismo, centramos el rectangulo y dibujamos el texto en la superficie


def draw_text(surface, text, font, color, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
# ------------------------------------------------------
# Eliminamos los espacios y convertimos en minuscula


def normalizar_respuesta(respuesta):
    return respuesta.strip().lower()
# ------------------------------------------------------
# Abrimos el csv en modo "append", creamos el escritor csv y escribimos los puntajes en una nueva fila


def guardar_puntaje(puntaje):
    with open('puntajes.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([puntaje])
# ------------------------------------------------------
# Abrimos archivo Json y cargamos y devolvemos los datos del mismo
