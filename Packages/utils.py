import pygame
import json

# ---------------------------------------------------------
"""
Carga una imagen desde la ruta especificada y la redimensiona al tamaño deseado.

Args:
    path (str): Ruta de la imagen a cargar.
    width (int): Ancho deseado de la imagen.
    height (int): Alto deseado de la imagen.

Returns:
    pygame.Surface: Superficie de la imagen cargada y redimensionada.
"""


def cargar_imagen(path, width, height):
    imagen = pygame.image.load(path)
    return pygame.transform.scale(imagen, (width, height))


# ---------------------------------------------------------
"""
Renderiza texto en una superficie dada con un fondo rectángular coloreado.

    Args:
        pantalla (pygame.Surface): Superficie donde se dibujará el texto.
        texto (str): Texto a renderizar.
        font (pygame.font.Font): Fuente del texto.
        color (tuple): Color del texto en formato RGB.
        posicion (tuple): Posición (x, y) donde se ubicará el texto.
        padding (int, optional): Espacio adicional alrededor del texto para el fondo. Default es 10.

    Returns:
        None
"""


def renderizar_texto(pantalla, texto, font, color, posicion, padding=10):
    texto_render = font.render(texto, True, color)
    texto_rect = texto_render.get_rect()
    texto_rect.topleft = posicion
    fondo = pygame.Rect(texto_rect.x - padding, texto_rect.y - padding,
                        texto_rect.width + 2 * padding, texto_rect.height + 2 * padding)
    pygame.draw.rect(pantalla, (0, 0, 255), fondo)  # Fondo azul
    pantalla.blit(texto_render, texto_rect)


# ---------------------------------------------------------
"""
Carga un archivo JSON desde la ruta especificada.
Args:
    ruta_archivo (str): Ruta del archivo JSON a cargar.
Returns:
    dict: Datos cargados desde el archivo JSON.
"""


def cargar_archivo_json(ruta_archivo):
    with open("json\preguntas.json", "r",  encoding="utf-8") as preguntas_json:
        pregunta = json.load(preguntas_json)
        return pregunta


# ---------------------------------------------------------
"""
Renderiza y dibuja texto en una superficie dada en la posición especificada.

Args:
    texto (str): Texto a renderizar.
    font (pygame.font.Font): Fuente del texto.
    color (tuple): Color del texto en formato RGB.
    surface (pygame.Surface): Superficie donde se dibujará el texto.
    x (int): Coordenada X de la posición del texto.
    y (int): Coordenada Y de la posición del texto.

Returns:
    None
"""


def escribir_texto(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
