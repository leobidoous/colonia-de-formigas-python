import numpy
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.animation as gif
from networkx import nx

# ----------------------------------------------------- DEFINIR A INVERSA DA DISTANCIA DO VERTICE X ATE Y ( Txy )
def inversaDistancia(grafo, origem):

    inversa_distancia = {}
    list_vizinhos = grafo.getVizinho(origem)
    for i in range(len(list_vizinhos)):
        inversa_distancia[(origem, list_vizinhos[i])] = 1 / grafo.getCustoAresta(origem, list_vizinhos[i])
    return inversa_distancia


# ------------------------------------------ DETERMINAR A PROBABILIDADE DE ESCOLHA PARA CADA VERTICE ADJACENTE ( Pxy = (Txy * Nxy) / (somatorio (Txy * Nxy) todos os vertices)
# Txy -> inversa da distancia , Nxy -> feromonio na aresta
def probabilidaAresta(grafo, origem):

    probabilidade_aresta = {}
    inversa_distancia = inversaDistancia(grafo, origem)
    list_vizinhos = grafo.getVizinho(origem)

    somatorio_TxyNxy = 0
    for i in range(len(list_vizinhos)):
        somatorio_TxyNxy += inversa_distancia[(origem, list_vizinhos[i])] * grafo.getFeromonioAresta(origem, list_vizinhos[i])

    for i in range(len(list_vizinhos)):
        probabilidade_aresta[(origem, list_vizinhos[i])] = (inversa_distancia[(origem, list_vizinhos[i])] * grafo.getFeromonioAresta(origem, list_vizinhos[i])) / somatorio_TxyNxy
    return probabilidade_aresta


# ----------------------------------------------------- DEFINIR PROXIMO DESTINO COM BASE NA PROBABILIDADE DE CADA ARESTA
def proximoVertice(grafo, origem):

    dict_probabilidade_aresta = probabilidaAresta(grafo, origem)

    vizinhos_origem = grafo.getVizinho(origem)
    list_probabilidade = []
    checar_destino = []
    for j in range(len(vizinhos_origem)):
        list_probabilidade.append(dict_probabilidade_aresta[(origem, vizinhos_origem[j])])
    checar_destino.append(numpy.random.choice(a=vizinhos_origem, p=list_probabilidade))
    return checar_destino[0]



# ----------------------------------------------------- DEFINIR O CAMINHO PERCORRIDO PELA FORMIGA
def caminho(grafo, origem, destino, lista_caminho):

    lista_caminho.append(origem)
    if origem != destino:
        proximo_vertice = proximoVertice(grafo, origem)
        caminho(grafo, proximo_vertice, destino, lista_caminho)



# ----------------------------------------------------- REMOVE CICLOS GERADOS NO PERCURSO
def removeCiclo(lista_caminho):

    aux = 0
    for i in range(len(lista_caminho)):

        for j in range((i+1),len(lista_caminho)):
            if lista_caminho[i] == lista_caminho[j]:
                aux = j
        if aux != 0:
            del lista_caminho[i:aux]
            aux = 0

# ----------------------------------------------------- ATUALIZA O FEROMÔNIO APÓS A EVAPORAÇÃO
def atualizarTaxaEvaporacao(grafo, lista_vertice, coeficiente_evaporacao):

    lista_visitado = []
    for k in range(len(lista_vertice)):
        list_vizinhos = grafo.getVizinho(lista_vertice[k])
        for i in range(len(list_vizinhos)):
            if list_vizinhos[i] not in lista_visitado:
                tx_evaporacao = (1 - coeficiente_evaporacao) * grafo.getFeromonioAresta(lista_vertice[k], list_vizinhos[i])
                grafo.setFeromonioAresta(lista_vertice[k], list_vizinhos[i], tx_evaporacao)
                grafo.setFeromonioAresta(list_vizinhos[i], lista_vertice[k], tx_evaporacao) #grafo não é bidirecional

        lista_visitado.append(lista_vertice[k])


# ----------------------------------------------------- ATUALIZA O FEROMÔNIO DEIXADO PELA FORMIGA NA ROTA
def atualizaTaxaFeromonio(grafo, lista_caminho, coeficiente_evaporacao, lista_vertice):

    atualizarTaxaEvaporacao(grafo, lista_vertice, coeficiente_evaporacao)

    #CALCULA A DISTANCIA TOTAL PERCORRIDA POR CADA FORMIGA
    distanciaTotal = []
    for i in range(len(lista_caminho)):
        caminhoFormiga = lista_caminho[i]
        somatorio = 0
        for j in range(len(caminhoFormiga)-1):
            somatorio += grafo.getCustoAresta(caminhoFormiga[j],caminhoFormiga[j+1])
        distanciaTotal.append(somatorio)

    # ATUALIZA O FEROMÔNIO NA ROTA DEIXADO POR CADA FORMIGA
    for i in range(len(lista_caminho)):
        caminhoFormiga = lista_caminho[i]
        for j in range(len(caminhoFormiga) - 1):
            somatorio = 100 / distanciaTotal[i] + grafo.getFeromonioAresta(caminhoFormiga[j], caminhoFormiga[j + 1])
            grafo.setFeromonioAresta(caminhoFormiga[j], caminhoFormiga[j + 1], somatorio)
            grafo.setFeromonioAresta(caminhoFormiga[j + 1], caminhoFormiga[j], somatorio) #grafo não é bidirecional

    return distanciaTotal


