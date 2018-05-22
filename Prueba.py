import Grafo
import Vertice
import random
from deap import base, creator, tools, algorithms

# Inicializamos el Grafo
g = Grafo.Grafo()

creator.create('Fitness', base.Fitness, weights=(-1.0,))
creator.create('Individuo', list, fitness = creator.Fitness)

caja_de_herramientas = base.Toolbox()
caja_de_herramientas.register('gen', random.randint, 0, 2)
caja_de_herramientas.register('individuo', tools.initRepeat,
                              container=creator.Individuo, func=caja_de_herramientas.gen, n=6)

random.seed(12345)  # Semilla para el mecanismo de generación de números aleatorios

#Mostramos por pantalla la lista de colores
print(caja_de_herramientas.individuo())

# Creamos la lista de colores aleatoria
colores = caja_de_herramientas.individuo()

#Agregamos los vértices, cada vértice un color de la lista
for i in range(6):
    g.agregarVertice(i, colores[i])

#Mostramos por pantalla cada vértice y su color
for j in g:
    print("(Vertice: %s, Color: %s)" % (j.obtenerId(), j.obtenerColor()))

# Agregamos las aristas que unen los vértices del grafo
g.agregarArista(0, 1, 0)
g.agregarArista(0, 5, 0)
g.agregarArista(1, 2, 0)
g.agregarArista(2, 3, 0)
g.agregarArista(3, 4, 0)
g.agregarArista(3, 5, 0)
g.agregarArista(4, 0, 0)
g.agregarArista(5, 4, 0)
g.agregarArista(5, 2, 0)

#Mostramos por pantalla las adyacencias de los vértices
for v in g:
    for w in v.obtenerConexiones():
        print("( %s , %s )" % (v.obtenerId(), w.obtenerId()))
