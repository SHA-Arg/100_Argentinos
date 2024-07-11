import pygame
import sys
import csv
from .config import *
from .ordenamiento import *
from .utils import *
from .inicializadores import *
from .main import *
"""
    Muestra el campo de entrada de texto en la pantalla del juego.

    Este método dibuja un rectángulo que representa el campo de entrada de texto y 
    muestra el texto actualmente ingresado por el usuario dentro de dicho rectángulo.

    Parámetros:
    - juego: Una instancia del objeto del juego que contiene los atributos necesarios 
    - como la pantalla y el texto de entrada.

    Acciones realizadas:
    - Dibuja un rectángulo blanco que representa el campo de entrada de texto.
    - Renderiza el texto actualmente ingresado por el usuario y lo muestra dentro del rectángulo.
    - Actualiza la porción de la pantalla donde se encuentra el campo de entrada de texto
"""


def mostrar_input(juego):
    input_respuesta_rect = pygame.Rect(70, 110, 500, 50)
    pygame.draw.rect(juego.pantalla, WHITE, input_respuesta_rect, 2)
    texto_input = juego.font.render(juego.input_respuesta, True, WHITE)
    juego.pantalla.blit(
        texto_input, (input_respuesta_rect.x + 5, input_respuesta_rect.y + 5))

    pygame.display.update(input_respuesta_rect)

# ---------------------------------------------------------


"""
Este método renderiza el texto que indica el número de rondas jugadas y lo muestra
    en una posición específica de la pantalla del juego.

    Parámetros:
    - juego: Una instancia del objeto del juego que contiene los atributos necesarios 
    - como la pantalla y el número de rondas jugadas.

    Atributos utilizados:
    - juego.pantalla: La superficie de Pygame donde se dibuja el texto.
    - juego.rondas_jugadas (int): El número de rondas que se han jugado.
    - juego.font: La fuente utilizada para renderizar el texto.
"""


def mostrar_rondas_jugadas(juego):
    texto_rondas = juego.font.render(
        f"Rondas jugadas: {juego.rondas_jugadas}", True, WHITE)
    texto_rondas_rect = texto_rondas.get_rect()
    texto_rondas_rect.topleft = (SCREEN_WIDTH - 370, 550)
    juego.pantalla.blit(texto_rondas, texto_rondas_rect)


# ---------------------------------------------------------

    """
    Muestra la pregunta actual en la pantalla del juego. Este método verifica si hay una pregunta seleccionada. Si no hay ninguna pregunta, lanza un ValueError

    Args:
        None

    Returns:
        None
    """


def mostrar_pregunta(juego):
    texto_pregunta = juego.font.render(
        juego.pregunta_actual["pregunta"] + "?", True, WHITE)
    pregunta_rect = texto_pregunta.get_rect()
    pregunta_rect.topleft = (20, 60)
    padding = 10
    fondo_pregunta = pygame.Rect(pregunta_rect.x - padding, pregunta_rect.y - padding,
                                 pregunta_rect.width + 2 * padding, pregunta_rect.height + 2 * padding)
    pygame.draw.rect(juego.pantalla, BLUE, fondo_pregunta)
    juego.pantalla.blit(texto_pregunta, pregunta_rect)

    print(juego.pregunta_actual["respuestas"])


# ---------------------------------------------------------
    """
    Muestra el reloj de tiempo restante en la pantalla del juego. Este método renderiza el tiempo restante en segundos en la esquina superior izquierda de la pantalla.

    Args:
        None

    Returns:
        None
    """


