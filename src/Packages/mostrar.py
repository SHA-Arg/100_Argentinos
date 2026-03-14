import pygame
import sys
import csv
from .config import *
from .ordenamiento import *
from .utils import *
from .inicializadores import *
# ---------------------------------------------------------


def mostrar_pregunta(juego):
    """Muestra la pregunta en un panel oscuro a ancho completo en la parte superior."""
    AMARILLO = (255, 215, 0)
    font_preg = pygame.font.Font(FONT_PATH1, 20)

    panel = pygame.Surface((760, 44), pygame.SRCALPHA)
    panel.fill((10, 10, 30, 210))
    juego.pantalla.blit(panel, (20, 10))
    pygame.draw.rect(juego.pantalla, AMARILLO, (20, 10, 760, 44), 1, border_radius=8)

    txt = font_preg.render(juego.pregunta_actual["pregunta"] + "?", True, WHITE)
    juego.pantalla.blit(txt, txt.get_rect(center=(400, 32)))

# ---------------------------------------------------------


def mostrar_input(juego):
    """Muestra el campo de entrada con estilo oscuro y borde dorado."""
    AMARILLO = (255, 215, 0)
    GRIS = (110, 110, 110)
    font_input = pygame.font.Font(FONT_PATH1, 20)
    font_hint = pygame.font.Font(FONT_PATH1, 16)

    rect = pygame.Rect(20, 64, 560, 42)
    pygame.draw.rect(juego.pantalla, (18, 18, 48), rect, border_radius=8)
    pygame.draw.rect(juego.pantalla, AMARILLO, rect, 2, border_radius=8)

    if juego.input_respuesta:
        txt = font_input.render(juego.input_respuesta, True, WHITE)
        juego.pantalla.blit(txt, (rect.x + 12, rect.y + 12))
    else:
        hint = font_hint.render("Escribi tu respuesta y presiona ENTER...", True, GRIS)
        juego.pantalla.blit(hint, (rect.x + 10, rect.y + 13))

# ---------------------------------------------------------


def mostrar_reloj(juego):
    """Muestra el reloj en la columna derecha como círculo con color de alerta."""
    AMARILLO = (255, 215, 0)
    ROJO = (220, 60, 60)
    font_reloj = pygame.font.Font(FONT_PATH1, 20)

    cx, cy, r = 732, 90, 32
    color_borde = ROJO if juego.tiempo_restante <= 5 else AMARILLO

    pygame.draw.circle(juego.pantalla, (10, 10, 30), (cx, cy), r)
    pygame.draw.circle(juego.pantalla, color_borde, (cx, cy), r, 3)

    txt = font_reloj.render(f"{int(juego.tiempo_restante)}s", True, color_borde)
    juego.pantalla.blit(txt, txt.get_rect(center=(cx, cy)))

# ---------------------------------------------------------


def mostrar_rondas_jugadas(juego):
    """Muestra las rondas jugadas en un panel de la columna derecha."""
    AMARILLO = (255, 215, 0)
    font_lbl = pygame.font.Font(FONT_PATH1, 13)
    font_val = pygame.font.Font(FONT_PATH1, 18)

    panel = pygame.Rect(605, 290, 188, 42)
    pygame.draw.rect(juego.pantalla, (10, 10, 30), panel, border_radius=6)
    pygame.draw.rect(juego.pantalla, AMARILLO, panel, 1, border_radius=6)

    lbl = font_lbl.render("RONDA", True, AMARILLO)
    juego.pantalla.blit(lbl, lbl.get_rect(midleft=(panel.x + 10, panel.y + 13)))
    val = font_val.render(f"{juego.rondas_jugadas} / {juego.max_rondas}", True, WHITE)
    juego.pantalla.blit(val, val.get_rect(midright=(panel.right - 10, panel.y + 28)))

# ---------------------------------------------------------


