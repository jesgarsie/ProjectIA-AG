import Grafo
import Vertice
import random
from deap import base, creator, tools, algorithms


class Problema:

    def __init__(self, path, repeticionesPorConsola):
        self.repeticionesDeEntrada = repeticionesPorConsola
        self.path = path

        # Inicializamos el Grafo
        self.g = self.inicializacion()

        self.creator = creator.create('Fitness', base.Fitness, weights=(-1.0,))
        self.create = creator.create('Individuo', list, fitness=creator.Fitness)

        # Limitamos los colores a 3
        self.caja_de_herramientas = base.Toolbox()
        self.gen = self.caja_de_herramientas.register('gen', random.randint, 0, 2)
        self.individuo = self.caja_de_herramientas.register('individuo', tools.initRepeat,container=creator.Individuo, func=self.caja_de_herramientas.gen, n=self.g.numVertices)

        #  Semilla aleatoria
        random.seed(random.randrange(987654321))

        # Creamos la lista de colores generada a partir de la semilla
        self.colores = self.caja_de_herramientas.individuo()
        print(self.colores)
        self.colors = self.comprobacionColores()

        self.g = self.generarGrafo(self.colors)

        self.evaluar = self.caja_de_herramientas.register('evaluate', self.evaluar_individuo)

        self.mutar = self.caja_de_herramientas.register('mutate', tools.mutFlipBit, indpb=0.25)



    # Generamos el grafo desde el fichero
    def inicializacion(self):
        graph = Grafo.Grafo()
        with open(self.path, mode='r') as f:
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





    # Agregamos los vértices, cada vértice un color de la lista
    def generarGrafo(self, colores):
        # Inicializamos el Grafo
        gra = Grafo.Grafo()
        for i in range(self.g.numVertices):
            gra.agregarVertice(i, colores[i])
        for j in self.g.listaVertices:
            vecinos = self.g.obtenerVertice(j).obtenerConexiones()
            for h in vecinos:
                gra.agregarArista(j, h.id, 0)

        return gra



    # Evaluamos que la lista de colores tenga al menos 3 colores
    def comprobacionColores(self):
        C1 = []
        C2 = []
        C3 = []
        for i in range(self.colores.__len__()):
            if self.colores[i] == 0:
                C1.append(self.colores[i])
            elif self.colores[i] == 1:
                C2.append(self.colores[i])
            else:
                C3.append(self.colores[i])

        if ((C1.__len__() > 0) and (C2.__len__() > 0) and (C3.__len__() > 0)):
            # Mostramos la lista de colores
            print(self.colores)
            return self.colores
        else:
            self.colores = self.caja_de_herramientas.individuo()
            return self.comprobacionColores()



    def fenotipo(self, grafo):
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

    def evaluar_individuo(self, grafoIn):
        C1 = []
        C2 = []
        C3 = []
        for i in range(grafoIn.numVertices):
            if grafoIn.obtenerVertice(i).color == 0:
                C1.append(grafoIn.obtenerVertice(i))
            elif grafoIn.obtenerVertice(i).color == 1:
                C2.append(grafoIn.obtenerVertice(i))
            else:
                C3.append(grafoIn.obtenerVertice(i))
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

    # indpb es la probabilidad de mutación de cada gen del cromosoma
    def ejecutarAlgoritmo(self):
        # Temperatura Inicial
        grafo = self.g
        TEMP_0 = 10000
        repeticiones = 0
        nuevosColores = self.caja_de_herramientas.mutate(self.colors)
        while TEMP_0 >=100 and repeticiones <= self.repeticionesDeEntrada:
            nuevosColores0 = nuevosColores
            nuevosColores = self.caja_de_herramientas.mutate(nuevosColores0)
            nuevosColores = self.comprobacionColores()
            nuevoGrafo = self.generarGrafo(nuevosColores)
            grafoFitness = self.evaluar_individuo(grafo)
            nuevoGrafoFitness0 = self.evaluar_individuo(nuevoGrafo)
            if grafoFitness != 0 and nuevoGrafoFitness0 !=0:
                nuevoGrafoFitness = self.caja_de_herramientas.evaluate(nuevoGrafo)
                grafoOri = self.caja_de_herramientas.evaluate(grafo)
                if  nuevoGrafoFitness < grafoOri:
                    TEMP_0 = TEMP_0 - (self.caja_de_herramientas.evaluate(grafo) - self.caja_de_herramientas.evaluate(nuevoGrafo))
                    grafo = nuevoGrafo
                    repeticiones = 0
                    print(nuevosColores)
                    print("Temperatura")
                    print(TEMP_0)
                else:
                    print(nuevoGrafoFitness)
                    print(grafoOri)
                    repeticiones = repeticiones+1
            else:
                if grafoFitness == 0:
                    break
                elif nuevoGrafoFitness0 ==0:
                    grafo = nuevoGrafo
                    break
        print("Fitness")
        print(self.evaluar_individuo(grafo))
        print("Temperatura:")
        print(TEMP_0)
        return nuevosColores
