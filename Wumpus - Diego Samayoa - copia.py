import pygame
import numpy as np
import threading
import heapq
import ctypes  # An included library with Python install.   

#### ---CONSTANTES---###
# Colores para tablero y participantes
WHITE = (255, 255, 255)  # CASILLA FONDO 0
GREEN = (200,230,201)  # CAZADOR 1

PURPLE = (102, 102, 255)  # POZO 2
LIGHTPURPLE = (179, 179, 255)  # BRISA POZO 6

BLUE = (25, 64, 255)  # WUMPUS 3
LIGHTBLUE = (77, 106, 255)  # OLOR WUMPUS 5

YELLOW = (255, 255, 0)  # ORO 4

BLACK = (0, 0, 0)  # CUADRICULA
RED = (255,0,0) #ROJO RASTRO 9


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
#pos_2 = np.unravel_index(np.random.choice(reservarPosiciones, size=6, replace=False), (10, 10))
grid[pos_2] = 2
pos_2_guardadas = pos_2
print("Los pozos están en: ", pos_2)

# Generamos el número 3 una vez en una posición aleatoria 
pos_3 = np.unravel_index(reservarPosiciones[2], (10, 10))
grid[pos_3] = 3
pos_3_guardadas = pos_3
print("El wumpus está en: ", pos_3)

