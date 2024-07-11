import random
import pygame
import csv
import sys
from .config import *
from .utils import *
from .ordenamiento import *
from .recursos import *
from .mostrar import *
from .inicializadores import *

# ---------------------------------------------------------


class Juego100ARG:

    def __init__(self):
        # Inicializa pygame y los componentes del juego
        inicializar_pygame()
        self.audio_correcto, self.audio_incorrecto, self.audio_comodin = cargar_sonidos()
        self.pantalla = inicializar_pantalla()
        self.font = cargar_fuente()
        self.clock = pygame.time.Clock()
        (self.fondo_menu, self.fondo_preguntas,
         self.fondo_game_over, self.cruz_roja_gif) = cargar_imagenes()
        variables = inicializar_variables()
        self.input_respuesta = variables['input_respuesta']
        self.puntaje = variables['puntaje']
        self.contador_rondas = variables['contador_rondas']
        self.rondas_jugadas = variables['rondas_jugadas']
        self.max_rondas = variables['max_rondas']
        self.comodin_usado = variables['comodin_usado']
        self.oportunidades = variables['oportunidades']
        self.preguntas = variables['preguntas']
        self.respuestas_ingresadas = variables['respuestas_ingresadas']
        self.puntajes_acumulados = variables['puntajes_acumulados']
        self.partidas_jugadas = variables['partidas_jugadas']
        self.used_hints = {
            "tiempo_extra": False,
            "menos_votada": False,
            "multiplicar_puntos": False
        }
        self.resetear_juego()

# ---------------------------------------------------------

# Reinicia las variables del juego para comenzar una nueva partida
    def resetear_juego(self):
        self.oportunidades = 3
        self.tiempo_restante = RESPONSE_TIME
        self.bonus_multiplicar = 1
        self.contador_rondas = 0
        self.seleccionar_pregunta_aleatoriamente()
        self.respuestas_ingresadas = []

# ---------------------------------------------------------

    """
    Reinicia el estado del juego a sus valores iniciales.

    Este método es útil para comenzar una nueva partida o reiniciar el juego
    después de que haya terminado.

    Atributos modificados:
    - oportunidades (int): Reestablece las oportunidades a 3.
    - tiempo_restante (int): Reinicia el tiempo restante al valor predeterminado 
    - definido por la constante RESPONSE_TIME.
    - bonus_multiplicar (int): Establece el multiplicador de bonificación a 1.
    - contador_rondas (int): Reinicia el contador de rondas a 0.
    - respuestas_ingresadas (list): Limpia la lista de respuestas ingresadas.

    Acciones realizadas:
    - Llama al método seleccionar_pregunta_aleatoriamente() para elegir una nueva pregunta al azar.
    """

    def seleccionar_pregunta_aleatoriamente(self):
        self.pregunta_actual = random.choice(self.preguntas)
        self.tiempo_restante = RESPONSE_TIME
        self.respuestas_ingresadas = []

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
        # Asegurarse de que se esté trabajando con el total
        total_puntajes_acumulados = sum(self.puntajes_acumulados)

        if total_puntajes_acumulados == 500:
            self.premio = 1000000
            mensaje = f"Usted ganó el gran premio de ${self.premio}"
        elif total_puntajes_acumulados == 0:
            mensaje = f" Usted ha perdido, no ganó nada! ${pozo_acumulado}\n"
        else:
            pozo_acumulado = total_puntajes_acumulados * 500
            self.puntajes_acumulados.append(pozo_acumulado)
            mensaje = f" Usted ganó  ${pozo_acumulado}"

        # Dividir el mensaje en líneas
        lineas = mensaje.split("\n")

        # Posición inicial del texto
        x, y = 350, 320

        for linea in lineas:
            texto_premio = self.font.render(linea, True, WHITE)
            texto_premio_rect = texto_premio.get_rect(topleft=(x, y))
            self.pantalla.blit(texto_premio, texto_premio_rect)
            # Ajustar la posición Y para la siguiente línea
            y += texto_premio.get_height() + 5

        pygame.display.flip()  # Actualizar la pantalla

        # Pedir nombre del jugador y guardar puntaje
        nombre_jugador = pedir_nombre_jugador(self)
        guardar_puntaje(nombre_jugador, sum(self.puntajes_acumulados))

        # Mostrar el ranking
        self.cargar_y_mostrar_ranking()

        pygame.display.update()


