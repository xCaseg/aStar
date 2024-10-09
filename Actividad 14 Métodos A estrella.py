#---------------------------------------LIBRERÍAS---------------------------------------#
import pygame
import sys
import tkinter.messagebox as tkMessageBox
import tkinter as tk

#------------------------------------INTERFAZ GRÁFICA------------------------------------#

#_______________________Ventana Principal________________________________# 

pygame.init()
ancho_ventana = 500
alto_ventana = 500

ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))
fuente = pygame.font.SysFont(None, 30)
Color = (255, 255, 255)

#_______________________Color de los nodos________________________________# 
    
colores = {
    "fondo": (255, 255, 255),
    "obstaculo": (24, 23, 28),
    "evaluado": (180, 180, 180),
    "camino": (50, 90, 140),
    "inicio": (0, 128, 0),
    "objetivo": (199, 29, 41)
}

def rgb_a_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

#________________________Texto en pantalla________________________________# 
    
def dibujar_texto(texto, pos_x, pos_y):
    texto_renderizado = fuente.render(texto, True, (0, 0, 0))
    ventana.blit(texto_renderizado, (pos_x, pos_y))

columnas = 10
filas = 10

ancho_nodo = ancho_ventana // columnas
alto_nodo = alto_ventana// filas

#_______________________Matrices_______________________________#
   
# Matrices
cuadricula = []
camino = []

#________________Booleanos de control de nodos_________________# 
    
class Lienzo:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.inicio = False
        self.obstaculo = False
        self.objetivo = False
        self.vecinos = []
        self.distancia_desde_inicio = float('inf')  # Distancia del nodo evaluado al origen
        self.distancia_al_objetivo = float('inf')  # Distancia heurística desde el nodo actual hasta el nodo objetivo
        self.costo_total = float('inf')  # Costo total del nodo actual al origen
        self.evaluado = False
        self.prioridad = None

#_______________________Números sobre nodos_______________________________#    

    def dibujar(self, ventana, color):
        pygame.draw.rect(ventana, color, (self.x * ancho_nodo, self.y * alto_nodo, ancho_nodo - 2, alto_nodo - 2))        
        if self.distancia_desde_inicio != float('inf'):
            texto_inicio = "{:.1f}".format(self.distancia_desde_inicio)
            texto_renderizado_inicio = fuente.render(texto_inicio, True, (0, 0, 0))
            ventana.blit(texto_renderizado_inicio, (self.x * ancho_nodo + 10, self.y * alto_nodo + 10))
        if self.distancia_al_objetivo != float('inf'):
            texto_heuristica = "{:.1f}".format(self.distancia_al_objetivo)
            texto_renderizado_heuristica = fuente.render(texto_heuristica, True, (0, 0, 0))
            ventana.blit(texto_renderizado_heuristica, (self.x * ancho_nodo + 10, self.y * alto_nodo + 30))
        if self.costo_total != float('inf'):
            texto_costo_total = str(int(self.costo_total))  # Convertir el costo total a entero
            texto_renderizado_costo_total = fuente.render(texto_costo_total, True, (0, 0, 0))
            ventana.blit(texto_renderizado_costo_total, (self.x * ancho_nodo + 10, self.y * alto_nodo + 50))

#------------------------------------LÓGICA DE NODOS VECINOS----------------------------------#
    def establecer_vecinos(self):
        if self.x > 0:
            self.vecinos.append(cuadricula[self.x - 1][self.y])
        if self.x < columnas - 1:
            self.vecinos.append(cuadricula[self.x + 1][self.y])
        if self.y > 0:
            self.vecinos.append(cuadricula[self.x][self.y - 1])
        if self.y < filas - 1:
            self.vecinos.append(cuadricula[self.x][self.y + 1])

        if self.x > 0 and self.y > 0:
            self.vecinos.append(cuadricula[self.x - 1][self.y - 1])
        if self.x > 0 and self.y < filas - 1:
            self.vecinos.append(cuadricula[self.x - 1][self.y + 1])
        if self.x < columnas - 1 and self.y > 0:
            self.vecinos.append(cuadricula[self.x + 1][self.y - 1])
        if self.x < columnas - 1 and self.y < filas - 1:
            self.vecinos.append(cuadricula[self.x + 1][self.y + 1])


