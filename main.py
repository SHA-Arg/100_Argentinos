import random
import pygame
import csv
import sys
from Packages.config import *
from Packages.utils import *
from Packages.ordenamiento import *
from Packages.recursos import *
from Packages.motrar import *
from Packages.inicializadores import *

# ---------------------------------------------------------


class Juego100ARG:
    def __init__(self):
        # Inicializa pygame y los componentes del juego
        inicializar_pygame()
        self.audio_correcto, self.audio_incorrecto = cargar_sonidos()
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
                mostrar_respuestas_ingresadas(juego)
        else:
            # self.mostrar_animacion_cruz(juego)
            self.audio_incorrecto.play()
            self.oportunidades -= 1
            self.input_respuesta = ""
            if self.oportunidades == 0:
                pygame.time.wait(1000)
                self.rondas_jugadas += 1
                if self.rondas_jugadas >= self.max_rondas:
                    mostrar_pantalla_final(self)
                    return
                self.resetear_juego()
                return

        self.limpiar_input_respuesta()

        if len(self.respuestas_ingresadas) == len(respuestas):
            self.seleccionar_pregunta_aleatoriamente()
            self.respuestas_ingresadas = []

        if self.puntaje >= 500:
            mostrar_game_over(self)
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

# # ---------------------------------------------------------
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
            mostrar_game_over(juego)
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

# # ---------------------------------------------------------
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

# # ---------------------------------------------------------
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
            mostrar_game_over(juego)
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
            mostrar_pregunta(self)
            mostrar_reloj(self)
            mostrar_input(self)
            mostrar_puntaje(self)
            mostrar_oportunidades(self)
            mostrar_comodines(self)
            mostrar_puntaje(self)
            mostrar_respuestas_ingresadas(self)
            for event in pygame.event.get():
                self.manejar_eventos(event)

            if self.oportunidades == 0:
                self.limpiar_input_respuesta()
                self.partidas_jugadas += 1
                self.chequear_fin_juego()

            if self.puntaje >= 500:
                mostrar_game_over(self)
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
