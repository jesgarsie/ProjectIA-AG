import Grafo
import Vertice
import random
from deap import base, creator, tools, algorithms

# Inicializamos el Grafo
g = Grafo.Grafo()
path = "C:\\Users\\jesus\\Desktop\\grafo.txt"


# Generamos el grafo desde el fichero
def inicializacion(path):
    graph = Grafo.Grafo()
    with open(path, mode='r') as f:
        i = 0
        for line in f.readlines():
            if line.split()[0] == 'A':
                _, w1, w2 = line.split()
                if w1 != w2:
                    graph.agregarArista(int(w1), int(w2), 0)
            elif line.split()[0] == 'V':
                _, w = line.split()
                graph.agregarVertice(int(w), 1)
                i = i + 1

    return graph


g = inicializacion(path)

print(g.listaVertices)

creator.create('Fitness', base.Fitness, weights=(-1.0,))
creator.create('Individuo', list, fitness = creator.Fitness)


# Limitamos los colores a 3
caja_de_herramientas = base.Toolbox()
caja_de_herramientas.register('gen', random.randint, 0, 2)
caja_de_herramientas.register('individuo', tools.initRepeat,
                              container=creator.Individuo, func=caja_de_herramientas.gen, n=g.numVertices)


#  Semilla aleatoria
random.seed(random.randrange(1234556798))

# Creamos la lista de colores generada a partir de la semilla
colores = caja_de_herramientas.individuo()
print(colores)


# Agregamos los vértices, cada vértice un color de la lista
def generarGrafo(assignamenColors):
    # Inicializamos el Grafo
    gra = Grafo.Grafo()
    for i in range(g.numVertices):
        gra.agregarVertice(i, assignamenColors[i])
    for j in g.listaVertices:
        vecinos = g.obtenerVertice(j).obtenerConexiones()
        for h in vecinos:
            gra.agregarArista(j, h.id, 0)

    return gra



# Evaluamos que la lista de colores tenga al menos 3 colores
def comprobacionColores(colorss):
    C1 = []
    C2 = []
    C3 = []
    for i in range(colorss.__len__()):
        if colorss[i] == 0:
            C1.append(colorss[i])
        elif colorss[i] == 1:
            C2.append(colorss[i])
        else:
            C3.append(colorss[i])

    if ((C1.__len__() > 0) and (C2.__len__() > 0) and (C3.__len__() > 0)):
        # Mostramos la lista de colores
        print(colorss)
        return colorss
    else:
        colores2 = caja_de_herramientas.individuo()
        return comprobacionColores(colores2)


colors = comprobacionColores(colores)

g = generarGrafo(colors)


def fenotipo(grafo):
    C1 = []
    C2 = []
    C3 = []
    for i in range(grafo.numVertices):
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




caja_de_herramientas.register('mutate', tools.mutFlipBit, indpb=0.2)
# indpb es la probabilidad de mutación de cada gen del cromosoma
def ejecutarAlgoritmo(grafo):
    # Temperatura Inicial
    TEMP_0 = 10000
    print(caja_de_herramientas.mutate(colors))
    repeticiones = 0
    while TEMP_0 <=100 or repeticiones <= 1000:
        nuevosColores = caja_de_herramientas.mutate(colors)
        nuevosColores = comprobacionColores(nuevosColores)
        nuevoGrafo = generarGrafo(nuevosColores)
        if evaluar_individuo(nuevoGrafo) != 0:
            if caja_de_herramientas.evaluate(nuevoGrafo) < caja_de_herramientas.evaluate(grafo):
                TEMP_0 = TEMP_0 - (caja_de_herramientas.evaluate(grafo) - caja_de_herramientas.evaluate(nuevoGrafo))
                grafo = nuevoGrafo
                repeticiones = 0
                print(nuevosColores)
            else:
                repeticiones = repeticiones+1
        else:
            print(evaluar_individuo(nuevoGrafo))
            grafo = nuevoGrafo
            break
        print(evaluar_individuo(grafo))
    return grafo


ejecutarAlgoritmo(g)
