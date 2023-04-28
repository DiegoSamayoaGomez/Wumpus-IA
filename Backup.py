import pygame
import numpy as np
import threading

#### ---CONSTANTES---###
# Colores para tablero y participantes
WHITE = (255, 255, 255)  # CASILLA FONDO 0
GREEN = (153, 255, 102)  # CAZADOR 1

PURPLE = (102, 102, 255)  # POZO 2
LIGHTPURPLE = (179, 179, 255)  # BRISA POZO 6

BLUE = (25, 64, 255)  # WUMPUS 3
LIGHTBLUE = (77, 106, 255)  # OLOR WUMPUS 5

YELLOW = (255, 255, 0)  # ORO 4

BLACK = (0, 0, 0)  # CUADRICULA

# Establecer el ancho y alto para cada cuadro individual
WIDTH = 64
HEIGHT = 64

# Margen en cada celda
MARGIN = 0
#### ---CONSTANTES---###

# Creación de array 2D formado por dos listas individuales
# Fue poblado unicamente con números 0
grid = []  # Inicio de array para tablero 0
cazador = []  # Inicio de array para cazador 1
wumpus = []  # Inicio de array para wumpus 2
pozo = [] #
oro = []

# Crear tablero 10x10 para el juego
grid = np.zeros((10, 10))

# Inserta el valor 1 en la posición indicada lo que indicará al tablero de dibujar al cazador
grid[0, 0] = 1

# Generamos una lista de posibles posiciones aleatorias para los números 2, 3 y 4
reservarPosiciones = list(range(10*10-9))
reservarPosiciones.remove(0) # Excluir la posición (0,0)
reservarPosiciones.remove(1) # Excluir la posición (0,1)
reservarPosiciones.remove(2) # Excluir la posición (0,2)

reservarPosiciones.remove(10) # Excluir la posición (1,0)
reservarPosiciones.remove(11) # Excluir la posición (1,1)
reservarPosiciones.remove(12) # Excluir la posición (1,2)

reservarPosiciones.remove(20) # Excluir la posición (2,0)
reservarPosiciones.remove(21) # Excluir la posición (2,1)
reservarPosiciones.remove(22) # Excluir la posición (2,2)

reservarPosiciones = np.random.permutation(reservarPosiciones)
#print(reservarPosiciones)

# Generamos el número 2 dos veces en posiciones aleatorias 
pos_2 = np.unravel_index(reservarPosiciones[0:2], (10, 10))
grid[pos_2] = 2
pos_2_guardadas = pos_2

# Generamos el número 3 una vez en una posición aleatoria 
pos_3 = np.unravel_index(reservarPosiciones[2], (10, 10))
grid[pos_3] = 3
pos_3_guardadas = pos_3

# Generamos el número 4 una vez en una posición aleatoria 
pos_4 = np.unravel_index(reservarPosiciones[3], (10, 10))
grid[pos_4] = 4
pos_4_guardadas = pos_4

'''
# En las posiciones reservadas se genera el número 0
#Posición [0, 0] es para el cazador
grid[0, 1] = 0
grid[0, 2] = 0

grid[1, 0] = 0
grid[1, 1] = 0
grid[1, 2] = 0

grid[2, 0] = 0
grid[2, 1] = 0
grid[2, 2] = 0
'''
# Imprimir tablero
print(grid)

# Establece el ancho y alto del tablero (10 cuadros de 64 pixeles = 640)
WINDOW_SIZE = [640, 640]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Establece el título del juego
pygame.display.set_caption("Wumpus")

# El ciclo principal del juego se recorre hasta que se interrumpa con una tecla especial o con el botón de cerrar
done = False

# Reloj proveído por PyGame para que el juego sea independiente de FPS
# El juego correrá a la misma velocidad en cualquier dispositivo
clock = pygame.time.Clock()
running = True
traversing = False
traversal_thread = None

