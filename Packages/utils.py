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
    with open("json\preguntas.json", "r",  encoding="utf-8") as preguntas_json:
        pregunta = json.load(preguntas_json)
        return pregunta


def escribir_texto(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# import pygame
# import json

# # ------------------------------------------------------
# # unción para cargar una imagen e imprimirlas en las dimensiones especificadas


# def cargar_imagen(self,path, width, height):
#     imagen = pygame.image.load(path)
#     return pygame.transform.scale(imagen, (width, height))

# # ------------------------------------------------------
# # Función para renderizar texto en la pantalla con un fondo azul.


# def renderizar_texto(pantalla, texto, font, color, posicion, padding=10):
#     texto_render = font.render(texto, True, color)
#     texto_rect = texto_render.get_rect()
#     texto_rect.topleft = posicion
#     fondo = pygame.Rect(texto_rect.x - padding, texto_rect.y - padding,
#                         texto_rect.width + 2 * padding, texto_rect.height + 2 * padding)
#     pygame.draw.rect(pantalla, (0, 0, 255), fondo)  # Fondo azul
#     pantalla.blit(texto_render, texto_rect)

# # ------------------------------------------------------
# # Función para cargar datos desde un archivo JSON.


# def cargar_archivo_json(self, path):
#     with open("preguntas.json", "r",  encoding="utf-8") as preguntas_json:
#         pregunta = json.load(preguntas_json)
#         return pregunta

# # ------------------------------------------------------
# # Renderizamos el texto, obtenemos el rectangulo del mismo, centramos el rectangulo y dibujamos el texto en la superficie


# def escribir_texto(text, font, color, surface, x, y):
#     textobj = font.render(text, True, color)
#     textrect = textobj.get_rect()
#     textrect.center = (x, y)
#     surface.blit(textobj, textrect)

# # ------------------------------------------------------
# # Eliminamos los espacios y convertimos en minuscula


# def normalizar_respuesta(respuesta):
#     return respuesta.strip().lower()

# # ------------------------------------------------------
# # Abrimos el csv en modo "append", creamos el escritor csv y escribimos los puntajes en una nueva fila

# # def guardar_puntaje(puntaje):
# #     with open('puntajes.csv', mode='a', newline='') as file:
# #         writer = csv.writer(file)
# #         writer.writerow([puntaje])

# # ------------------------------------------------------


# def limpiar_input_respuesta():
#     input_respuesta = ""
