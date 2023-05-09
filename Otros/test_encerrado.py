import numpy as np
import heapq
# Crear un array de 10x10 con ceros
grid = np.zeros((10, 10))

# Asignar valores a las posiciones requeridas
grid[0, 0] = 1
grid[9, 9] = 4
grid[9, 8] = 2
grid[7, 7] = 2
grid[8, 9] = 3

# Imprimir el array resultante
print(grid)

def moves(row, col):
    valid_moves = []
    if row > 0:
        valid_moves.append('up')
    if row < 9:
        valid_moves.append('down')
    if col > 0:
        valid_moves.append('left')
    if col < 9:
        valid_moves.append('right')
    return valid_moves


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
final = (9,9)

path = astar(inicio, final, grid)
if path is None:
    print("No hay camino hacia el objetivo.")
else:
    print("El camino más corto hacia el objetivo es:", path)