# ---------------------------------------------------------

    """
    Carga el ranking desde un archivo CSV y lo muestra en pantalla.

    Este método lee los datos de puntaje desde un archivo CSV, los ordena de mayor a menor
    y muestra los 10 mejores puntajes en la pantalla del juego.

    Atributos modificados:
    - ruta_ranking (str): Ruta del archivo CSV que contiene el ranking.
    - ranking (list): Lista que almacena los datos del ranking leídos del archivo.
    - ranking_ordenado (list): Lista que almacena los datos del ranking ordenados por puntaje.

    Acciones realizadas:
    - Lee el archivo de ranking y almacena los datos en una lista.
    - Ordena la lista de ranking por puntaje en orden descendente.
    - Muestra el fondo de pantalla de "game over".
    - Muestra los 10 mejores puntajes en la pantalla, con un desplazamiento vertical entre cada uno.

    Excepciones manejadas:
    - FileNotFoundError: Si el archivo de ranking no existe, se inicializa una lista vacía.
    """

    def cargar_y_mostrar_ranking(self):
        ruta_ranking = "data/ranking.csv"
        ranking = []

        # Leer el archivo de ranking
        try:
            with open(ruta_ranking, mode='r') as file:
                reader = csv.reader(file)
                ranking = list(reader)
        except FileNotFoundError:
            ranking = []

        # Ordenar el ranking por puntaje (de mayor a menor)
        ranking_ordenado = sorted(
            ranking, key=lambda x: int(x[1]), reverse=True)

        # Mostrar el ranking en pantalla
        self.pantalla.blit(self.fondo_game_over, (0, 0))
        y_offset = 50
        # Mostrar solo los 10 mejores
        for nombre, puntaje in ranking_ordenado[:10]:
            texto_ranking = self.font.render(
                f"{nombre}: {puntaje}", True, WHITE)
            self.pantalla.blit(texto_ranking, (50, y_offset))
            y_offset += 30

        pygame.display.update()

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
            f"Ronda: {self.rondas_jugadas}", True, WHITE)
        texto_contador_rect = texto_contador.get_rect()
        texto_contador_rect.topleft = (SCREEN_WIDTH - 800, 50)
        self.pantalla.blit(texto_contador, texto_contador_rect)

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

            # Verificar si la respuesta ya está en respuestas_ingresadas
            if input_respuesta not in [respuesta for respuesta, _ in self.respuestas_ingresadas]:
                puntos_obtenidos = respuestas[input_respuesta] * \
                    self.bonus_multiplicar
                self.puntaje += puntos_obtenidos  # Sumar puntos al puntaje total
                self.puntajes_acumulados.append(puntos_obtenidos)
                self.respuestas_ingresadas.append(
                    (input_respuesta, puntos_obtenidos))
                # Mostrar respuestas ingresadas ordenadas por puntos
                mostrar_respuestas_ingresadas(self)

        else:
            self.audio_incorrecto.play()
            mostrar_animacion_cruz(self)
            self.oportunidades -= 1
            self.input_respuesta = ""
            # Si se acaban las oportunidades, mostrar "Game Over" y reiniciar el juego
            if self.oportunidades == 0:
                pygame.time.wait(1000)
                self.rondas_jugadas += 1
                if self.rondas_jugadas >= self.max_rondas:
                    mostrar_pantalla_final(self)
                    return  # Salir de la función si el juego ha terminado
                self.resetear_juego()
                return  # Salir de la función si el juego se reinicia

        self.limpiar_input_respuesta()  # Limpiar el input después de procesar la respuesta

        # Seleccionar una nueva pregunta solo si todas las respuestas han sido ingresadas
        if len(self.respuestas_ingresadas) == len(respuestas):
            self.seleccionar_pregunta_aleatoriamente()
            # Resetear respuestas ingresadas para la nueva pregunta
            self.respuestas_ingresadas = []

