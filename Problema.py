import Grafo
import Vertice
import random
from deap import base, creator, tools, algorithms

# Inicializamos el Grafo
g = Grafo.Grafo()

creator.create('Fitness', base.Fitness, weights=(-1.0,))
creator.create('Individuo', list, fitness = creator.Fitness)

# Limitamos los colores a 3
caja_de_herramientas = base.Toolbox()
caja_de_herramientas.register('gen', random.randint, 0, 2)
caja_de_herramientas.register('individuo', tools.initRepeat,
                              container=creator.Individuo, func=caja_de_herramientas.gen, n=6)

# Semilla para el mecanismo de generación de números aleatorios
random.seed(random.randrange(1234556798))

# Creamos la lista de colores aleatoria
colores = caja_de_herramientas.individuo()

# Mostramos la lista de colores
print(colores)

def fenotipo(grafo):
    C1 = []
    C2 = []
    C3 = []
    for i in range(6):
        if grafo.obtenerVertice(i).color == 0:
            C1.append(grafo.obtenerVertice(i))
        elif grafo.obtenerVertice(i).color == 1:
            C2.append(grafo.obtenerVertice(i))
        else:
            C3.append(grafo.obtenerVertice(i))
    return (C1, C2, C3)

def evaluar_individuo(grafo):
    C1, C2, C3 = fenotipo(grafo)
    res = 0

    for i in C1:
        vecinos = list(i.obtenerConexiones())
        for j in vecinos:
            if C1.__contains__(j):
                res = res + 50

    for k in C2:
        vecinos = list(k.obtenerConexiones())
        for l in vecinos:
            if C2.__contains__(l):
                res = res + 50

    for n in C3:
        vecinos = list(n.obtenerConexiones())
        for m in vecinos:
            if C3.__contains__(m):
                res = res + 50
    return res

caja_de_herramientas.register('evaluate', evaluar_individuo)
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


print(caja_de_herramientas.evaluate(g))