# Generamos el número 4 una vez en una posición aleatoria 
pos_4 = np.unravel_index(reservarPosiciones[3], (10, 10))
grid[pos_4] = 4
pos_4_guardadas = pos_4
print("El oro está en: ", pos_4)
pos4_tupla = tuple(pos_4)

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
            
            color = GREEN # Color de fondo de tablero
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
            
            #pozo_image = pygame.image.load('monte.png').convert_alpha()
            #screen.blit(pozo_image, ((MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN))
 

            if grid[row][column] == 2:  # POZO BRISA 6
                #color = PURPLE
                pozo.append(row)
                pozo.append(column)
                pozo_image = pygame.image.load('Pozo.png').convert_alpha()
                screen.blit(pozo_image, ((MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN))

                if column < 9:  # DERECHA
                    grid[row][column+1] = 6
                if column > 0:  # IZQUIERDA
                    grid[row][column - 1] = 6
                if row > 0:  # ARRIBA
                    grid[row-1][column] = 6
                if row < 9:  # ABAJO
                    grid[row+1][column] = 6

            elif grid[row][column] == 3:  # WUMPUS OLOR 7
                #color = BLUE
                #wumpus = pygame.image.load("wumpus.png").convert_alpha()
                wumpus_image = pygame.image.load('wumpus.png').convert_alpha()
                screen.blit(wumpus_image, ((MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN))
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

            elif grid[row][column] == 4:  # ORO
                #color = YELLOW
                gold_image = pygame.image.load('Oro.png').convert_alpha()
                screen.blit(gold_image, ((MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN))
                oro.append(row)
                oro.append(column)
                
            elif grid[row][column] == 6:  # PESTILENCIA
                #color = LIGHTPURPLE
                pestilanecia_image = pygame.image.load('Neblina.png').convert_alpha()
                screen.blit(pestilanecia_image, ((MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN))               

            elif grid[row][column] == 7:  # BRISA
                #color = LIGHTBLUE
                brisa_image = pygame.image.load('OlorPozo.png').convert_alpha()
                screen.blit(brisa_image, ((MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN)) 
                

            elif grid[row][column] == 9:  # BRISA
                #color = RED
                piedra_image = pygame.image.load('Piedra.png').convert_alpha()
                screen.blit(piedra_image, ((MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN))  
                #RASTROS
            # Dibujo de cada cuadro en tablero según el color y dimensiones

          
def dibujarCazador():
    imagen = None
    for row in range(10):
        for column in range(10):
            if grid[row][column] == 1: #CAZADOR
                #screen.blit(image, (0, 0))
                cazador_image = pygame.image.load('Cazador.png').convert_alpha()
                imagen = cazador_image
                screen.blit(imagen, ((MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN))
                
                # Se unen las filas y columnas en una lista para conocer su ubicación X Y en el tablero
                #color = GREEN
                cazador.append(row) #[0]
                cazador.append(column) #[1]
            # Dibujar la imagen encima del cuadro si corresponde

                

# Función que dibuja un cuadro en la posición derecha, elimina el cuadro en la posición antigua y acumula la posición

# Función para mover a la derecha
def derecha():
    if cazador[0] < 9:
        grid[cazador[1]][cazador[0]] = 0  # Eliminar anterior
        grid[cazador[1]][cazador[0]+1] = 1  # Dibujar nuevo
        cazador[0] = cazador[0]+1  # Acumular posición
        reposicionar()
        if (cazador[0] == oro[1] and cazador[1] == oro[0]): print("GANASTE")      

# Función para mover a la izquierda
def izquierda():
    if cazador[0] > 0:
        grid[cazador[1]][cazador[0]] = 0  # Eliminar anterior
        grid[cazador[1]][cazador[0]-1] = 1  # Dibujar nuevo
        cazador[0] = cazador[0]-1  # Acumular posición
        reposicionar()
        if (cazador[0] == oro[1] and cazador[1] == oro[0]): print("GANASTE")  
        


# Función para mover hacia abajo
def abajo():
    if cazador[1] < 9:
        grid[cazador[1]][cazador[0]] = 0  # Eliminar anterior
        grid[cazador[1]+1][cazador[0]] = 1  # Dibujar nuevo
        cazador[1] = cazador[1]+1  # Acumular posición
        reposicionar()
        if (cazador[0] == oro[1] and cazador[1] == oro[0]): print("GANASTE")  
        

# Función para mover hacia arriba
def arriba():
    if cazador[1] > 0:
        grid[cazador[1]][cazador[0]] = 0  # Eliminar anterior
        grid[cazador[1]-1][cazador[0]] = 1  # Dibujar nuevo
        cazador[1] = cazador[1]-1  # Acumular posición
        reposicionar()
        if (cazador[0] == oro[1] and cazador[1] == oro[0]): print("GANASTE")  


        #Actualizar pantalla y dibujar nueva posición
def dibujarPos():
        dibujar()
        dibujarCuadricula(screen)
        dibujarCazador()
        clock.tick(10)
        pygame.display.update()

def reposicionar ():
    #grid[0,0] = 1
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


# Define la función de heurística para A* (distancia Manhattan)
def heuristic(current_row, current_col, end_row, end_col):
    return abs(end_row - current_row) + abs(end_col - current_col)


def astar(start, end, grid):
    # Inicializa las estructuras de datos
    open_set = []
    closed_set = set()
    came_from = {}

    # Pone la distancia inicial a 0
    g_score = {start: 0}

    # Pone la heurística inicial a la distancia Manhattan
    h_score = {start: manhattan_distance(start, end)}

    # Calcula la función f(n) para el punto inicial
    f_score = {start: g_score[start] + h_score[start]}

    # Agrega el punto inicial a la lista de abiertos
    heapq.heappush(open_set, (f_score[start], start))

    # Bucle principal
    while len(open_set) > 0:
        # Toma el nodo con la menor función f(n)
        current = heapq.heappop(open_set)[1]

        # Si llegamos al objetivo, reconstruye el camino y lo devuelve
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
                   
            # Agrega el camino encontrado al arreglo y establece el valor 9 en cada posición
            def mostrarRastro():
                for pos in path:
                    grid[pos[0]][pos[1]] = 9

            return path

        # Marca el nodo como cerrado
        closed_set.add(current)

        # Explora los vecinos del nodo actual
        for neighbor in neighbors(current, grid):
            if neighbor in closed_set:
                continue

            # Calcula el costo de llegar al vecino desde el nodo actual
            tentative_g_score = g_score[current] + distance(current, neighbor)

            # Si el vecino no está en la lista de abiertos, agrégalo
            if neighbor not in [i[1] for i in open_set]:
                heapq.heappush(open_set, (f_score.get(neighbor, float('inf')), neighbor))

            # Si el nuevo costo es mayor que el costo existente, ignora este vecino
            elif tentative_g_score >= g_score.get(neighbor, float('inf')):
                continue

            # Este es un camino mejor, registra este camino
            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            h_score[neighbor] = manhattan_distance(neighbor, end)
            f_score[neighbor] = g_score[neighbor] + h_score[neighbor]

    # No se encontró un camino
    return None

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def distance(a, b):
    return manhattan_distance(a, b)

def neighbors(node, grid):
    neighbors = []
    for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        neighbor = (node[0] + direction[0], node[1] + direction[1])
        if (0 <= neighbor[0] < len(grid) and
            0 <= neighbor[1] < len(grid[0]) and
            grid[neighbor[0]][neighbor[1]] not in [2, 3]):
            neighbors.append(neighbor)
    return neighbors

# Ejemplo de uso
inicio = (0,0)
final = pos4_tupla
print(pos4_tupla)

path = astar(inicio, final, grid)
if path is None:
    print("No hay camino hacia el objetivo.")
else:
    print("El camino más corto hacia el objetivo es:", path)


path_invertido = [(y, x) for x, y in path]
#print(path_invertido)

def mover_objeto(path_invertido):
    for coordenada in path_invertido:
        # Si la coordenada es a la derecha del objeto, llama a la función "derecha()"
        if coordenada[0] > cazador[0]:
            print("derecha")
            derecha()
        # Si la coordenada es a la izquierda del objeto, llama a la función "izquierda()"
        elif coordenada[0] < cazador[0]:
            print("izquierda")
            izquierda()
        # Si la coordenada es arriba del objeto, llama a la función "arriba()"
        elif coordenada[1] < cazador[1]:
            print("arriba")
            arriba()
        # Si la coordenada es abajo del objeto, llama a la función "abajo()"
        elif coordenada[1] > cazador[1]:
            print("abajo")
            abajo()


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
        elif keys[pygame.K_p]:
            ctypes.windll.user32.MessageBoxW(0, "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.!", "Instrucciones", 0)

        elif keys[pygame.K_s]:
            mover_objeto(path_invertido)
            if path is not None:
                for pos in path:
                    grid[pos[0]][pos[1]] = 9
                print("El rastro es:", path)
            else:
                print("No hay camino hacia el objetivo.")

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
    dibujarCazador()
    # Limitar juego a 30 FPS por segundo
    clock.tick(60)

    # Actualizar la pantalla con los nuevos datos dibujados
    pygame.display.update()

pygame.quit()