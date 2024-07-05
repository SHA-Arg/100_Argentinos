import random
import pygame
import csv
import sys
from Packages.config import *
from Packages.utils import *
from Packages.ordenamiento import *
from Packages.recursos import pantalla, font, fondo_menu, escribir_texto, font_instrucciones, fondo_instrucciones

# ---------------------------------------------------------


class Juego100ARG:
    def __init__(self):
        # Inicializa pygame y los componentes del juego
        pygame.init()
        self.audio_correcto = pygame.mixer.Sound("assets/sounds/correcto.mp3")
        self.audio_incorrecto = pygame.mixer.Sound("assets/sounds/error.mp3")
        self.pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("100 Argentinos dicen")
        self.font = pygame.font.Font(FONT_PATH1, FONT_SIZE)
        self.clock = pygame.time.Clock()
        self.fondo_menu = cargar_imagen(
            "assets/imgs/fondo_menu2.jpg", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.fondo_preguntas = cargar_imagen(
            "assets/imgs/Fondo_Juego_100Arg.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.fondo_game_over = cargar_imagen(
            "assets/imgs/Fondo_de_Pantalla_con_Frase_e_Imagen_.jpg", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.cruz_roja_gif = cargar_imagen(
            "assets/imgs/cruz_roja.gif", 100, 100)
        # Variables globales
        self.input_respuesta = ""
        self.puntaje = 0
        self.contador_rondas = 0
        self.rondas_jugadas = 0
        self.max_rondas = 5
        self.comodin_usado = False
        self.oportunidades = 3
        self.preguntas = cargar_archivo_json("json\preguntas.json")
        self.respuestas_ingresadas = []
        self.puntajes_acumulados = []
        self.partidas_jugadas = 0
        self.resetear_juego()

# ---------------------------------------------------------
# Reinicia las variables del juego para comenzar una nueva partida
    def resetear_juego(self):
        self.puntaje = 0
        self.oportunidades = 3
        self.tiempo_restante = RESPONSE_TIME
        self.bonus_multiplicar = 1
        self.used_hints = {
            "tiempo_extra": False,
            "menos_votada": False,
            "multiplicar_puntos": False
        }
        self.contador_rondas = 0
        self.seleccionar_pregunta_aleatoriamente()
        self.respuestas_ingresadas = []

# ---------------------------------------------------------
# Selecciona una pregunta aleatoria del archivo de preguntas
    def seleccionar_pregunta_aleatoriamente(self):
        self.pregunta_actual = random.choice(self.preguntas)
        self.tiempo_restante = RESPONSE_TIME

# ---------------------------------------------------------
    """
    Calcula y muestra el premio ganado al finalizar el juego. Este método determina el premio basado en el puntaje final del jugador.

    Args:
    None

    Returns:
    None
    """

    def premio_ganado(self):
        pozo_acumulado = 0
        if self.puntaje >= 500:
            self.premio = 1000000
            mensaje = f"Usted ganó el gran premio\n de\n ${self.premio}"
        elif self.puntaje > 0 and self.puntaje < 500:
            pozo_acumulado = self.puntaje * 500
            self.puntajes_acumulados.append(pozo_acumulado)
            mensaje = f" Usted ganó \n ${pozo_acumulado}"
        elif self.puntaje == 0:
            mensaje = f" Usted ha perdido,\n no ganó nada! ${pozo_acumulado}\n"

        volver_a_jugar = f"\n¿Desea volver a jugar? (S/N)"
        mensaje += "\n" + volver_a_jugar

        self.pantalla.blit(self.fondo_game_over, (0, 0))

        # Dividir el mensaje en líneas
        lineas = mensaje.split('\n')

        # Posición inicial del texto
        x, y = 300, 350

        # Renderizar y dibujar cada línea de texto
        for linea in lineas:
            texto_premio = self.font.render(linea, True, WHITE)
            texto_premio_rect = texto_premio.get_rect(topleft=(x, y))
            self.pantalla.blit(texto_premio, texto_premio_rect)
            # Ajustar la posición Y para la siguiente línea
            y += texto_premio.get_height() + 5
        pygame.display.flip()  # Actualizar la pantalla

        # Guardar el puntaje en el archivo CSV
        with open('data/ranking.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.puntaje])

        pygame.display.update()
        # Mostrar el mensaje en pantalla
        self.pantalla.blit(self.fondo_game_over, (0, 0))
        texto_premio = self.font.render(mensaje, True, WHITE)
        texto_premio_rect = texto_premio.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.pantalla.blit(texto_premio, texto_premio_rect)
        pygame.display.update()
    '''
def premio_ganado(self):
        pozo_acumulado = 0
        if self.puntaje == 500:
            self.premio = 1000000
            mensaje = f"Usted gano el gran premio\n de\n ${self.premio}"
        elif self.puntaje > 0 and self.puntaje < 500:
            pozo_acumulado = self.puntaje * 500
            self.puntajes_acumulados.append(pozo_acumulado)
            mensaje = f" Usted gano \n ${pozo_acumulado}"
        elif self.puntaje == 0:
            mensaje = f" Usted a perdido,\n no gano nada! ${
                pozo_acumulado}\n"

        volver_a_jugar = f"\n¿Desea volver a jugar? (S/N)"
        mensaje += "\n" + volver_a_jugar

        self.pantalla.blit(self.fondo_game_over, (0, 0))

        # Dividir el mensaje en líneas
        lineas = mensaje.split('\n')

        # Posición inicial del texto
        x, y = 300, 350

        # Renderizar y dibujar cada línea de texto
        for linea in lineas:
            texto_premio = self.font.render(linea, True, WHITE)
            texto_premio_rect = texto_premio.get_rect(topleft=(x, y))
            self.pantalla.blit(texto_premio, texto_premio_rect)
            # Ajustar la posición Y para la siguiente línea
            y += texto_premio.get_height() + 5
        pygame.display.flip()  # Actualizar la pantalla

        # Guardar el puntaje en el archivo CSV
        with open('data\ranking.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.puntaje])

        # Mostrar el mensaje en pantalla

        pygame.display.update()
    '''

# ---------------------------------------------------------
    def mostrar_ranking(self):
        with open('ranking.csv', 'r') as file:
            reader = csv.reader(file)
            ranking = ranking = ordenar_respuestas(reader)

        y_offset = 100
        for i, row in enumerate(ranking):
            texto_ranking = self.font.render(
                f"{i+1}. {row[0]} puntos", True, WHITE)
            texto_ranking_rect = texto_ranking.get_rect()
            texto_ranking_rect.topleft = (50, y_offset)
            self.pantalla.blit(texto_ranking, texto_ranking_rect)
            y_offset += 40

# ---------------------------------------------------------
    """
    Muestra el contador de rondas en la pantalla del juego. Este metodo renderiza el número de la ronda actual en la esquina superior izquierda de la pantalla
    Args:
        None

    Returns:
        None
    """

    def contador_rondas(self):
        texto_contador = self.font.render(
            f"Ronda: {self.contador_rondas}", True, WHITE)
        texto_contador_rect = texto_contador.get_rect()
        texto_contador_rect.topleft = (SCREEN_WIDTH - 800, 50)
        self.pantalla.blit(texto_contador, texto_contador_rect)

# ---------------------------------------------------------
    """
    Muestra la pregunta actual en la pantalla del juego. Este método verifica si hay una pregunta seleccionada. Si no hay ninguna pregunta, lanza un ValueError

    Args:
        None

    Returns:
        None
    """

    def mostrar_pregunta(self):
        texto_pregunta = self.font.render(
            self.pregunta_actual["pregunta"] + "?", True, WHITE)
        pregunta_rect = texto_pregunta.get_rect()
        pregunta_rect.topleft = (20, 60)
        padding = 10
        fondo_pregunta = pygame.Rect(pregunta_rect.x - padding, pregunta_rect.y - padding,
                                     pregunta_rect.width + 2 * padding, pregunta_rect.height + 2 * padding)
        pygame.draw.rect(self.pantalla, BLUE, fondo_pregunta)
        self.pantalla.blit(texto_pregunta, pregunta_rect)

        print(self.pregunta_actual["respuestas"])

# ---------------------------------------------------------
    """
    Muestra el reloj de tiempo restante en la pantalla del juego. Este método renderiza el tiempo restante en segundos en la esquina superior izquierda de la pantalla.

    Args:
        None

    Returns:
        None
    """

    def mostrar_reloj(self):
        texto_reloj = self.font.render(
            f"{int(self.tiempo_restante)}s", True, WHITE)
        texto_reloj_rect = texto_reloj.get_rect()
        texto_reloj_rect.topleft = (SCREEN_WIDTH - 780, 120)
        circle_center = (texto_reloj_rect.x + texto_reloj_rect.width //
                         2, texto_reloj_rect.y + texto_reloj_rect.height // 2)

        pygame.draw.circle(self.pantalla, BLACK, circle_center, RADIUS_Time)
        pygame.draw.circle(self.pantalla, YELLOW,
                           circle_center, RADIUS_Time, WIDTH)
        self.pantalla.blit(texto_reloj, texto_reloj_rect)

        if self.tiempo_restante <= 5:
            pygame.draw.circle(self.pantalla, RED,
                               circle_center, RADIUS_Time, WIDTH)

# ---------------------------------------------------------
    """
    Muestra las respuestas ingresadas ordenadas en la pantalla del juego. Este método ordena las respuestas ingresadas por puntaje usando la función `ordenar_respuestas`

    Args:
        None

    Returns:
        None
    """

    def mostrar_respuestas_ingresadas(self):
        respuestas_ordenadas = ordenar_respuestas(self.respuestas_ingresadas)

        y_offset = 200
        for respuesta, puntos in respuestas_ordenadas:
            texto_respuesta = self.font.render(
                f"{respuesta}: {puntos}", True, WHITE)
            texto_respuesta_rect = texto_respuesta.get_rect()
            texto_respuesta_rect.topleft = (100, y_offset)

            pygame.draw.rect(self.pantalla, BLUE, texto_respuesta_rect)
            self.pantalla.blit(texto_respuesta, texto_respuesta_rect)

            y_offset += 50

# ---------------------------------------------------------
    """
    Muestra el campo de entrada de respuesta en la pantalla del juego. Este método renderiza un rectángulo blanco como campo de entrada

    Args:
        None

    Returns:
        None
    """

    def mostrar_input(self):
        input_respuesta_rect = pygame.Rect(70, 110, 500, 50)
        pygame.draw.rect(self.pantalla, WHITE, input_respuesta_rect, 2)
        texto_input = self.font.render(self.input_respuesta, True, WHITE)
        self.pantalla.blit(
            texto_input, (input_respuesta_rect.x + 5, input_respuesta_rect.y + 5))

        pygame.display.update(input_respuesta_rect)

# ---------------------------------------------------------
# Verifica la respuesta ingresada
    def verificar_respuesta(self):
        respuesta_ingresada = self.input_respuesta.strip().lower()
        for respuesta in self.pregunta_actual["respuestas"]:
            if respuesta_ingresada == respuesta["respuesta"].strip().lower():
                if respuesta_ingresada not in self.respuestas_ingresadas:
                    self.audio_correcto.play()
                    self.puntaje += respuesta["puntos"]
                    self.respuestas_ingresadas.append(
                        (respuesta_ingresada, respuesta["puntos"]))
                else:
                    print("Respuesta ya ingresada.")
                self.input_respuesta = ""
                return True
        self.audio_incorrecto.play()
        self.oportunidades -= 1
        self.input_respuesta = ""
        return False

# ---------------------------------------------------------
# Limpia el campo de entrada de texto
    def limpiar_input_respuesta(self):
        self.input_respuesta = ""

# ---------------------------------------------------------
    """
    Muestra la pantalla final del juego y gestiona la respuesta del jugador.Este método muestra el fondo de pantalla de juego terminado y un mensaje para preguntar al jugador si desea jugar otra vez.

    Args:
        None

    Returns:
        None
    """

    def mostrar_pantalla_final(self):
        self.pantalla.blit(self.fondo_game_over, (0, 0))
        texto_pantalla_final = self.font.render(
            "¡Juego terminado! ¿Deseas jugar otra vez? (S/N)", True, WHITE)
        texto_pantalla_final_rect = texto_pantalla_final.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.pantalla.blit(texto_pantalla_final, texto_pantalla_final_rect)
        pygame.display.update()

        esperando_respuesta = True
        while esperando_respuesta:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.rondas_jugadas = 0
                        self.resetear_juego()
                        esperando_respuesta = False
                    elif event.key == pygame.K_n:
                        pygame.quit()
                        return

        self.pantalla.blit(self.fondo_game_over, (0, 0))
        texto_pantalla_final = self.font.render(
            "¡Juego terminado! ¿Deseas jugar otra vez? (S/N)", True, WHITE)
        texto_pantalla_final_rect = texto_pantalla_final.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.pantalla.blit(texto_pantalla_final, texto_pantalla_final_rect)
        pygame.display.update()

        esperando_respuesta = True
        while esperando_respuesta:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.rondas_jugadas = 0
                        self.resetear_juego()
                        esperando_respuesta = False
                    elif event.key == pygame.K_n:
                        pygame.quit()
                        return

# ---------------------------------------------------------
    """
    Chequea la respuesta ingresada por el jugador y gestiona las acciones correspondientes. Este método verifica si la respuesta ingresada por el jugador está en las respuestas válidas para la pregunta actual

    Args:
        input_respuesta (str): La respuesta ingresada por el jugador.

    Returns:
        None
    """

    def chequear_respuesta(self, input_respuesta):
        respuestas = self.pregunta_actual["respuestas"]
        if input_respuesta in respuestas:
            self.audio_correcto.play()
            puntos_obtenidos = respuestas[input_respuesta] * \
                self.bonus_multiplicar

            if input_respuesta not in [respuesta for respuesta, _ in self.respuestas_ingresadas]:
                puntos_obtenidos = respuestas[input_respuesta] * \
                    self.bonus_multiplicar
                self.respuestas_ingresadas.append(
                    (input_respuesta, puntos_obtenidos))
                self.puntaje += puntos_obtenidos  # Sumar puntos al puntaje total
                self.mostrar_respuestas_ingresadas()
        else:
            self.mostrar_animacion_cruz()
            self.audio_incorrecto.play()
            self.oportunidades -= 1
            self.input_respuesta = ""
            if self.oportunidades == 0:
                pygame.time.wait(1000)
                self.rondas_jugadas += 1
                if self.rondas_jugadas >= self.max_rondas:
                    self.mostrar_pantalla_final()
                    return
                self.resetear_juego()
                return

        self.limpiar_input_respuesta()

        if len(self.respuestas_ingresadas) == len(respuestas):
            self.seleccionar_pregunta_aleatoriamente()
            self.respuestas_ingresadas = []

        if self.puntaje >= 500:
            self.mostrar_game_over()
            self.premio_ganado()
    '''
    def chequear_respuesta(self, input_respuesta):
        respuestas = self.pregunta_actual["respuestas"]
        if input_respuesta in respuestas:
            self.audio_correcto.play()
            puntos_obtenidos = respuestas[input_respuesta] * \
                self.bonus_multiplicar

            # Verificar si la respuesta ya está en respuestas_ingresadas
            if input_respuesta not in [respuesta for respuesta, _ in self.respuestas_ingresadas]:
                puntos_obtenidos = respuestas[input_respuesta] * \
                    self.bonus_multiplicar
                self.respuestas_ingresadas.append(
                    (input_respuesta, puntos_obtenidos))
                self.puntaje += puntos_obtenidos  # Sumar puntos al puntaje total
                # Mostrar respuestas ingresadas ordenadas por puntos
                self.mostrar_respuestas_ingresadas()
        else:
            self.mostrar_animacion_cruz()
            self.audio_incorrecto.play()
            self.oportunidades -= 1
            self.input_respuesta = ""
            if self.oportunidades == 0:
                # Si se acaban las oportunidades, mostrar "Game Over" y reiniciar el juego
                if self.oportunidades == 0:
                    pygame.time.wait(1000)
                    self.rondas_jugadas += 1
                    if self.rondas_jugadas >= self.max_rondas:
                        self.mostrar_pantalla_final()
                        return  # Salir de la función si el juego ha terminado
                    self.resetear_juego()
                    return  # Salir de la función si el juego se reinicia

        self.limpiar_input_respuesta()  # Limpiar el input después de procesar la respuesta

        # Seleccionar una nueva pregunta solo si todas las respuestas han sido ingresadas
        if len(self.respuestas_ingresadas) == len(respuestas):
            self.seleccionar_pregunta_aleatoriamente()
            # Resetear respuestas ingresadas para la nueva pregunta
            self.respuestas_ingresadas = []
    '''

# ---------------------------------------------------------
    """
    Muestra una animación de cruz roja en la pantalla del juego. Este método posiciona y muestra una animación de cruz roja

    Args:
        None

    Returns:
        None
    """

    def mostrar_animacion_cruz(self):
        cruz_rect = self.cruz_roja_gif.get_rect()
        cruz_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.pantalla.blit(self.cruz_roja_gif, cruz_rect)
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

    def mostrar_comodines(self):
        texto_comodin_tiempo_extra = self.font.render(
            "Tiempo extra", True, WHITE)
        texto_comodin_menos_votada = self.font.render(
            "Menos votada", True, WHITE)
        texto_comodin_multiplicar_puntos = self.font.render(
            "Multiplicar puntos", True, WHITE)

        self.comodin_tiempo_extra_rect = texto_comodin_tiempo_extra.get_rect()
        self.comodin_menos_votada_rect = texto_comodin_menos_votada.get_rect()
        self.comodin_multiplicar_puntos_rect = texto_comodin_multiplicar_puntos.get_rect()

        self.comodin_tiempo_extra_rect.topleft = (610, 450)
        self.comodin_menos_votada_rect.topleft = (610, 500)
        self.comodin_multiplicar_puntos_rect.topleft = (610, 550)

        pygame.draw.rect(self.pantalla, BLUE, self.comodin_tiempo_extra_rect)
        pygame.draw.rect(self.pantalla, BLUE, self.comodin_menos_votada_rect)
        pygame.draw.rect(self.pantalla, BLUE,
                         self.comodin_multiplicar_puntos_rect)

        if not self.used_hints["tiempo_extra"]:
            self.pantalla.blit(texto_comodin_tiempo_extra,
                               self.comodin_tiempo_extra_rect)
        if not self.used_hints["menos_votada"]:
            self.pantalla.blit(texto_comodin_menos_votada,
                               self.comodin_menos_votada_rect)
        if not self.used_hints["multiplicar_puntos"]:
            self.pantalla.blit(texto_comodin_multiplicar_puntos,
                               self.comodin_multiplicar_puntos_rect)

# ---------------------------------------------------------
    """
    Usa el comodín seleccionado durante el juego, permite al jugador usar diferentes comodines según el tipo especificado
    Args:
        tipo (str): El tipo de comodín a usar.

    Returns:
        None
    """

    def usar_comodin(self, tipo):
        if tipo == "tiempo_extra" and not self.used_hints[tipo]:
            self.tiempo_restante += 10
            self.used_hints[tipo] = True
        elif tipo == "menos_votada" and not self.used_hints[tipo]:
            respuestas = self.pregunta_actual["respuestas"]
            menos_votada = min(respuestas, key=respuestas.get)
            self.respuestas_ingresadas.append(
                (menos_votada, respuestas[menos_votada]))
            self.used_hints[tipo] = True
        elif tipo == "multiplicar_puntos" and not self.used_hints[tipo]:
            self.bonus_multiplicar = 2
            self.used_hints[tipo] = True

# ---------------------------------------------------------
    """
    Chequea si el juego ha llegado a su fin y realiza las acciones finales correspondientes.
    Args:
        None

    Returns:
        None
    """

    def chequear_fin_juego(self):
        if self.contador_rondas == 0:
            self.mostrar_game_over()
            self.premio_ganado()
            self.puntaje_total = sum(self.puntajes_acumulados)
            pygame.time.wait(2000)
            self.resetear_juego()

# ---------------------------------------------------------
    """
    Maneja los eventos del juego como presionar teclas o clics de ratón.

    Args:
        event (pygame.event): El evento pygame que se está gestionando.

    Returns:
        None
    """

    def manejar_eventos(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.resetear_juego()
            elif event.key == pygame.K_BACKSPACE:
                self.input_respuesta = self.input_respuesta[:-1]
            elif event.key == pygame.K_RETURN:
                self.chequear_respuesta(self.input_respuesta)
            else:
                self.input_respuesta += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.comodin_tiempo_extra_rect.collidepoint(mouse_pos):
                self.usar_comodin("tiempo_extra")
            if self.comodin_menos_votada_rect.collidepoint(mouse_pos):
                self.usar_comodin("menos_votada")
            if self.comodin_multiplicar_puntos_rect.collidepoint(mouse_pos):
                self.usar_comodin("multiplicar_puntos")

# ---------------------------------------------------------
    """
    Muestra el puntaje actual del jugador en la pantalla del juego.

    Args:
        None

    Returns:
        None
    """

    def mostrar_puntaje(self):
        texto_puntaje = self.font.render(
            f"Puntos: {self.puntaje}", True, WHITE)
        texto_puntaje_rect = texto_puntaje.get_rect()
        texto_puntaje_rect.topright = (SCREEN_WIDTH - 400, 500)
        circle_center = (texto_puntaje_rect.x + texto_puntaje_rect.width //
                         2, texto_puntaje_rect.y + texto_puntaje_rect.height // 2)
        pygame.draw.circle(self.pantalla, BLACK, circle_center, RADIUS_Puntaje)
        pygame.draw.circle(self.pantalla, YELLOW,
                           circle_center, RADIUS_Puntaje, WIDTH)
        self.pantalla.blit(texto_puntaje, texto_puntaje_rect)

# ---------------------------------------------------------
# Verifica el estado del juego (ganar, perder, continuar)
    def verificar_estado_juego(self):
        if self.puntaje >= 500:
            self.premio_ganado()
            return True
        elif self.rondas_jugadas >= self.max_rondas:
            self.premio_ganado()
            return True
        elif self.oportunidades <= 0:
            self.pantalla.blit(
                self.cruz_roja_gif, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50))
            pygame.display.flip()
            pygame.time.wait(2000)
            self.resetear_juego()
            self.rondas_jugadas += 1
            if self.rondas_jugadas >= self.max_rondas:
                self.premio_ganado()
                return True
        return False

# ---------------------------------------------------------
    """
    Muestra el número de oportunidades restantes en la pantalla del juego.

    Args:
        None

    Returns:
        None
    """

    def mostrar_oportunidades(self):
        texto_oportunidades = self.font.render(
            f"Oportunidades: {self.oportunidades}", True, BLACK, GREEN)
        texto_oportunidades_rect = texto_oportunidades.get_rect()
        texto_oportunidades_rect.topleft = (SCREEN_WIDTH - 370, 500)
        self.pantalla.blit(texto_oportunidades, texto_oportunidades_rect)

# ---------------------------------------------------------
    """
    Muestra la pantalla de juego terminado con el texto correspondiente y el premio ganado.

    Args:
        None

    Returns:
        None

    """

    def mostrar_game_over(self):
        # Texto de Game Over
        game_over_text = self.font.render(
            "¡EL JUEGO A FINALIZADO!", True, WHITE)
        game_over_rect = game_over_text.get_rect()
        game_over_rect.topleft = (270, 50)
        padding = 10
        fondo_game_over = pygame.Rect(game_over_rect.x - padding, game_over_rect.y - padding,
                                      game_over_rect.width + 2 * padding, game_over_rect.height + 2 * padding)
        self.pantalla.blit(game_over_text, game_over_rect)

        self.premio_ganado()
        self.pantalla.blit(self.fondo_game_over, (0, 0))

        # Mostrar ranking
        self.mostrar_ranking()

        pygame.display.update()
        pygame.time.wait(2000)

# ---------------------------------------------------------
    """
    Actualiza el reloj del juego y gestiona las acciones correspondientes cuando se agota el tiempo.

    Args:
        None

    Returns:
        None
    """

    def actualizar_reloj(self):
        self.tiempo_restante -= 1 / FPS
        if self.tiempo_restante <= 0:
            self.oportunidades -= 1
            self.tiempo_restante = RESPONSE_TIME
            if self.oportunidades > 0:
                self.seleccionar_pregunta_aleatoriamente()
                self.mostrar_pregunta()

        if self.oportunidades == 0:
            self.mostrar_game_over()
            pygame.time.wait(2000)
            self.resetear_juego()

# ---------------------------------------------------------
    """
    Ejecuta el bucle principal del juego,donde se actualizan y muestran en pantalla todos los elementos del juego

        Args:
        None

    Returns:
        None
    """

    def ejecutar(self):
        while True:
            self.pantalla.blit(self.fondo_preguntas, (0, 0))
            self.mostrar_pregunta()
            self.mostrar_reloj()
            self.mostrar_input()
            self.mostrar_puntaje()
            self.mostrar_oportunidades()
            self.mostrar_comodines()
            self.mostrar_respuestas_ingresadas()
            for event in pygame.event.get():
                self.manejar_eventos(event)

            if self.oportunidades == 0:
                self.limpiar_input_respuesta()
                self.partidas_jugadas += 1
                self.chequear_fin_juego()

            if self.puntaje >= 500:
                self.mostrar_game_over()
                self.premio_ganado()
                break

            self.actualizar_reloj()
            pygame.display.update()
            self.clock.tick(FPS)

# ---------------------------------------------------------


if __name__ == "__main__":
    juego = Juego100ARG()
    juego.ejecutar()

# ---------------------------------------------------------
