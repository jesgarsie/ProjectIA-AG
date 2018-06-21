import Grafo
import Vertice
import random
from deap import base, creator, tools, algorithms



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
def generarGrafo(assignamenColors):
    # Inicializamos el Grafo
    g = Grafo.Grafo()
    for i in range(6):
        g.agregarVertice(i, assignamenColors[i])


    # Agregamos las aristas que unen los vértices del grafo
    g.agregarArista(0, 1, 0)
    g.agregarArista(0, 5, 0)
    g.agregarArista(1, 2, 0)
    g.agregarArista(2, 3, 0)
    g.agregarArista(3, 4, 0)
    g.agregarArista(3, 5, 0)
    g.agregarArista(4, 0, 0)
    g.agregarArista(5, 2, 0)
    return g




caja_de_herramientas.register('mutate', tools.mutFlipBit, indpb=0.2)
# indpb es la probabilidad de mutación de cada gen del cromosoma
def ejecutarAlgoritmo(grafo):
    # Temperatura Inicial
    TEMP_0 = 10000
    print(caja_de_herramientas.mutate(colores))
    repeticiones = 0
    while TEMP_0 <=100 or repeticiones <= 30:
        nuevosColores = caja_de_herramientas.mutate(colores)
        nuevoGrafo = generarGrafo(nuevosColores[0])
        if evaluar_individuo(nuevoGrafo) == 0:
            print(evaluar_individuo(nuevoGrafo))
            grafo = nuevoGrafo
            return grafo
        else:
            if caja_de_herramientas.evaluate(nuevoGrafo) < caja_de_herramientas.evaluate(grafo):
                TEMP_0 = TEMP_0 - (caja_de_herramientas.evaluate(grafo) - caja_de_herramientas.evaluate(nuevoGrafo)) -10
                grafo = nuevoGrafo
                repeticiones = 0
            else:
                repeticiones = repeticiones+1
        print(evaluar_individuo(grafo))
    return grafo

ejecutarAlgoritmo(generarGrafo(colores))