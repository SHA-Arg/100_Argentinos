import pygame
import sys

# Inicializa Pygame
pygame.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Juego 100 Argentinos dicen')

# Fuente
font = pygame.font.Font(None, 36)

#------------------------------------------------------
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

#------------------------------------------------------
def main_menu():
    while True:
        screen.fill(WHITE)

        draw_text('Juego 100 Argentinos dicen', font, BLACK,
                  screen, WIDTH // 2, HEIGHT // 4)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(WIDTH // 3, HEIGHT // 2, 200, 50)
        button_2 = pygame.Rect(WIDTH // 3, HEIGHT // 2 + 70, 200, 50)
        button_3 = pygame.Rect(WIDTH // 3, HEIGHT // 2 + 140, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                instructions()
        if button_3.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        pygame.draw.rect(screen, BLUE, button_1)
        pygame.draw.rect(screen, BLUE, button_2)
        pygame.draw.rect(screen, BLUE, button_3)

        draw_text('Jugar', font, WHITE, screen,
                  button_1.centerx, button_1.centery)
        draw_text('Instrucciones', font, WHITE, screen,
                  button_2.centerx, button_2.centery)
        draw_text('Salir', font, WHITE, screen,
                  button_3.centerx, button_3.centery)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

#------------------------------------------------------
def game():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        draw_text('El juego a comenzado', font, BLACK,
                  screen, WIDTH // 2, HEIGHT // 2)

        pygame.display.update()

#------------------------------------------------------
def instructions():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        draw_text('Instrucciones del juego', font,
                  BLACK, screen, WIDTH // 2, HEIGHT // 2)
        draw_text('Presiona ESC para volver al menú', font,
                  BLACK, screen, WIDTH // 2, HEIGHT // 2 + 50)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        pygame.display.update()


main_menu()
