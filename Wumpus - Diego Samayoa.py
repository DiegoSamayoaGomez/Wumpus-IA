import pygame
import numpy as np  

####---CONSTANTES---###
# Colores para tablero y participantes
WHITE = (255, 255, 255) # CASILLA FONDO 0
GREEN = (153,255,102) #CAZADOR 1

PURPLE = (102,102,255) #WUMPUS 2
LIGHTPURPLE = (179,179,255) #PESTILENCIA WUMPUS 6

BLUE = (25,64,255) #POZO 3 - POZO 5
LIGHTBLUE = (77,106,255) #BRISA POZO 7

YELLOW = (255, 255, 0) #ORO 4

BLACK = (0,0,0) #CUADRICULA

#Color


# Establecer el ancho y alto para cada cuadro individual
WIDTH = 64
HEIGHT = 64
 
# Margen en cada celda
MARGIN = 0
####---CONSTANTES---###

# Creación de array 2D formado por dos listas individuales
# Fue poblado unicamente con números 0 
grid = [] # Inicio de array para tablero 0
cazador = [] # Inicio de array para cazador 1
wumpus = [] # Inicio de array para wumpus 2


'''
for row in range(10): #Se crean las filas del tablero
    grid.append([])
    for column in range(10): #Se crean las columnas del tablero
        grid[row].append(0)  # Se combinan las celdas y se llena con ceros
'''

grid = np.zeros((10, 10), dtype=int)

arr = np.arange(2,7)
poblarX= np.random.permutation(10)
arr = np.arange(2,7)
poblarY= np.random.permutation(10)


# Genera números del 1 al 4 sin repetición
# Los números generados se insertan aleatoriamente en el tablero
# Se ignora el número 1 ya que este es el cazador y siempre aparecerá en la posición [0] [0] del tablero
i=1
#poblarX = np.random.permutation(10)[:6]
#poblarY = np.random.permutation(10)[:6]
for i in range(2,6):
    grid[poblarX[i]][poblarY[i]] = i

    #print(i)

grid[0][0] = 1
# Inserta el valor 1 en la posición indicada lo que indicará al tablero de dibujar al cazador

print(grid)
 
# Inicio de pygame
pygame.init()
 
# Establece el ancho y alto del tablero (10 cuadros de 64 pixeles = 640)
WINDOW_SIZE = [640,640]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Establece el título del juego
pygame.display.set_caption("Wumpus")

# El ciclo principal del juego se recorre hasta que se interrumpa con una tecla especial o con el botón de cerrar
done = False
 
# Reloj proveído por PyGame para que el juego sea independiente de FPS
# El juego correrá a la misma velocidad en cualquier dispositivo
clock = pygame.time.Clock()

# Dibujo de la cuadricula del tablero en base al ancho y alto de los cuadros 
def dibujar_cuadricula(screen):
    for i in range(10):
        new_height = round(i * HEIGHT)
        new_width = round(i * WIDTH)
        pygame.draw.line(screen, BLACK, (0, new_height), (640, new_height), 1)
        pygame.draw.line(screen, BLACK, (new_width, 0), (new_width, 640), 1)

# Dibujo de los cuadros que llenarán cada cuadrícula del tablero en base al color de cada participante
def dibujar():       
    for row in range(10):        
        for column in range(10):            
            color = WHITE # Color de fondo de tablero 
            if grid[row][column] == 1: #CAZADOR
                color = GREEN
                # Se unen las filas y columnas en una lista para conocer su ubicación X Y en el tablero
                cazador.append(row) #[0]
                cazador.append(column) #[1]

            if grid[row][column] == 2: #WUMPUS
                color = PURPLE
                
                """ 
                wumpus.append(row)
                wumpus.append(column)
                """     
        
                if column < 9: #DERECHA 
                    grid[row][column+1] = 6                
                if column > 0: #IZQUIERDA 
                    grid[row][column -1] = 6
                if row >0: #ARRIBA 
                    grid[row-1] [column] = 6
                if row <9: #ABAJO 
                    grid[row+1] [column] = 6


            if grid[row][column] == 3: #POZO
                color = BLUE
                if column < 9: #DERECHA 
                    grid[row][column+1] = 7                
                if column > 0: #IZQUIERDA 
                    grid[row][column -1] = 7
                if row >0: #ARRIBA 
                    grid[row-1] [column] = 7
                if row <9: #ABAJO 
                    grid[row+1] [column] = 7

            if grid[row][column] == 4: #ORO
                color = YELLOW
            if grid[row][column] == 5: #POZO 2
                color = BLUE

                if column < 9: #DERECHA 
                    grid[row][column+1] = 7                
                if column > 0: #IZQUIERDA 
                    grid[row][column -1] = 7
                if row >0: #ARRIBA 
                    grid[row-1] [column] = 7
                if row <9: #ABAJO 
                    grid[row+1] [column] = 7      

            if grid[row][column] == 6: #PESTILENCIA
                color = LIGHTPURPLE
            if grid[row][column] == 7: #BRISA
                color = LIGHTBLUE
            
                
            
            #Dibujo de cada cuadro en tablero según el color y dimensiones
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

