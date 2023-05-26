import pygame

# Definir constantes
WIDTH = 100
HEIGHT = 100
MARGIN = 1
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Definir la función para reiniciar el juego
def reiniciar_juego():
    # Aquí debes reiniciar todas las variables y objetos necesarios para comenzar una nueva partida
    print("El juego se ha reiniciado.")

# Definir la clase para representar el botón
class Boton:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text

    def dibujar(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.SysFont(None, 24)
        text = font.render(self.text, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

# Inicializar pygame
pygame.init()

# Establecer las dimensiones de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Crear un botón para reiniciar el juego
reiniciar_boton = Boton(10, 10, 100, 50, GREEN, "Reiniciar")

# -------- Loop principal -----------
done = False
clock = pygame.time.Clock()

while not done:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if reiniciar_boton.rect.collidepoint(pos):
                reiniciar_juego()

    # Resto del código...

    # Dibujar el botón de reinicio
    reiniciar_boton.dibujar(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
