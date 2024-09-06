# Realizar un menu de opciones para seleccionar el tipo de árbol a visualizar y sus parámetros
import generar_arbol as ga
import pygame
print("""
        1. Busqueda por amplitud
        2. Busqueda por Costo Uniforme
        3. Busqueda por preferente por amplitud
        4. Busqueda por Limitada por Profundidad
        5. Busqueda profunidad iterativa
        6. Busqueda Avara
        !(1,6). Salir
    """)    

opcion = int(input("Seleccione una opcion: "))
if opcion == 1:
    ga.busqueda_amplitud() # Sin implementar
elif opcion == 2:
    ga.busqueda_costo_uniforme() # Sin implementar    
elif opcion == 3:
    ga.busqueda_preferente_amplitud() # Sin implementar   
elif opcion == 4:
    ga.busqueda_limitada_profundidad() # Sin implementar  
elif opcion == 5:
    ga.busqueda_profundidad_iterativa() # Sin implementar 
elif opcion == 6:
    ga.busqueda_avara() # Sin implementar    
else:
    exit()

    
    
    
    
        