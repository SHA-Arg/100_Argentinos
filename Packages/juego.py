import random
import pygame
import sys
from .config import *
from .utils import *
from .mostrar import *
from .ordenamiento import *
from .inicializadores import *
from .recursos import *

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
        self.resetear_juego()

# ---------------------------------------------------------

    def resetear_juego(self):
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
        self.oportunidades = 3
        self.tiempo_restante = RESPONSE_TIME
        self.bonus_multiplicar = 1
        self.puntaje = 0
        self.contador_rondas = 0
        self.seleccionar_pregunta_aleatoriamente()
        self.respuestas_ingresadas = []
        self.used_hints = {
            "tiempo_extra": False,
            "menos_votada": False,
            "multiplicar_puntos": False
        }


# ---------------------------------------------------------

    def seleccionar_pregunta_aleatoriamente(self):
        """
    Este método selecciona una pregunta de manera aleatoria de la lista de preguntas 
    cargadas, resetea el tiempo restante para responder y limpia las respuestas ingresadas anteriormente.
    """
        self.pregunta_actual = random.choice(self.preguntas)
        self.tiempo_restante = RESPONSE_TIME
        self.respuestas_ingresadas = []

# ---------------------------------------------------------
    def contador_rondas(self):
        """
    Muestra el contador de rondas en la pantalla del juego. Este metodo renderiza el número de la ronda actual en la esquina superior izquierda de la pantalla
    Args:
        None

    Returns:
        None
    """
        texto_contador = self.font.render(
            f"Ronda: {self.rondas_jugadas}", True, WHITE)
        texto_contador_rect = texto_contador.get_rect()
        texto_contador_rect.topleft = (SCREEN_WIDTH - 800, 50)
        self.pantalla.blit(texto_contador, texto_contador_rect)

# ---------------------------------------------------------
    def chequear_respuesta(self, input_respuesta):
        """
    Chequea la respuesta ingresada por el jugador y gestiona las acciones correspondientes. Este método verifica si la respuesta ingresada por el jugador está en las respuestas válidas para la pregunta actual

    Args:
        input_respuesta (str): La respuesta ingresada por el jugador.

    Returns:
        None
    """
        # Convertir la respuesta del usuario a minúsculas
        input_respuesta = input_respuesta.lower()
        # Convertir las respuestas correctas a minúsculas
        respuestas = {key.lower(): value for key,
                      value in self.pregunta_actual["respuestas"].items()}
        # Mapeo de respuestas minúsculas a originales
        respuesta_original = {
            key.lower(): key for key in self.pregunta_actual["respuestas"]}

        if input_respuesta in respuestas:
            self.audio_correcto.play()
            puntos_obtenidos = respuestas[input_respuesta] * \
                self.bonus_multiplicar

            # Verificar si la respuesta ya está en respuestas_ingresadas
            if input_respuesta not in [respuesta.lower() for respuesta, _ in self.respuestas_ingresadas]:
                self.puntaje += puntos_obtenidos  # Sumar puntos al puntaje total
                self.puntajes_acumulados.append(puntos_obtenidos)
                self.respuestas_ingresadas.append(
                    (respuesta_original[input_respuesta], puntos_obtenidos))
                # Mostrar respuestas ingresadas ordenadas por puntos
                mostrar_respuestas_ingresadas(self)
        else:
            self.audio_incorrecto.play()
            mostrar_animacion_cruz(self)
            self.oportunidades -= 1
            self.input_respuesta = ""

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

    def limpiar_input_respuesta(self):
        """
    Limpia el campo de entrada de respuesta del usuario.

    Este método establece la variable `input_respuesta` a una cadena vacía, 
    reiniciando así cualquier respuesta previamente ingresada.

    Atributos modificados:
    - input_respuesta (str): Campo de entrada de respuesta del usuario.
    """
        self.input_respuesta = ""

# ---------------------------------------------------------
    def limpiar_respuestas_ingresadas(self):
        """
    Limpia la lista de respuestas ingresadas por el usuario.

    Este método establece la variable `respuestas_ingresadas` a una lista vacía,
    eliminando todas las respuestas que se han ingresado previamente.

    Atributos modificados:
    - respuestas_ingresadas (list): Lista de respuestas ingresadas por el usuario.
    """
        self.respuestas_ingresadas = []

# ---------------------------------------------------------
    def usar_comodin(self, tipo):
        """
    Usa el comodín seleccionado durante el juego, permite al jugador usar diferentes comodines según el tipo especificado
    Args:
        tipo (str): El tipo de comodín a usar.

    Returns:
        None
    """
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
    def chequear_fin_juego(self):
        """
    Chequea si el juego ha llegado a su fin y realiza las acciones finales correspondientes.
    Args:
        None

    Returns:
        None
    """
        if self.contador_rondas == 0:
            self.premio_ganado()
            self.puntaje_total = sum(self.puntajes_acumulados)
            pygame.time.wait(2000)
            self.resetear_juego()

# ---------------------------------------------------------

    def manejar_eventos(self, event):
        """
    Maneja los eventos del juego como presionar teclas o clics de ratón.

    Args:
        event (pygame.event): El evento pygame que se está gestionando.

    Returns:
        None
    """
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                juego.menu_main()
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
    def actualizar_reloj(self):
        """
    Actualiza el reloj del juego y gestiona las acciones correspondientes cuando se agota el tiempo.

    Args:
        None

    Returns:
        None
    """
        self.tiempo_restante -= 1 / FPS
        if self.tiempo_restante <= 0:
            self.oportunidades -= 1
            self.tiempo_restante = RESPONSE_TIME
            if self.oportunidades > 0:
                self.seleccionar_pregunta_aleatoriamente()
                mostrar_pregunta(self)

        if self.oportunidades == 0:
            pygame.time.wait(1000)
            self.resetear_juego()

# ---------------------------------------------------------
    def ejecutar(self):
        """
    Ejecuta el bucle principal del juego,donde se actualizan y muestran en pantalla todos los elementos del juego
    """
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

            self.actualizar_reloj()
            pygame.display.update()
            self.clock.tick(FPS)


# ---------------------------------------------------------


if __name__ == "__main__":
    juego = Juego100ARG()
    juego.ejecutar()


# ---------------------------------------------------------