# Función que dibuja un cuadro en la posición derecha, elimina el cuadro en la posición antigua y acumula la posición
def derecha():
    if cazador[0] <9:
        grid[cazador[1]][cazador[0]]=0 #Eliminar anterior
        grid[cazador[1]][cazador[0]+1]=1 #Dibujar nuevo
        cazador[0] = cazador[0]+1 #Acumular posición

# Función que dibuja un cuadro en la posición izquierda, elimina el cuadro en la posición antigua y acumula la posición
def izquierda():
    if cazador[0]>0:
        grid[cazador[1]][cazador[0]]=0
        grid[cazador[1]][cazador[0]-1]=1
        cazador[0] = cazador[0]-1

# Función que dibuja un cuadro en la posición inferior, elimina el cuadro en la posición antigua y acumula la posición
def abajo():
    if cazador[1]<9:
        grid[cazador[1]][cazador[0]]=0
        grid[cazador[1]+1][cazador[0]]=1
        cazador[1] = cazador[1]+1

# Función que dibuja un cuadro en la posición superior, elimina el cuadro en la posición antigua y acumula la posición
def arriba():
    if cazador[1]>0:
        grid[cazador[1]][cazador[0]]=0
        grid[cazador[1]-1][cazador[0]]=1
        cazador[1] = cazador[1]-1

# -------- Loop principal -----------
while not done:
    keys = pygame.key.get_pressed() #Almacenar información de tecla presionada
    for event in pygame.event.get():  # Se crea un evento cada vez que se presione alguna tecla o si se usa el mouse
        if event.type == pygame.QUIT:  # Cerrar el juego al concluir el ciclo
            done = True  # Se termina el ciclo al presionar el botón cerrar
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Conseguir la posición del mouse cuando se realiza un click
            pos = pygame.mouse.get_pos()
            # Las coordenadas son por pixeles, se realiza la conversión a coordenadas X Y
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            #Imprimir coordenadas de pixeles y ejes X Y al hacer click
            print("Click ", pos, "Coordenadas de tablero: ", row, column)

    #----- Controles de juego -----#
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
            
        # Al presionar la tecla espacio se inicia el movimiento automático del juego
        # Se crea una función para cada movimiento
            # Cada función se encarga de mover el cuadro en la dirección indicada
            # Se dibuja el nuevo cuadro por cada iteración
            # Se dibuja la cuadrícula por cada iteración
            # Se actualiza el frame en la pantalla
            # Se limita el contador de fps para hacer visible el movimiento del cazador en cada casilla
            
            
            #NOTA: esta parte aun no está terminada por lo que el código actual puede ser modificado 
            
            def derecha_fun():
                for derecha_automatico in range(9):
                    derecha()
                    dibujar()
                    dibujar_cuadricula(screen)
                    clock.tick(30)
                    pygame.display.update()                


            def abajo_fun():        
                for abajo_automatico in range(1):
                    abajo()
                    dibujar()
                    dibujar_cuadricula(screen)
                    clock.tick(30)
                    pygame.display.update()                

            
            def izquierda_fun():                
                for izquierda_automatico in range(9):
                    izquierda()
                    dibujar()
                    dibujar_cuadricula(screen)
                    clock.tick(30)
                    pygame.display.update()                


            def arriba_fun():
                for arriba_automatico in range(9):
                    arriba()
                    dibujar()
                    dibujar_cuadricula(screen)
                    clock.tick(30)
                    pygame.display.update()                


            derecha_fun()
            abajo_fun()
            izquierda_fun()
            abajo_fun()
            derecha_fun()
            abajo_fun()
            izquierda_fun()
            abajo_fun()
            derecha_fun()
            abajo_fun()
            izquierda_fun()
            abajo_fun()
            derecha_fun()
            abajo_fun()
            izquierda_fun()
            abajo_fun()
            derecha_fun()
            abajo_fun()
            izquierda_fun()
            arriba_fun()

            

    # Establer color de fondo de pantalla
    screen.fill(BLACK)
    # Dibujar cuadros según su color
    dibujar()
    # Dibujar cuadrícula del tablero
    dibujar_cuadricula(screen)
 
    # Limitar juego a 30 FPS por segundo
    clock.tick(30)
 
    # Actualizar la pantalla con los nuevos datos dibujados
    pygame.display.update()
 
pygame.quit()