for i in range(columnas):
    fila = []
    for j in range(filas):
        fila.append(Lienzo(i, j))
    cuadricula.append(fila)

for i in range(columnas):
    for j in range(filas):
        cuadricula[i][j].establecer_vecinos()

#----------------------------------VENTANA SECUNDARIA INFORMATIVA------------------------------------#

# Función para abrir la ventana secundaria
def abrir_ventana_secundaria(colores):
    ventana_secundaria = tk.Toplevel()
    ventana_principal_dimensiones = ventana.get_rect()

    pos_x_ventana_secundaria = ventana_principal_dimensiones.left  
    pos_y_ventana_secundaria = ventana_principal_dimensiones.centery  

    ventana_secundaria.geometry(f"+{pos_x_ventana_secundaria + 80}+{pos_y_ventana_secundaria}")
    ventana_secundaria.overrideredirect(True)

    lienzo = tk.Canvas(ventana_secundaria, width= ancho_ventana //2 + 20, height=alto_ventana //2 +10)
    lienzo.pack()

    x = 20  
    y = 60  
    ancho = ancho_nodo /2 
    alto = alto_nodo /2 

    espacio = lienzo.create_rectangle(x, y, x + ancho, y + alto, fill=rgb_a_hex(colores["fondo"]))  
    lienzo.create_rectangle(x, y + alto, x + ancho, y + 2 * alto, fill=rgb_a_hex(colores["inicio"]))  
    lienzo.create_rectangle(x, y + 2 * alto, x + ancho, y + 3 * alto, fill=rgb_a_hex(colores["objetivo"]))  
    lienzo.create_rectangle(x, y + 3 * alto, x + ancho, y + 4 * alto, fill=rgb_a_hex(colores["obstaculo"]))  
    lienzo.create_rectangle(x, y + 4 * alto, x + ancho, y + 5 * alto, fill=rgb_a_hex(colores["evaluado"]))  
    lienzo.create_rectangle(x, y + 5 * alto, x + ancho, y + 6 * alto, fill=rgb_a_hex(colores["camino"]))  

    lienzo.create_text(120, 20, anchor=tk.CENTER, text="Nodos por color", font=("Arial", 16, "bold"))  
    lienzo.create_text(80, y + 1.5 * alto, anchor=tk.W, text="inicio", font=("Arial", 12, "bold"))  
    lienzo.create_text(80, y + 2.5 * alto, anchor=tk.W, text="objetivo", font=("Arial", 12, "bold"))  
    lienzo.create_text(80, y + 3.5 * alto, anchor=tk.W, text="obstaculo", font=("Arial", 12, "bold"))  
    lienzo.create_text(80, y + 4.5 * alto, anchor=tk.W, text="evaluado", font=("Arial", 12, "bold")) 
    lienzo.create_text(80, y + 5.5 * alto, anchor=tk.W, text="camino", font=("Arial", 12, "bold"))
    lienzo.create_text(x, y + 6.5 * alto, anchor=tk.W, text="[#]", font=("Arial", 12, "bold")) 
    lienzo.create_text(80, y + 6.5 * alto, anchor=tk.W, text="[Distancia heuristica]", font=("Arial", 12, "bold")) 
    lienzo.create_text(x, y + 7.5 * alto, anchor=tk.W, text="[#]", font=("Arial", 12, "bold"))  
    lienzo.create_text(80, y + 7.5 * alto, anchor=tk.W, text="[Costo total]", font=("Arial", 12, "bold"))  

    lienzo.itemconfig(espacio, state="hidden")

#-------------------------------------------VALOR HEURISTICO-------------------------------------------#

import math

def calcular_valor_h(fila, columna, destino):
    # Calcular la diferencia en cada dimensión
    diferencia_x = fila - destino[0]
    diferencia_y = columna - destino[1]
    # Calcular la distancia euclidiana utilizando la fórmula
    distancia_euclidiana = math.sqrt(diferencia_x ** 2 + diferencia_y ** 2)
    return distancia_euclidiana
 # Se calcula con la distancia de Euclidiana ya que la de Manhatan d = |x2 - x1| + |y2 -y1| No tiene en cuenta las diagonales como la euclidiana

def mostrar_mensaje(titulo, mensaje):
    ventana = tk.Tk()
    ventana.withdraw()
    tkMessageBox.showinfo(titulo, mensaje)

#----------------------------------------------MÉTODO A* -----------------------------------------------#

def a_estrella(nodo_inicio, nodo_objetivo):
    abiertos = []  # Lista de nodos abiertos que aún no han sido evaluados
    cerrados = []  # Lista de nodos que ya han sido evaluados y cerrados

    abiertos.append(nodo_inicio)  # Agregar el nodo inicial a la lista de abiertos

    while abiertos:  # Mientras haya nodos abiertos por evaluar
        # Ordenar los nodos abiertos por su costo total (suma de distancia desde inicio y distancia al objetivo)
        abiertos.sort(key=lambda nodo: nodo.distancia_desde_inicio + nodo.distancia_al_objetivo)
        nodo_actual = abiertos.pop(0)  # Tomar el nodo con menor costo total como el nodo actual

        if nodo_actual == nodo_objetivo:  # Si el nodo actual es el objetivo
            abrir_ventana_secundaria(colores)  # Mostrar ventana informativa
            distancia_recorrida = nodo_actual.distancia_desde_inicio  # Obtener la distancia recorrida
            # Mostrar mensaje con la distancia recorrida
            mostrar_mensaje("Distancia Recorrida", f"La distancia recorrida es de {distancia_recorrida:.2f} unidades")
            # Reconstruir el camino desde el nodo objetivo hasta el nodo inicial
            while nodo_actual.prioridad:
                camino.append(nodo_actual)
                nodo_actual = nodo_actual.prioridad
            camino.append(nodo_inicio)  # Agregar el nodo inicial al camino
            break  # Salir del bucle

        cerrados.append(nodo_actual)  # Agregar el nodo actual a la lista de nodos cerrados

        # Iterar sobre los vecinos del nodo actual
        for vecino in nodo_actual.vecinos:
            if not vecino.obstaculo and vecino not in cerrados:  # Si el vecino no es un obstáculo ni ha sido evaluado
                vecino.evaluado = True  # Marcar el vecino como evaluado
                # Calcular el costo de movimiento entre nodos
                if vecino.x != nodo_actual.x and vecino.y != nodo_actual.y:
                    nuevo_costo = nodo_actual.distancia_desde_inicio + 1.4  # Costo diagonal (teorema de Pitágoras)
                else:
                    nuevo_costo = nodo_actual.distancia_desde_inicio + 1  # Costo horizontal o vertical
                if nuevo_costo < vecino.distancia_desde_inicio:  # Si el nuevo costo es menor al costo actual del vecino
                    vecino.distancia_desde_inicio = nuevo_costo  # Actualizar el costo desde el inicio del vecino
                    # Calcular la distancia heurística desde el vecino hasta el objetivo
                    vecino.distancia_al_objetivo = calcular_valor_h(vecino.x, vecino.y, (nodo_objetivo.x, nodo_objetivo.y))
                    # Calcular el costo total del vecino (suma de costo desde inicio y distancia al objetivo)
                    vecino.costo_total = vecino.distancia_desde_inicio + vecino.distancia_al_objetivo
                    vecino.prioridad = nodo_actual  # Establecer al nodo actual como prioridad del vecino
                    if vecino not in abiertos:  # Si el vecino no está en la lista de abiertos
                        abiertos.append(vecino)  # Agregar el vecino a la lista de abiertos


#--------------------------------------------BUCLE PRINCIPAL---------------------------------------------#

def main():
    pygame.display.set_caption("Algoritmo de búsqueda de caminos con A*")
    mostrar_mensaje("Instrucciones", "Haz clic izquierdo para establecer el nodo de inicio.\nHaz clic derecho para establecer el nodo objetivo.\nHaz clic izquierdo y arrastra para colocar obstáculos.\nPresiona cualquier tecla para iniciar la búsqueda.")

    objetivo_establecido = False  # Se ha establecido el nodo objetivo.
    inicio_establecido = False    # Se ha establecido el nodo de inicio.
        
    nodo_inicio = None           # Almacena el nodo de inicio seleccionado por el usuario.
    nodo_objetivo = None         # Almacena el nodo objetivo seleccionado por el usuario.

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    # Botón izquierdo del ratón
                    x, y = pygame.mouse.get_pos()
                    i = x // ancho_nodo
                    j = y // alto_nodo
                    if not inicio_establecido and not cuadricula[i][j].obstaculo:
                        # Si no se ha establecido el nodo de inicio y la celda no es un obstáculo
                        cuadricula[i][j].inicio = True
                        inicio_establecido = True
                        nodo_inicio = cuadricula[i][j]
                        nodo_inicio.distancia_desde_inicio = 0
                elif event.button == 3:  
                    # Botón derecho del ratón
                    x, y = pygame.mouse.get_pos()
                    i = x // ancho_nodo
                    j = y // alto_nodo
                    if not objetivo_establecido and not cuadricula[i][j].obstaculo and not cuadricula[i][j].inicio:  
                        # Si no se ha establecido el nodo objetivo y la celda no es un obstáculo ni el nodo de inicio
                        cuadricula[i][j].objetivo = True
                        objetivo_establecido = True
                        nodo_objetivo = cuadricula[i][j]           

            elif event.type == pygame.MOUSEMOTION:                 
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                if event.buttons[0]:
                    # Arrastrar click izquierdo del ratón
                    i = x // ancho_nodo
                    j = y // alto_nodo
                    if not cuadricula[i][j].inicio:  
                        # Si la celda no es el nodo de inicio
                        cuadricula[i][j].obstaculo = True
                if event.buttons[2] and not objetivo_establecido:
                    # Si se mantiene presionado el botón derecho del ratón y no se ha establecido el nodo objetivo
                    i = x // ancho_nodo
                    j = y // alto_nodo
                    cuadricula[i][j].objetivo = True
                    objetivo_establecido = True
                    nodo_objetivo = cuadricula[i][j]
        
            elif event.type == pygame.KEYDOWN:
                # Presionar tecla
                if inicio_establecido and objetivo_establecido:
                    # Si tanto el nodo de inicio como el objetivo están establecidos
                    a_estrella(nodo_inicio, nodo_objetivo)
                    if not camino:
                        # Si no hay camino posible
                        mostrar_mensaje("Error", "No hay caminos posibles debido a los obstáculos en el camino.")                    
                elif not (inicio_establecido and objetivo_establecido):          
                    # Si no se han establecido tanto el nodo de inicio como el objetivo
                    mostrar_mensaje("Error", "Debes establecer un nodo de inicio y un nodo objetivo antes de iniciar la búsqueda.")

        ventana.fill((234, 235, 237)) 
        
        for i in range(columnas):
            for j in range(filas):
                lienzo = cuadricula[i][j]
                color = colores["fondo"]
                if lienzo.obstaculo:
                    color = colores["obstaculo"]
                if lienzo.evaluado:  
                    color = colores["evaluado"]
                if lienzo in camino:
                    color = colores["camino"]
                if lienzo.inicio:
                    color = colores["inicio"]
                if lienzo.objetivo:
                    color = colores["objetivo"]

                lienzo.dibujar(ventana, color)

        pygame.display.flip()

if __name__ == "__main__":
    main()
