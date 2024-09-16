import numpy 
import networkx as nx
import matplotlib.pyplot as plt


# Crear un arbol

arbol = nx.Graph()

# Agregar nodos al arbol
arbol.add_node(1)
arbol.add_node(2)
arbol.add_node(3)

# Agregar aristas al arbol
arbol.add_edge(1, 2)
arbol.add_edge(1, 3)

# Mostrar los nodos del arbol
print(arbol.nodes())

# Mostrar las aristas del arbol
print(arbol.edges())

# Mostrar el arbol
plt.figure()
nx.draw(arbol, with_labels=True)

plt.show()

