
from networkx import nx

mapa = nx.Graph()

#   ------------------------------------------ CLASSE PARA CRIACAO DE ARESTA
class Aresta:

    def __init__(self, origem, destino, custo):
        self._origem = origem
        self._destino = destino
        self._custo = custo
        self._feromonio = 0.1

    def getOrigem(self):
        return self._origem

    def getDestino(self):
        return self._destino

    def getCusto(self):
        return self._custo

    def getFeromonio(self):
        return self._feromonio

    def setFeromonio(self, feromonio):
        self._feromonio = feromonio

#   ------------------------------------------ CLASSE PARA CRIACAO DE GRAFO
class Grafo:

    def __init__(self):
        self._aresta = {}
        self._vizinho = {}
        self._grafo = {}

    def setAddAresta(self, origem, destino, custo):
        aresta = Aresta(origem=origem, destino=destino, custo=custo)
        self._aresta[(origem, destino)] = aresta
        self._grafo[(aresta.getOrigem(), aresta.getDestino())] = [aresta.getCusto()]

        if origem not in self._vizinho:
            self._vizinho[origem] = [destino]
        else:
            self._vizinho[origem].append(destino)

    def nArestas(self):
        return len(self._aresta)

    def nVertices(self):
        return len(self._vizinho)

    def getAresta(self):
        return self._aresta

    def getVizinho(self, origem):
        return self._vizinho[origem]

    def getCustoAresta(self, origem, destino):
        return self._aresta[(origem, destino)].getCusto()

    def getFeromonioAresta(self, origem, destino):
        return self._aresta[(origem, destino)].getFeromonio()

    def setFeromonioAresta(self, origem, destino, feromonio):
        self._aresta[(origem, destino)].setFeromonio(feromonio)