def sistemaColoniaFormiga(grafo, mapa, origem, destino, lista_vertice, coeficiente_evaporacao, iteracao, vel_iteracao, formiga):

    rota_total = [('AP', 'PA'), ('AC', 'RO'), ('RO', 'AM'), ('AM', 'AC'), ('RR', 'AM'), ('RR', 'PA'),
                  ('PA', 'AM'), ('PA', 'TO'), ('RS', 'SC'), ('SC', 'PR'), ('PR', 'MS'), ('PR', 'SP'),
                  ('SP', 'RJ'), ('RJ', 'MG'), ('MG', 'SP'), ('MS', 'MT'), ('MT', 'RO'), ('MT', 'PA'),
                  ('MT', 'GO'), ('GO', 'DF'), ('DF', 'MG'), ('MG', 'GO'), ('GO', 'BA'), ('BA', 'TO'),
                  ('TO', 'GO'), ('TO', 'MA'), ('MA', 'PI'), ('PI', 'TO'), ('BA', 'MG'), ('BA', 'ES'),
                  ('BA', 'SE'), ('SE', 'AL'), ('AL', 'PE'), ('PE', 'PI'), ('PE', 'PB'), ('PI', 'CE'),
                  ('CE', 'RN'), ('RN', 'PB'), ('PB', 'CE'), ('PB', 'PE'), ('PA', 'MA'), ('PI', 'BA'),
                  ('MG', 'MS'), ('MS', 'GO'), ('MS', 'SP'), ('MG', 'ES'), ('RJ', 'ES')]

    pos = {'AC': (53.71, 229.51), 'AL': (579.10, 233.28), 'AM': (133.96, 158.04), 'AP': (340.86, 60.23),
           'BA': (505.12, 274.66), 'CE': (531.45, 160.55), 'DF': (387.83, 351.83), 'ES': (513.90, 390.02),
           'GO': (382.24, 306.00), 'MA': (444.93, 161.80), 'MG': (453.71, 369.95), 'MT': (281.92, 283.47),
           'MS': (293.21, 392.52), 'PA': (314.53, 163.06), 'PE': (551.52, 208.20), 'PB': (587.88, 198.17),
           'PI': (488.82, 200.67), 'PR': (342.11, 467.76), 'RN': (577.85, 168.07), 'RO': (174.09, 262.12),
           'RR': (194.15, 53.97), 'RS': (315.78, 544.25), 'RJ': (473.77, 437.66), 'SC': (374.71, 512.90),
           'SE': (567.82, 249.58), 'SP': (383.49, 423.87), 'TO': (397.29, 237.04)}

    lista_formigas = []
    for i in range(formiga):
        lista_formigas.append(str(i+1))

    im = Image.open('back.png')

    fig1 = plt.figure()
    fig1.set_facecolor('#CCCCCC')

    # ax3 = fig1.add_subplot(2,2,2) # plot do gráfico1
    # ax3.set_title('Gráfico 2 das Formigas')
    # ax3.set_facecolor('#CCCCCC')
    # ax3.grid()
    # ax3.plot()

    ax2 = fig1.add_subplot(1,2,2) # plot do gráfico1
    ax2.set_title('Gráfico 1 das Formigas ')
    ax2.set_facecolor('#CCCCCC')
    ax2.grid()
    ax2.plot()

    ax1 = fig1.add_subplot(1,2,1) # plot do mapa
    ax1.set_title('Mapa de Colônia')
    ax1.set_xticklabels([])
    ax1.set_xlabel('Latitude')
    ax1.set_yticklabels([])
    ax1.set_ylabel('Longitude')
    ax1.set_facecolor('#CCCCCC')
    ax1.plot()

    nx.draw_networkx_nodes(mapa, pos, node_color='#6986a3',alpha=0.8, node_size=100)
    nx.draw_networkx_nodes(mapa, pos, nodelist=[origem], node_color='green', node_size=150, alpha=0.9, label='Origem')
    nx.draw_networkx_nodes(mapa, pos, nodelist=[destino], node_color='red', node_size=150, alpha=0.9, label='Destino')

    nx.draw_networkx_edges(mapa, pos, width=1.5, alpha=0.9, edge_color='white')

    nx.draw_networkx_labels(mapa, pos, font_size=6, font_color='white')
    # nx.draw_networkx_edge_labels(mapa, pos, font_size=5) # EXIBE OS PESOS DAS ARESTAS

    def refresh(x):
        for i in range(1):
            lista_caminho_formiga = []
            rota = []
            for j in range(formiga):
                list_caminho = []
                caminho(grafo, origem, destino, list_caminho)
                removeCiclo(list_caminho)
                lista_caminho_formiga.append(list_caminho)
            distanciaTotal = atualizaTaxaFeromonio(grafo, lista_caminho_formiga, coeficiente_evaporacao, lista_vertice)

            ax2.plot_date(lista_formigas, distanciaTotal)
            ax2.bar(lista_formigas, distanciaTotal, color='white', label='teste')
            ax2.plot(distanciaTotal, lw=0.02)
            # ax2.hist(distanciaTotal)

            print(distanciaTotal)
            for j in range(formiga):
                for k in range(len(lista_caminho_formiga[j]) - 1):
                    rota.append((lista_caminho_formiga[j][k], lista_caminho_formiga[j][k + 1]))
                nx.draw_networkx_edges(mapa, pos, edgelist=rota, width=2, alpha=0.01, edge_color='black')
                nx.draw_networkx_edges(mapa, pos, edgelist=rota_total, width=2.7, alpha=0.0095, edge_color='w')

        ax2.set_title('Comportamento das Formigas')
        ax2.set_ylabel('Distância (KM)')
        ax2.set_xticks(lista_formigas)
        ax2.set_xticklabels(distanciaTotal)
        ax2.set_xlabel('Distância Percorrida até o destino (KM)')

    plt.legend(loc='lower left')
    plt.imshow(im)
    ani1 = gif.FuncAnimation(fig1, refresh, iteracao, interval=vel_iteracao, repeat=False)
    plt.tight_layout()
    plt.show()