running = True
traversing = False
traversal_thread = None

# Dibujo de la cuadricula del tablero en base al ancho y alto de los cuadros
def dibujarCuadricula(screen):
    for i in range(10):
        new_height = round(i * HEIGHT)
        new_width = round(i * WIDTH)
        pygame.draw.line(screen, BLACK, (0, new_height), (640, new_height), 1)
        pygame.draw.line(screen, BLACK, (new_width, 0), (new_width, 640), 1)



def dibujar():
    for row in range(10):        
        for column in range(10):            
            color = WHITE # Color de fondo de tablero 
            if grid[row][column] == 1: #CAZADOR
                '''
                # Cargar la imagen
                cazador_image = pygame.image.load("wumpus.png")
                cazador_rect = cazador_image.get_rect() # Obtiene el rectángulo que contiene la imagen del cazador
                cazador_rect.x = (MARGIN + WIDTH) * column + MARGIN # Establece la posición x del rectángulo a la posición donde se dibuja el rectángulo
                cazador_rect.y = (MARGIN + HEIGHT) * row + MARGIN # Establece la posición y del rectángulo a la posición donde se dibuja el rectángulo
                screen.blit(cazador_image, cazador_rect) # Dibuja la imagen del cazador en el rectángulo en la superficie de juego
                '''
                color = GREEN

                # Se unen las filas y columnas en una lista para conocer su ubicación X Y en el tablero
                #color = GREEN
                cazador.append(row) #[0]
                cazador.append(column) #[1]

            if grid[row][column] == 2:  # POZO BRISA 6
                color = PURPLE
                pozo.append(row)
                pozo.append(column)

                if column < 9:  # DERECHA
                    grid[row][column+1] = 6
                if column > 0:  # IZQUIERDA
                    grid[row][column - 1] = 6
                if row > 0:  # ARRIBA
                    grid[row-1][column] = 6
                if row < 9:  # ABAJO
                    grid[row+1][column] = 6

            if grid[row][column] == 3:  # WUMPUS OLOR 7
                color = BLUE
                #wumpus = pygame.image.load("wumpus.png").convert_alpha()
                wumpus.append(row)
                wumpus.append(column)

                if column < 9:  # DERECHA
                    grid[row][column+1] = 7
                if column > 0:  # IZQUIERDA
                    grid[row][column - 1] = 7
                if row > 0:  # ARRIBA
                    grid[row-1][column] = 7
                if row < 9:  # ABAJO
                    grid[row+1][column] = 7

            if grid[row][column] == 4:  # ORO
                color = YELLOW
                oro.append(row)
                oro.append(column)
                

            if grid[row][column] == 6:  # PESTILENCIA
                color = LIGHTPURPLE

            if grid[row][column] == 7:  # BRISA
                color = LIGHTBLUE

            # Dibujo de cada cuadro en tablero según el color y dimensiones
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
'''       
def dibujarCazador():
     color = GREEN # Color de fondo de tablero 
     for row in range(1):
        for column in range(1):
            if grid[row][column] == 1:  # CAZADOR
                color = GREEN
                # Se unen las filas y columnas en una lista para conocer su ubicación X Y en el tablero
                cazador.append(row)  # [0]
                cazador.append(column)  # [1]
            pygame.draw.rect(screen, color, 
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

'''
# Función que dibuja un cuadro en la posición derecha, elimina el cuadro en la posición antigua y acumula la posición

def derecha():
    if cazador[0] < 9:
        grid[cazador[1]][cazador[0]] = 0  # Eliminar anterior
        grid[cazador[1]][cazador[0]+1] = 1  # Dibujar nuevo
        cazador[0] = cazador[0]+1  # Acumular posición
        reposicionar()


# Función que dibuja un cuadro en la posición izquierda, elimina el cuadro en la posición antigua y acumula la posición

