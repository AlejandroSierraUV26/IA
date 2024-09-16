import numpy
"""
Este script se encarga de analizar el laberinto los posibles movimientos que se pueden realizar en el laberinto, apartir del punto donde se encuentra

"""

def leer_laberinto():
    with open("lab_matrix.txt", "r") as archivo:
        contenido = archivo.read()
        datos = contenido.split("\n")
        datos = [dato.split(" ") for dato in datos if dato]
        datos = [[int(dato) for dato in fila] for fila in datos]
    return datos
def comprobar_movimientos(laberinto):
    # Esta funcion indicara que elemntos se pueden mover
    # El elemento 0 es un espacio vacio
    # El elemento 1 es un obstaculo
    # El elemento 2 es donde inicia
    
    elementos = []
    
    inicio = buscar_inicio(laberinto)
    if inicio is None:
        return elementos

    x, y = inicio
    movimientos = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]  # arriba, abajo, izquierda, derecha

    for mov in movimientos:
        i, j = mov
        if 0 <= i < len(laberinto) and 0 <= j < len(laberinto[0]) and laberinto[i][j] == 0:
            elementos.append(mov)

    return elementos

    
    
    inicio = buscar_inicio(laberinto)
    
def buscar_inicio(laberinto):
    for i in range(len(laberinto)):
        for j in range(len(laberinto[i])):
            if laberinto[i][j] == 2:
                return (i, j)
    return None

def guardar_movimientos(movimientos):
    movimientos = comprobar_movimientos(leer_laberinto())
    with open("movimientos.txt", "w") as archivo:
        for mov in movimientos:
            archivo.write(f"{mov}\n")
    

print(numpy.array(leer_laberinto()))
guardar_movimientos(comprobar_movimientos(leer_laberinto()))
print(comprobar_movimientos(leer_laberinto()))