# ---------------------------------------------------------

    """
    Limpia el campo de entrada de respuesta del usuario.

    Este método establece la variable `input_respuesta` a una cadena vacía, 
    reiniciando así cualquier respuesta previamente ingresada.

    Atributos modificados:
    - input_respuesta (str): Campo de entrada de respuesta del usuario.
    """

    def limpiar_input_respuesta(self):
        self.input_respuesta = ""

# ---------------------------------------------------------

    """
    Limpia la lista de respuestas ingresadas por el usuario.

    Este método establece la variable `respuestas_ingresadas` a una lista vacía,
    eliminando todas las respuestas que se han ingresado previamente.

    Atributos modificados:
    - respuestas_ingresadas (list): Lista de respuestas ingresadas por el usuario.
    """

    def limpiar_respuestas_ingresadas(self):
        self.respuestas_ingresadas = []

# ---------------------------------------------------------

    """
    Usa el comodín seleccionado durante el juego, permite al jugador usar diferentes comodines según el tipo especificado
    Args:
        tipo (str): El tipo de comodín a usar.

    Returns:
        None
    """

    def usar_comodin(self, tipo):
        if not self.used_hints[tipo]:  # Verificar si el comodín no se ha usado
            if tipo == "tiempo_extra":
                self.tiempo_restante += 10
            elif tipo == "menos_votada":
                respuestas = self.pregunta_actual["respuestas"]
                menos_votada = min(respuestas, key=respuestas.get)
                self.respuestas_ingresadas.append(
                    (menos_votada, respuestas[menos_votada]))
            elif tipo == "multiplicar_puntos":
                self.bonus_multiplicar = 2

            # Marcar el comodín como usado
            self.used_hints[tipo] = True
            self.audio_comodin.play()

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
    Este método evalúa diferentes condiciones para decidir si el juego debe terminar
    o si se ha ganado un premio. También maneja la visualización de una imagen y
    el reinicio del juego en caso de que se hayan agotado las oportunidades del jugador.

    Retorna:
    - bool: True si el juego ha terminado o se ha ganado un premio, False en caso contrario.

    Condiciones verificadas:
    - Si el puntaje es mayor o igual a 500, se llama al método premio_ganado() y se retorna True.
    - Si el número de rondas jugadas es mayor o igual al máximo de rondas permitidas, se llama
    - al método premio_ganado() y se retorna True.
    - Si las oportunidades se han agotado:
        - Muestra una imagen de cruz roja en la pantalla.
        - Actualiza la pantalla y espera 2 segundos.
        - Reinicia el juego llamando al método resetear_juego().
        - Incrementa el contador de rondas jugadas.
        - Si el número de rondas jugadas es mayor o igual al máximo de rondas permitidas,
        - se llama al método premio_ganado() y se retorna True.

    Atributos modificados:
    - rondas_jugadas (int): Incrementa el contador de rondas jugadas si las oportunidades se han agotado.
    """

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
                mostrar_pregunta(juego)

        if self.oportunidades == 0:
            pygame.time.wait(1000)
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
            mostrar_pregunta(self)
            mostrar_reloj(self)
            mostrar_input(self)
            mostrar_puntaje(self)
            mostrar_oportunidades(self)
            mostrar_comodines(self)
            mostrar_puntaje(self)
            mostrar_rondas_jugadas(self)
            mostrar_respuestas_ingresadas(self)
            for event in pygame.event.get():
                self.manejar_eventos(event)

            if self.oportunidades == 0:
                self.limpiar_input_respuesta()
                self.partidas_jugadas += 1
                self.chequear_fin_juego()

            if self.puntaje >= 500:
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
