import random
import pygame
import csv
import sys
from Packages.config import *
from Packages.utils import *
from Packages.ordenamiento import *
from Packages.recursos import *
from Packages.mostrar import *
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

        volver_a_jugar = f"\n¿Desea volver a jugar? (S/N)"
        mensaje += "\n" + volver_a_jugar

        # Posición inicial del texto
        x, y = 350, 320

        texto_premio = self.font.render(linea, True, WHITE)
        texto_premio_rect = texto_premio.get_rect(topleft=(x, y))
        self.pantalla.blit(texto_premio, texto_premio_rect)
        # Ajustar la posición Y para la siguiente línea
        y += texto_premio.get_height() + 5
        pygame.display.flip()  # Actualizar la pantalla

        # Se renderiza, posiciona y muestra el mensaje en pantalla|
        x_volver, y_volver = 350, 400
        volver_a_jugar = self.font.render(linea, True, WHITE)
        texto_volver_a_jugar_rect = volver_a_jugar.get_rect(
            topleft=(x_volver, y_volver))
        self.pantalla.blit(volver_a_jugar, texto_volver_a_jugar_rect)


# ---------------------------------------------------------
    """
    Muestra el contador de rondas en la pantalla del juego. Este metodo renderiza el número de la ronda actual en la esquina superior izquierda de la pantalla
    Args:
        None

    Returns:
        None
    """

    # def contador_rondas(self):
    #     texto_contador = self.font.render(
    #         f"Ronda: {self.rondas_jugadas}", True, WHITE)
    #     texto_contador_rect = texto_contador.get_rect()
    #     texto_contador_rect.topleft = (SCREEN_WIDTH - 800, 50)
    #     self.pantalla.blit(texto_contador, texto_contador_rect)

# ---------------------------------------------------------
    def pedir_nombre_jugador(self):
        nombre_jugador = ""
        pedir_nombre_text = self.font.render("Ingresa tu nombre:", True, WHITE)
        pedir_nombre_rect = pedir_nombre_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

        input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100,
                                 SCREEN_HEIGHT // 2, 200, 50)
        activo = True

        while activo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        activo = False
                    elif event.key == pygame.K_BACKSPACE:
                        nombre_jugador = nombre_jugador[:-1]
                    else:
                        nombre_jugador += event.unicode

            self.pantalla.blit(self.fondo_game_over, (0, 0))
            self.pantalla.blit(pedir_nombre_text, pedir_nombre_rect)

            # Actualizar rectángulo de entrada
            pygame.draw.rect(self.pantalla, WHITE, input_rect, 2)
            nombre_surface = self.font.render(nombre_jugador, True, WHITE)
            self.pantalla.blit(
                nombre_surface, (input_rect.x + 5, input_rect.y + 5))
            input_rect.w = max(200, nombre_surface.get_width() + 10)

            pygame.display.flip()

        return nombre_jugador


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
                mostrar_respuestas_ingresadas(juego)

        else:
            mostrar_animacion_cruz(juego)
            self.audio_incorrecto.play()
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
# Limpia el campo de entrada de texto
    def limpiar_input_respuesta(self):
        self.input_respuesta = ""

# ---------------------------------------------------------
    def limpiar_respuestas_ingresadas(self):
        self.respuestas_ingresadas = []
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