def mostrar_respuestas_ingresadas(juego):
    """Muestra las respuestas ingresadas como filas estilizadas con acento dorado."""
    AMARILLO = (255, 215, 0)
    font_resp = pygame.font.Font(FONT_PATH1, 19)

    respuestas_ordenadas = ordenar_respuestas(juego.respuestas_ingresadas)

    y = 120
    for respuesta, puntos in respuestas_ordenadas:
        fila = pygame.Rect(20, y, 560, 28)
        pygame.draw.rect(juego.pantalla, (18, 18, 50), fila, border_radius=6)
        pygame.draw.rect(juego.pantalla, AMARILLO, (20, y, 4, 28), border_radius=3)

        txt = font_resp.render(f"{respuesta}:", True, WHITE)
        juego.pantalla.blit(txt, (34, y + 6))
        pts = font_resp.render(str(puntos), True, AMARILLO)
        juego.pantalla.blit(pts, pts.get_rect(midright=(570, y + 14)))
        y += 34

# ---------------------------------------------------------


def _dibujar_panel(superficie, x, y, w, h, alpha=210, borde=(255, 215, 0)):
    """Dibuja un panel oscuro semi-transparente con borde coloreado y esquinas redondeadas."""
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    surf.fill((10, 10, 30, alpha))
    superficie.blit(surf, (x, y))
    pygame.draw.rect(superficie, borde, (x, y, w, h), 2, border_radius=8)


def _leer_ranking():
    """Lee el CSV de ranking y retorna lista de [nombre, puntaje_int] ordenada de mayor a menor."""
    try:
        with open('data/ranking.csv', 'r', encoding='utf-8') as f:
            filas = []
            for row in csv.reader(f):
                if len(row) >= 2:
                    try:
                        filas.append([row[0], int(row[1])])
                    except ValueError:
                        pass
            return ordenar_ranking(filas)
    except FileNotFoundError:
        return []


