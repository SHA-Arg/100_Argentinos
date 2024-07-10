import pygame
import sys
import csv
from .config import *
from .ordenamiento import ordenar_respuestas


def mostrar_input(juego):
    input_respuesta_rect = pygame.Rect(70, 110, 500, 50)
    pygame.draw.rect(juego.pantalla, WHITE, input_respuesta_rect, 2)
    texto_input = juego.font.render(juego.input_respuesta, True, WHITE)
    juego.pantalla.blit(
        texto_input, (input_respuesta_rect.x + 5, input_respuesta_rect.y + 5))

    pygame.display.update(input_respuesta_rect)


# def mostrar_ranking(juego):
#     with open('ranking.csv', 'r') as file:
#         reader = csv.reader(file)


# ranking = ordenar_respuestas(reader)


# y_offset = 100
# for i, row in enumerate(ranking):
#     texto_ranking = juego.font.render(
#         f"{i+1}. {row[0]} puntos", True, WHITE)
#     texto_ranking_rect = texto_ranking.get_rect()
#     texto_ranking_rect.topleft = (50, y_offset)
#     juego.pantalla.blit(texto_ranking, texto_ranking_rect)
#     y_offset += 40

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

        y_offset += 50

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
    juego.pantalla.blit(juego.fondo_game_over, (0, 0))
    texto_pantalla_final = juego.font.render(
        "¡Juego terminado! ¿Deseas jugar otra vez? (S/N)", True, WHITE)
    texto_pantalla_final_rect = texto_pantalla_final.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    juego.pantalla.blit(texto_pantalla_final, texto_pantalla_final_rect)
    pygame.display.update()

    esperando_respuesta = True
    while esperando_respuesta:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    juego.rondas_jugadas = 0
                    juego.resetear_juego()
                    esperando_respuesta = False
                elif event.key == pygame.K_n:
                    pygame.quit()
                    return

    juego.pantalla.blit(juego.fondo_game_over, (0, 0))
    texto_pantalla_final = juego.font.render(
        "¡Juego terminado! ¿Deseas jugar otra vez? (S/N)", True, WHITE)
    texto_pantalla_final_rect = texto_pantalla_final.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    juego.pantalla.blit(texto_pantalla_final, texto_pantalla_final_rect)
    pygame.display.update()

    esperando_respuesta = True
    while esperando_respuesta:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    juego.rondas_jugadas = 0
                    juego.resetear_juego()
                    esperando_respuesta = False
                elif event.key == pygame.K_n:
                    pygame.quit()
                    return

# ---------------------------------------------------------
    """
    Muestra una animación de cruz roja en la pantalla del juego. Este método posiciona y muestra una animación de cruz roja

    Args:
        None

    Returns:
        None
    """


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
Muestra la pantalla de juego terminado con el texto correspondiente y el premio ganado.

Args:
        None

Returns:
    None

"""


def mostrar_game_over(juego):
    # Texto de Game Over
    game_over_text = juego.font.render(
        "¡EL JUEGO A FINALIZADO!", True, WHITE)
    game_over_rect = game_over_text.get_rect()
    game_over_rect.topleft = (270, 50)
    padding = 10
    fondo_game_over = pygame.Rect(game_over_rect.x - padding, game_over_rect.y - padding,
                                  game_over_rect.width + 2 * padding, game_over_rect.height + 2 * padding)
    juego.pantalla.blit(game_over_text, game_over_rect)

    juego.premio_ganado()
    juego.pantalla.blit(juego.fondo_game_over, (0, 0))

    # Mostrar ranking
    # mostrar_ranking(juego)

    pygame.display.update()
    pygame.time.wait(2000)

# ---------------------------------------------------------