def izquierda():
    if cazador[0] > 0:
        grid[cazador[1]][cazador[0]] = 0
        grid[cazador[1]][cazador[0]-1] = 1
        cazador[0] = cazador[0]-1
        reposicionar()


# Función que dibuja un cuadro en la posición inferior, elimina el cuadro en la posición antigua y acumula la posición

def abajo():
    if cazador[1] < 9:
        grid[cazador[1]][cazador[0]] = 0
        grid[cazador[1]+1][cazador[0]] = 1
        cazador[1] = cazador[1]+1
        reposicionar()

# Función que dibuja un cuadro en la posición superior, elimina el cuadro en la posición antigua y acumula la posición

def arriba():
    if cazador[1] > 0:
        grid[cazador[1]][cazador[0]] = 0
        grid[cazador[1]-1][cazador[0]] = 1
        cazador[1] = cazador[1]-1
        reposicionar()


        #Actualizar pantalla y dibujar nueva posición
def dibujarPos():
        dibujar()
        dibujarCuadricula(screen)
        #dibujarCazador()
        clock.tick(30)
        pygame.display.update()

def reposicionar ():
    grid[pos_2_guardadas]=2
    grid[pos_3_guardadas]=3
    grid[pos_4_guardadas]=4

def recorridoAutomatico():
    for x in range(5):
        for y in range(9):
            derecha()
            dibujarPos()
        
        abajo()
        dibujarPos()

        for y in range(9):
            izquierda()
            dibujarPos()
        
        abajo()
        dibujarPos()

    for y in range(9):
        arriba()
        dibujarPos()


# -------- Loop principal -----------
while not done:
    keys = pygame.key.get_pressed()  # Almacenar información de tecla presionada
    for event in pygame.event.get():  # Se crea un evento cada vez que se presione alguna tecla o si se usa el mouse
        if event.type == pygame.QUIT:  # Cerrar el juego al concluir el ciclo
            running = False
            done = True  # Se termina el ciclo al presionar el botón cerrar
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Conseguir la posición del mouse cuando se realiza un click
            pos = pygame.mouse.get_pos()
            # Las coordenadas son por pixeles, se realiza la conversión a coordenadas X Y
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            # Imprimir coordenadas de pixeles y ejes X Y al hacer click
            print("Click ", pos, "Coordenadas de tablero: ", row, column)

    # ----- Controles de juego -----#

        
        # Al presionar la tecla de flecha derecha se llama la función derecha() la cual mueve el cuadro en dicha posición
        elif keys[pygame.K_RIGHT]:
            derecha()
        # Al presionar la tecla de flecha izquierda se llama la función izquierda() la cual mueve el cuadro en dicha posición
        elif keys[pygame.K_LEFT]:
            izquierda()
        # Al presionar la tecla de flecha abajo se llama la función abajo() la cual mueve el cuadro en dicha posición
        elif keys[pygame.K_DOWN]:
            abajo()
        # Al presionar la tecla de flecha arriba se llama la función arriba() la cual mueve el cuadro en dicha posición
        elif keys[pygame.K_UP]:
            arriba()

        elif keys[pygame.K_SPACE]:

            #xd
            if not traversing:
                    # iniciar el hilo de recorrido del tablero
                    traversal_thread = threading.Thread(target=recorridoAutomatico)
                    traversal_thread.start()
                    traversing = True
            else:
                    # interrumpir el hilo de recorrido del tablero
                    traversing = False

            # Al presionar la tecla espacio se inicia el movimiento automático del juego


    # Establer color de fondo de pantalla
    screen.fill(BLACK)
    # Dibujar cuadros según su color
    dibujar()
    # Dibujar cuadrícula del tablero
    dibujarCuadricula(screen)

    #Dibujar cuadrícula del cazador
    #dibujarCazador()
    # Limitar juego a 30 FPS por segundo
    clock.tick(30)

    # Actualizar la pantalla con los nuevos datos dibujados
    pygame.display.update()

pygame.quit()