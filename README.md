

O projeto Ant Colony Simulator foi feito em parceria dos alunos Leonardo e Wemerson, estudantes do curso de Ciência da Computação com o professor Daniel, ministrante da disciplina de Projetos e Análises de Algoritmos II, na Pontifícia Universidade Católica de Goiás. A finalidade do projeto foi compor a nota final da disciplina.

O funcionamento do algoritmo consiste em, após passados os parâmetros solicitados, encontrar um caminho ótimo entre uma ORIGEM até um DESTINO. O MAPA foi construído com base em um grafo, onde os nós são os pontos dados como CIDADES e as arestas são os caminhos entre elas. Cada aresta é ponderada com uma distância.

Em cada ponto de origem são depositadas um número N de formigas que atualizam, a cada iteração, a taxa de ferômonio contida em cada aresta, o que influencia na decisão de qual caminho a próxima formiga deve tomar.

Para fins de testes, foram utilizados os seguintes parâmetros:

ORIGEM: MS

DESTINO: PB

COEFICIENTE DE EVAPORAÇÃO: 0.3

NÚMERO DE ITERAÇÕES: 100

VELOCIDADE DE EXECUÇÃO: 700

NÚMERO DE FORMIGAS: 5

##########################################################

PARA EXECUTAR O CÓDIGO, BASTA EXECUTAR O SEGUINTE COMANDO:

python3 main.py

##########################################################

Necessário a instalação de algumas dependencias para a execução, testes e demonstração do projeto.

sudo pip install networkx && sudo pip install matplotlib && sudo pip install numpy && sudo pip install pandas && sudo pip install seaborn

** A interface gráfica é a execução do projeto kivi > 1.9

Instalar e verificar documentação sobre como implementá-la

Demais dependências já resolvidas na instalação do python 3.5 ou superior

Vídeo do funcionamento do algoritmo: https://www.youtube.com/watch?v=fMn1_6qhEn0&t=9s

