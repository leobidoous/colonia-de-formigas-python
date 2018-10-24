# coding: utf-8

# authors: Leonardo Emilly Dias Santos Bidó e Wemerson Rodrigues da Silva

# Este algoritmo visa encontrar a menor rota
# entre um vértice X até um vértice Y, passando
# pelas arestas com o menor custo, sem repeti-las.

# REFERENCIA: "https://www.youtube.com/watch?v=UXSc0jwgZis"

# O ALGORITMO TÊM UMA PARTE RECURSSIVA DEVIDO A QUANTIDADE DE VEZES NECESSÁRIAS
# PARA ENCONTRAR AS PROBABILIDADES DE ESCOLHA DE ALGUMA DETERMINADA ROTA, POR
# ISSO, QUANDO O DESTINO É BASTANTE LONGE DA ORIGEM, DEVE-SE EVITAR UTILIZAR
# MUITAS FORMIGAS E MUITAS ITERAÇÕES PARA ENCONTRAR O CAMINHO ÓTIMO. OUTRA
# SOLUÇÃO É AUMENTAR O LIMITE DE RECURSIVIDADE SUPORTADO PELA LINGUAGEM ADOTADA
# UMA VEZ QUE O PYTHON LIMITA ESSA EXECUÇÃO POR DEFAULT.
# SENDO ASSIM, BASTA UTILIZAR A FUNÇÃO sys.setrecursionlimit()
# LEIA MAIS SOBRE ESSA FUNÇÃO ANTES DE UTILIZÁ-LA

import classe
import acs
import dates

# ADICIONAR AS ARESTAS COM SEUS PESOS
# TODOS OS PESOS DAS ARESTAS SAO AS KILOMETRAGENS POR RODOVIA DA ORIGEM AO DESTINO
# DADOS OBTIDOS ATRAVES DO GOOGLE MAPS

import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout


class TelaPrincipal(FloatLayout):

    def on_press_btn1(self):
        origem = self.ids.origem.text
        destino = self.ids.destino.text
        coef_evaporacao = float(self.ids.coef_evaporacao.text)
        n_iteracoes = int(self.ids.n_iteracoes.text)
        vel_execucao = int(self.ids.vel_execucao.text)
        n_formigas = int(self.ids.n_formigas.text)

        grafo = classe.Grafo()
        mapa = dates.mapa

        # Ler do arquivo e montar o grafo
        lista = []
        file = open('arquivo.txt', 'r')
        for line in file:
            line = line.rstrip()
            aux = ''
            for i in line:
                if i != ',':
                    aux = aux + i
                else:
                    lista.append(aux)
                    aux = ''
            lista.append(aux)
            grafo.setAddAresta(lista[0], lista[1], float(lista[2]))
            lista = []
        file.close()

        list_vertice = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF',
                        'ES', 'GO', 'MA', 'MG', 'MT', 'MS', 'PA',
                        'PE', 'PB', 'PI', 'PR', 'RN', 'RO', 'RR',
                        'RS', 'RJ', 'SC', 'SE', 'SP', 'TO']

        acs.sistemaColoniaFormiga(grafo, mapa, origem, destino, list_vertice, coef_evaporacao, n_iteracoes, vel_execucao, n_formigas)


class Init(App):
    def build(self):
        self.title = 'Ant Colony Simulator'
        return TelaPrincipal()

window = Init()

window.run()