def pedir_nombre_jugador(juego):
    """
    Muestra un panel estético centrado para que el jugador ingrese su nombre.
    Retorna el nombre ingresado (str).
    """
    AMARILLO = (255, 215, 0)
    GRIS = (180, 180, 180)
    font_titulo = pygame.font.Font(FONT_PATH1, 26)
    font_sub = pygame.font.Font(FONT_PATH1, 18)
    font_input = pygame.font.Font(FONT_PATH1, 22)

    panel_w, panel_h = 560, 210
    panel_x = (SCREEN_WIDTH - panel_w) // 2
    panel_y = (SCREEN_HEIGHT - panel_h) // 2

    nombre = ""
    activo = True
    while activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and nombre.strip():
                    activo = False
                elif event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif len(nombre) < 20:
                    nombre += event.unicode

        juego.pantalla.blit(juego.fondo_game_over, (0, 0))
        ov = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 150))
        juego.pantalla.blit(ov, (0, 0))

        _dibujar_panel(juego.pantalla, panel_x, panel_y, panel_w, panel_h)

        t_titulo = font_titulo.render("INGRESÁ TU NOMBRE", True, AMARILLO)
        juego.pantalla.blit(t_titulo, t_titulo.get_rect(
            center=(SCREEN_WIDTH // 2, panel_y + 32)))

        pygame.draw.line(juego.pantalla, AMARILLO,
                         (panel_x + 20, panel_y + 57),
                         (panel_x + panel_w - 20, panel_y + 57), 1)

        inp_w, inp_h = 420, 44
        inp_x = (SCREEN_WIDTH - inp_w) // 2
        inp_y = panel_y + 74
        pygame.draw.rect(juego.pantalla, (30, 30, 60),
                         (inp_x, inp_y, inp_w, inp_h), border_radius=6)
        pygame.draw.rect(juego.pantalla, AMARILLO,
                         (inp_x, inp_y, inp_w, inp_h), 2, border_radius=6)

        cursor = "|" if pygame.time.get_ticks() % 900 < 450 else " "
        surf_nombre = font_input.render(nombre + cursor, True, WHITE)
        juego.pantalla.blit(surf_nombre, (inp_x + 10, inp_y + 9))

        t_sub = font_sub.render("Ingresá tu nombre y presioná ENTER", True, GRIS)
        juego.pantalla.blit(t_sub, t_sub.get_rect(
            center=(SCREEN_WIDTH // 2, inp_y + inp_h + 22)))

        t_max = font_sub.render("(máximo 20 caracteres)", True, (120, 120, 120))
        juego.pantalla.blit(t_max, t_max.get_rect(
            center=(SCREEN_WIDTH // 2, inp_y + inp_h + 46)))

        pygame.display.flip()

    return nombre.strip() or "Anónimo"

# -------------------------------------------------


def mostrar_ranking(juego):
    """
    Dibuja el top-5 del ranking en un panel estético dentro de la pantalla actual.
    """
    AMARILLO = (255, 215, 0)
    GRIS = (180, 180, 180)
    COLORES_TOP = [(255, 215, 0), (192, 192, 192), (205, 127, 50)]  # oro, plata, bronce

    font_titulo = pygame.font.Font(FONT_PATH1, 20)
    font_fila = pygame.font.Font(FONT_PATH1, 17)

    panel_w, panel_h = 700, 220
    panel_x = (SCREEN_WIDTH - panel_w) // 2
    panel_y = 285

    _dibujar_panel(juego.pantalla, panel_x, panel_y, panel_w, panel_h)

    t = font_titulo.render("RANKING", True, AMARILLO)
    juego.pantalla.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 20)))
    pygame.draw.line(juego.pantalla, AMARILLO,
                     (panel_x + 20, panel_y + 38),
                     (panel_x + panel_w - 20, panel_y + 38), 1)

    ranking = _leer_ranking()[:5]
    if not ranking:
        sin_datos = font_fila.render("Aún no hay puntajes registrados.", True, GRIS)
        juego.pantalla.blit(sin_datos, sin_datos.get_rect(
            center=(SCREEN_WIDTH // 2, panel_y + 120)))
    else:
        y = panel_y + 52
        for i, (nombre, pts) in enumerate(ranking):
            color = COLORES_TOP[i] if i < 3 else WHITE
            pos_surf = font_fila.render(f"{i + 1}.", True, color)
            nom_surf = font_fila.render(str(nombre)[:26], True, color)
            pts_surf = font_fila.render(f"{pts} pts", True, color)
            juego.pantalla.blit(pos_surf, (panel_x + 20, y))
            juego.pantalla.blit(nom_surf, (panel_x + 58, y))
            juego.pantalla.blit(pts_surf, (panel_x + panel_w - 100, y))
            y += 32

# ---------------------------------------------------------


def mostrar_pantalla_final(juego):
    """
    Pantalla final completa: muestra el resultado del jugador, el ranking
    y botones para jugar de nuevo o salir.
    """
    AMARILLO = (255, 215, 0)
    VERDE = (80, 200, 120)
    ROJO = (220, 60, 60)
    GRIS = (180, 180, 180)

    font_titulo = pygame.font.Font(FONT_PATH1, 27)
    font_premio = pygame.font.Font(FONT_PATH1, 21)
    font_sub = pygame.font.Font(FONT_PATH1, 16)
    font_btn = pygame.font.Font(FONT_PATH1, 19)

    total = sum(juego.puntajes_acumulados)

    if total >= 500:
        juego.premio = 1_000_000
        titulo_txt = "GANASTE EL GRAN PREMIO!"
        premio_txt = "$ 1.000.000"
        color_titulo = AMARILLO
        color_premio = VERDE
        color_borde = AMARILLO
    elif total == 0:
        titulo_txt = "SIN PUNTOS  -  MEJOR SUERTE!"
        premio_txt = "No ganaste puntos esta vez."
        color_titulo = ROJO
        color_premio = GRIS
        color_borde = ROJO
    else:
        pozo = total * 500
        titulo_txt = "BUEN JUEGO!"
        premio_txt = f"Ganaste: ${pozo:,}   ({total} pts)".replace(",", ".")
        color_titulo = VERDE
        color_premio = WHITE
        color_borde = VERDE

    # Fase 1: pedir nombre y guardar puntaje
    nombre_jugador = pedir_nombre_jugador(juego)
    guardar_puntaje(nombre_jugador, total)

    # Fase 2: pantalla de resultados interactiva
    btn_jugar = pygame.Rect(SCREEN_WIDTH // 2 - 220, 530, 200, 46)
    btn_salir = pygame.Rect(SCREEN_WIDTH // 2 + 20, 530, 200, 46)

    esperando = True
    clock = pygame.time.Clock()
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    juego.rondas_jugadas = 0
                    juego.resetear_juego()
                    esperando = False
                elif event.key == pygame.K_n:
                    mostrar_pantalla_agradecimiento(juego)
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_jugar.collidepoint(event.pos):
                    juego.rondas_jugadas = 0
                    juego.resetear_juego()
                    esperando = False
                elif btn_salir.collidepoint(event.pos):
                    mostrar_pantalla_agradecimiento(juego)
                    pygame.quit()
                    sys.exit()

        juego.pantalla.blit(juego.fondo_game_over, (0, 0))
        ov = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 145))
        juego.pantalla.blit(ov, (0, 0))

        # --- Panel resultado ---
        _dibujar_panel(juego.pantalla, 50, 12, 700, 155, borde=color_borde)
        t1 = font_titulo.render(titulo_txt, True, color_titulo)
        juego.pantalla.blit(t1, t1.get_rect(center=(SCREEN_WIDTH // 2, 52)))
        pygame.draw.line(juego.pantalla, color_borde, (70, 78), (730, 78), 1)
        t2 = font_premio.render(premio_txt, True, color_premio)
        juego.pantalla.blit(t2, t2.get_rect(center=(SCREEN_WIDTH // 2, 110)))
        t3 = font_sub.render(f"Jugador: {nombre_jugador}", True, GRIS)
        juego.pantalla.blit(t3, t3.get_rect(center=(SCREEN_WIDTH // 2, 148)))

        # --- Ranking ---
        mostrar_ranking(juego)

        # --- Botones con hover ---
        mx, my = pygame.mouse.get_pos()
        for btn, label, color_base in [
            (btn_jugar, "[ S ]  JUGAR DE NUEVO", VERDE),
            (btn_salir, "[ N ]  SALIR", ROJO),
        ]:
            hover = btn.collidepoint(mx, my)
            fill = color_base if hover else (25, 25, 55)
            pygame.draw.rect(juego.pantalla, fill, btn, border_radius=8)
            pygame.draw.rect(juego.pantalla, color_base, btn, 2, border_radius=8)
            lbl = font_btn.render(label, True, WHITE)
            juego.pantalla.blit(lbl, lbl.get_rect(center=btn.center))

        pygame.display.flip()
        clock.tick(60)

# ---------------------------------------------------------


def mostrar_animacion_cruz(juego):
    """
    Muestra una animación de cruz roja en la pantalla del juego. Este método posiciona y muestra una animación de cruz roja

    Args:
        None

    Returns:
        None
    """
    cruz_rect = juego.cruz_roja_gif.get_rect()
    cruz_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    juego.pantalla.blit(juego.cruz_roja_gif, cruz_rect)
    pygame.display.update()
    pygame.time.delay(1000)

# ---------------------------------------------------------


def mostrar_puntaje(juego):
    """Muestra el puntaje en la esquina inferior izquierda de la pantalla."""
    AMARILLO = (255, 215, 0)
    font_lbl = pygame.font.Font(FONT_PATH1, 13)
    font_pts = pygame.font.Font(FONT_PATH1, 24)

    # Posición esquina inferior izquierda
    x = 20
    y = SCREEN_HEIGHT - 70
    panel = pygame.Rect(x, y, 160, 60)
    pygame.draw.rect(juego.pantalla, (10, 10, 30), panel, border_radius=6)
    pygame.draw.rect(juego.pantalla, AMARILLO, panel, 2, border_radius=6)

    lbl = font_lbl.render("PUNTAJE", True, AMARILLO)
    juego.pantalla.blit(lbl, (x + 10, y + 10))
    pts = font_pts.render(str(juego.puntaje), True, WHITE)
    juego.pantalla.blit(pts, (x + 10, y + 30))

# ---------------------------------------------------------


def mostrar_oportunidades(juego):
    """Muestra las vidas restantes como círculos de colores en la columna derecha."""
    ROJO = (220, 60, 60)
    GRIS_OSC = (50, 50, 50)
    font_lbl = pygame.font.Font(FONT_PATH1, 13)

    panel = pygame.Rect(605, 213, 188, 62)
    pygame.draw.rect(juego.pantalla, (10, 10, 30), panel, border_radius=6)
    pygame.draw.rect(juego.pantalla, ROJO, panel, 2, border_radius=6)

    lbl = font_lbl.render("VIDAS", True, ROJO)
    juego.pantalla.blit(lbl, lbl.get_rect(center=(panel.centerx, panel.y + 16)))

    cx_start = panel.x + 34
    for i in range(3):
        color = ROJO if i < juego.oportunidades else GRIS_OSC
        cx = cx_start + i * 42
        cy = panel.y + 44
        pygame.draw.circle(juego.pantalla, color, (cx, cy), 14)
        if i >= juego.oportunidades:
            pygame.draw.circle(juego.pantalla, (80, 80, 80), (cx, cy), 14, 2)

# ---------------------------------------------------------


def mostrar_comodines(juego):
    """Muestra los comodines como botones estilizados; grisado si ya fueron usados."""
    AMARILLO = (255, 215, 0)
    GRIS = (70, 70, 70)
    font_lbl = pygame.font.Font(FONT_PATH1, 13)
    font_cmd = pygame.font.Font(FONT_PATH1, 14)

    datos = [
        ("tiempo_extra",        "TIEMPO EXTRA",     "+10s"),
        ("menos_votada",        "MENOS VOTADA",     "REVEAL"),
        ("multiplicar_puntos",  "x2 PUNTOS",        "x2"),
    ]

    y_start = 345
    gap = 52

    for i, (clave, nombre, icono) in enumerate(datos):
        usado = juego.used_hints[clave]
        rect = pygame.Rect(605, y_start + i * gap, 188, 42)

        borde = GRIS if usado else AMARILLO
        fill = (25, 25, 25) if usado else (10, 10, 40)
        pygame.draw.rect(juego.pantalla, fill, rect, border_radius=6)
        pygame.draw.rect(juego.pantalla, borde, rect, 2, border_radius=6)

        txt_color = (80, 80, 80) if usado else WHITE
        lbl = font_cmd.render(nombre, True, txt_color)
        juego.pantalla.blit(lbl, lbl.get_rect(midleft=(rect.x + 10, rect.centery)))

        if usado:
            used_txt = font_lbl.render("USADO", True, GRIS)
            juego.pantalla.blit(used_txt, used_txt.get_rect(midright=(rect.right - 8, rect.centery)))
        else:
            ico = font_lbl.render(icono, True, AMARILLO)
            juego.pantalla.blit(ico, ico.get_rect(midright=(rect.right - 8, rect.centery)))

        # Almacenar rect para detección de clicks
        if clave == "tiempo_extra":
            juego.comodin_tiempo_extra_rect = rect
        elif clave == "menos_votada":
            juego.comodin_menos_votada_rect = rect
        else:
            juego.comodin_multiplicar_puntos_rect = rect

# ---------------------------------------------------------


def mostrar_pantalla_agradecimiento(juego):
    """
    Muestra una pantalla de despedida estética y espera 3 segundos antes de cerrar.
    """
    AMARILLO = (255, 215, 0)
    GRIS = (180, 180, 180)
    font_grande = pygame.font.Font(FONT_PATH1, 30)
    font_chico = pygame.font.Font(FONT_PATH1, 18)

    juego.pantalla.blit(juego.fondo_game_over, (0, 0))
    ov = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 160))
    juego.pantalla.blit(ov, (0, 0))

    panel_w, panel_h = 580, 130
    panel_x = (SCREEN_WIDTH - panel_w) // 2
    panel_y = (SCREEN_HEIGHT - panel_h) // 2

    _dibujar_panel(juego.pantalla, panel_x, panel_y, panel_w, panel_h)

    t1 = font_grande.render("Gracias por jugar!", True, AMARILLO)
    juego.pantalla.blit(t1, t1.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 42)))

    t2 = font_chico.render("Hasta la proxima  *  100 Argentinos Dicen", True, GRIS)
    juego.pantalla.blit(t2, t2.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 92)))

    pygame.display.update()
    pygame.time.wait(3000)

# ---------------------------------------------------------
