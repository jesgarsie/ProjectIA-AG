import Grafo
import Vertice
import random
from deap import base, creator, tools, algorithms


g = Grafo.Grafo()

creator.create('Fitness', base.Fitness, weights=(-1.0,))
creator.create('Individuo', list, fitness = creator.Fitness)

caja_de_herramientas = base.Toolbox()
caja_de_herramientas.register('gen', random.randint, 0, 2)
caja_de_herramientas.register('individuo', tools.initRepeat,
                              container=creator.Individuo, func=caja_de_herramientas.gen, n=6)

random.seed(12345)  # Semilla para el mecanismo de generación de números aleatorios

print(caja_de_herramientas.individuo())

for i in range(6):
    g.agregarVertice(i, caja_de_herramientas.individuo)

print(g.listaVertices)

g.agregarArista(0, 1, 5)
g.agregarArista(0, 5, 2)
g.agregarArista(1, 2, 4)
g.agregarArista(2, 3, 9)
g.agregarArista(3, 4, 7)
g.agregarArista(3, 5, 3)
g.agregarArista(4, 0, 1)
g.agregarArista(5, 4, 8)
g.agregarArista(5, 2, 1)
for v in g:
    for w in v.obtenerConexiones():
        print("( %s , %s )" % (v.obtenerId(), w.obtenerId()))