def mostrar_reloj(juego):

    texto_reloj = juego.font.render(
        f"{int(juego.tiempo_restante)}s", True, WHITE)
    texto_reloj_rect = texto_reloj.get_rect()
    texto_reloj_rect.topleft = (SCREEN_WIDTH - 780, 120)
    circle_center = (texto_reloj_rect.x + texto_reloj_rect.width //
                     2, texto_reloj_rect.y + texto_reloj_rect.height // 2)

    pygame.draw.circle(juego.pantalla, BLACK, circle_center, RADIUS_Time)
    pygame.draw.circle(juego.pantalla, YELLOW,
                       circle_center, RADIUS_Time, WIDTH)
    juego.pantalla.blit(texto_reloj, texto_reloj_rect)

    if juego.tiempo_restante <= 5:

        pygame.draw.circle(juego.pantalla, RED,
                           circle_center, RADIUS_Time, WIDTH)


# ---------------------------------------------------------
    """
    Muestra las respuestas ingresadas ordenadas en la pantalla del juego. Este método ordena las respuestas ingresadas por puntaje usando la función `ordenar_respuestas`

    Args:
        None

    Returns:
        None
    """


def mostrar_respuestas_ingresadas(juego):
    respuestas_ordenadas = ordenar_respuestas(juego.respuestas_ingresadas)

    y_offset = 200
    for respuesta, puntos in respuestas_ordenadas:
        texto_respuesta = juego.font.render(
            f"{respuesta}: {puntos}", True, WHITE)
        texto_respuesta_rect = texto_respuesta.get_rect()
        texto_respuesta_rect.topleft = (100, y_offset)

        pygame.draw.rect(juego.pantalla, BLUE, texto_respuesta_rect)
        juego.pantalla.blit(texto_respuesta, texto_respuesta_rect)

        y_offset += 30


# ---------------------------------------------------------
"""
Este método muestra un mensaje de fin de juego en la pantalla y permite al jugador 
    ingresar su nombre a través del teclado. El nombre ingresado se devuelve cuando 
    el jugador presiona la tecla Enter.

    Parámetros:
    - juego: Una instancia del objeto del juego que contiene los atributos necesarios 
    - como la pantalla, la fuente para renderizar el texto, y el fondo de "game over".

    Retorna:
    - str: El nombre ingresado por el jugador.

"""


def pedir_nombre_jugador(juego):
    nombre = ""
    pedir_nombre = True
    while pedir_nombre:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pedir_nombre = False
                elif event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    nombre += event.unicode

        # Renderizar y mostrar el nombre ingresado
        juego.pantalla.blit(juego.fondo_game_over, (0, 0))
        texto_pedir_nombre = juego.font.render(
            "Ingrese su nombre:", True, WHITE)
        texto_nombre = juego.font.render(nombre, True, WHITE)
        juego.pantalla.blit(texto_pedir_nombre, (50, SCREEN_HEIGHT // 2 - 50))
        juego.pantalla.blit(texto_nombre, (50, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.display.update()
    return nombre


"""
Este método lee los datos del ranking desde un archivo CSV, los ordena y los muestra
    en una lista en la pantalla del juego.

    Parámetros:
    - juego: Una instancia del objeto del juego que contiene los atributos necesarios 
    - como la pantalla y la fuente para renderizar el texto.

    Notas:
    - Se asume que el archivo CSV está ubicado en la ruta 'data/ranking.csv' y contiene
    - los datos del ranking en un formato adecuado.
    - La función `ordenar_respuestas` debe estar definida y ser capaz de ordenar los datos del ranking.
"""


def mostrar_ranking(juego):
    with open('data/ranking.csv', 'r') as file:
        reader = csv.reader(file)

        # ranking = sorted(reader, key=lambda x: int(x[1]), reverse=True)
        ranking = ordenar_ranking(list(reader))

        y_offset = 100
        for i, row in enumerate(ranking):
            texto_ranking = juego.font.render(
                f"{i+1}. {row[0]}: {row[1]} puntos", True, WHITE)
            texto_ranking_rect = texto_ranking.get_rect()
            texto_ranking_rect.topleft = (50, y_offset)
            juego.pantalla.blit(texto_ranking, texto_ranking_rect)
            y_offset += 40


# ---------------------------------------------------------
# ---------------------------------------------------------
"""
    Muestra la pantalla final del juego y gestiona la respuesta del jugador.Este método muestra el fondo de pantalla de juego terminado y un mensaje para preguntar al jugador si desea jugar otra vez.

    Args:
        None

    Returns:
        None
    """


def mostrar_pantalla_final(juego):
    # Mostrar fondo de pantalla final
    juego.pantalla.blit(juego.fondo_game_over, (0, 0))

    # Calcular puntaje total
    pozo_acumulado = 0
    mensaje = ""
    # Asegurarse de que se esté trabajando con el total
    total_puntajes_acumulados = sum(juego.puntajes_acumulados)

    if total_puntajes_acumulados == 500:
        juego.premio = 1000000
        mensaje = f"Usted ganó el gran premio de ${juego.premio}"

    elif total_puntajes_acumulados == 0:
        mensaje = f" Usted ha perdido, no ganó nada! ${pozo_acumulado}\n"

    else:
        pozo_acumulado = total_puntajes_acumulados * 500
        mensaje = f" Usted ganó  ${pozo_acumulado}"

        juego.pantalla.blit(juego.fondo_game_over, (0, 0))

    # Pedir nombre del jugador
    nombre_jugador = pedir_nombre_jugador(juego)

    # Guardar puntaje
    guardar_puntaje(nombre_jugador, mensaje)
    pygame.display.flip()
    # Mostrar ranking actualizado
    mostrar_ranking(juego)

    pygame.display.flip()
    texto_pantalla_final = juego.font.render(
        "¡Juego terminado! ¿Deseas jugar otra vez? (S/N)", True, WHITE)
    texto_pantalla_final_rect = texto_pantalla_final.get_rect()
    texto_pantalla_final_rect.topleft = (50, 50)
    juego.pantalla.blit(texto_pantalla_final, texto_pantalla_final_rect)
    # Preguntar si desea jugar otra vez
    esperando_respuesta = True
    while esperando_respuesta:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    juego.resetear_juego()
                    esperando_respuesta = False
                elif event.key == pygame.K_n:
                    mostrar_pantalla_agradecimiento(juego)
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


# ---------------------------------------------------------
    """
    Muestra una animación de cruz roja en la pantalla del juego. Este método posiciona y muestra una animación de cruz roja

    Args:
        None

    Returns:
        None
    """

# ---------------------------------------------------------


def mostrar_animacion_cruz(juego):
    cruz_rect = juego.cruz_roja_gif.get_rect()
    cruz_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    juego.pantalla.blit(juego.cruz_roja_gif, cruz_rect)
    pygame.display.update()
    pygame.time.delay(1000)


# ---------------------------------------------------------
"""
Muestra los comodines disponibles en la pantalla del juego. Este método los diferentes comodines disponibles.

Args:
    None

    Returns:
        None
"""


def mostrar_comodines(juego):

    texto_comodin_tiempo_extra = juego.font.render(
        "Tiempo extra", True, WHITE)
    texto_comodin_menos_votada = juego.font.render(
        "Menos votada", True, WHITE)
    texto_comodin_multiplicar_puntos = juego.font.render(
        "Multiplicar puntos", True, WHITE)

    juego.comodin_tiempo_extra_rect = texto_comodin_tiempo_extra.get_rect()
    juego.comodin_menos_votada_rect = texto_comodin_menos_votada.get_rect()
    juego.comodin_multiplicar_puntos_rect = texto_comodin_multiplicar_puntos.get_rect()

    juego.comodin_tiempo_extra_rect.topleft = (610, 450)
    juego.comodin_menos_votada_rect.topleft = (610, 500)
    juego.comodin_multiplicar_puntos_rect.topleft = (610, 550)

    pygame.draw.rect(juego.pantalla, BLUE, juego.comodin_tiempo_extra_rect)
    pygame.draw.rect(juego.pantalla, BLUE, juego.comodin_menos_votada_rect)
    pygame.draw.rect(juego.pantalla, BLUE,
                     juego.comodin_multiplicar_puntos_rect)

    if not juego.used_hints["tiempo_extra"]:
        juego.pantalla.blit(texto_comodin_tiempo_extra,
                            juego.comodin_tiempo_extra_rect)
    if not juego.used_hints["menos_votada"]:
        juego.pantalla.blit(texto_comodin_menos_votada,
                            juego.comodin_menos_votada_rect)
    if not juego.used_hints["multiplicar_puntos"]:
        juego.pantalla.blit(texto_comodin_multiplicar_puntos,
                            juego.comodin_multiplicar_puntos_rect)


# ---------------------------------------------------------
"""
Muestra el puntaje actual del jugador en la pantalla del juego.

Args:
    None

Returns:
    None
"""


def mostrar_puntaje(juego):
    texto_puntaje = juego.font.render(
        f"Puntos: {juego.puntaje}", True, WHITE)
    texto_puntaje_rect = texto_puntaje.get_rect()
    texto_puntaje_rect.topright = (SCREEN_WIDTH - 400, 500)
    circle_center = (texto_puntaje_rect.x + texto_puntaje_rect.width //
                     2, texto_puntaje_rect.y + texto_puntaje_rect.height // 2)
    pygame.draw.circle(juego.pantalla, BLACK, circle_center, RADIUS_Puntaje)
    pygame.draw.circle(juego.pantalla, YELLOW,
                       circle_center, RADIUS_Puntaje, WIDTH)
    juego.pantalla.blit(texto_puntaje, texto_puntaje_rect)


# ---------------------------------------------------------
"""
Muestra el número de oportunidades restantes en la pantalla del juego.

Args:
    None

Returns:
    None
"""


def mostrar_oportunidades(juego):
    texto_oportunidades = juego.font.render(
        f"Oportunidades: {juego.oportunidades}", True, BLACK, GREEN)
    texto_oportunidades_rect = texto_oportunidades.get_rect()
    texto_oportunidades_rect.topleft = (SCREEN_WIDTH - 370, 500)
    juego.pantalla.blit(texto_oportunidades, texto_oportunidades_rect)


# ---------------------------------------------------------
"""
Este método limpia la pantalla, muestra un mensaje de agradecimiento en el centro,
    actualiza la pantalla para mostrar el mensaje, espera 3 segundos y luego cierra el juego.
"""


def mostrar_pantalla_agradecimiento(juego):
    texto_agradecimiento = juego.font.render(
        "Gracias por jugar. ¡Hasta la próxima!", True, WHITE)
    texto_agradecimiento_rect = texto_agradecimiento.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    juego.pantalla.blit(texto_agradecimiento, texto_agradecimiento_rect)
    pygame.display.update()
    pygame.time.wait(3000)

# ---------------------------------------------------------
