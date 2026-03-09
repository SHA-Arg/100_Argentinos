import pygame
import sys
from .recursos import *
from .config import *
from .utils import *

# ---------------------------------------------------------


def instrucciones():
    """
    Muestra las instrucciones del juego en un panel estético centrado.
    Presionar ESC para volver al menú principal.
    """
    AMARILLO = (255, 215, 0)
    GRIS_CLARO = (200, 200, 200)

    font_titulo = pygame.font.Font(FONT_PATH1, 26)
    font_texto = pygame.font.Font(FONT_PATH2, 16)

    panel_w, panel_h = 700, 400
    panel_x = (SCREEN_WIDTH - panel_w) // 2
    panel_y = (SCREEN_HEIGHT - panel_h) // 2

    instrucciones_texto = [
        ("1. El juego seleccionará una temática al azar.", WHITE),
        ("2. Ingresá tu respuesta antes de que se acabe el tiempo (10 seg).", WHITE),
        ("3. Tenés 3 errores como máximo por ronda.", WHITE),
        ("4. Los puntos se calculan según cuántos argentinos", WHITE),
        ("   coinciden con tu respuesta.", WHITE),
        ("5. Al acumular 500 puntos, ¡ganás el premio mayor!", WHITE),
        ("", WHITE),
        ("Comodines disponibles:", AMARILLO),
        ("  •  Tiempo extra: suma 10 segundos al reloj.", GRIS_CLARO),
        ("  •  Menos votada: revela la respuesta menos popular.", GRIS_CLARO),
        ("  •  Multiplicar puntos: duplica los puntos de la ronda.", GRIS_CLARO),
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fondo del menú
        pantalla.blit(fondo_menu, (0, 0))

        # Panel semi-transparente
        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel.fill((10, 10, 30, 210))
        pantalla.blit(panel, (panel_x, panel_y))

        # Borde dorado
        pygame.draw.rect(pantalla, AMARILLO, (panel_x, panel_y, panel_w, panel_h), 2, border_radius=10)

        # Título
        titulo = font_titulo.render("CÓMO SE JUEGA", True, AMARILLO)
        titulo_rect = titulo.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 28))
        pantalla.blit(titulo, titulo_rect)

        # Línea separadora bajo el título
        pygame.draw.line(pantalla, AMARILLO,
                         (panel_x + 30, panel_y + 50),
                         (panel_x + panel_w - 30, panel_y + 50), 1)

        # Texto de instrucciones
        y = panel_y + 65
        for linea, color in instrucciones_texto:
            surf = font_texto.render(linea, True, color)
            pantalla.blit(surf, (panel_x + 28, y))
            y += 24

        # Línea separadora superior al pie
        pygame.draw.line(pantalla, AMARILLO,
                         (panel_x + 30, panel_y + panel_h - 38),
                         (panel_x + panel_w - 30, panel_y + panel_h - 38), 1)

        # Pie de página
        pie = font_texto.render("Presioná  ESC  para volver al menú", True, GRIS_CLARO)
        pie_rect = pie.get_rect(center=(SCREEN_WIDTH // 2, panel_y + panel_h - 20))
        pantalla.blit(pie, pie_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        pygame.display.update()
# ------------------------------------------------------
