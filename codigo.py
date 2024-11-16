import networkx as nx
import matplotlib.pyplot as plt

def gera_grafo_input(musicas: list) -> list:
    # Define listas de vertices e arestas que serao preenchidas
    vertices = {}
    arestas = {}
    # Para cada musica adiciona o nome dela como vertice
    for musica in musicas:
        vertices[musica[0]] = [musica[1], musica[2]]
        # Para cada vizinho da musica, encontra ele na lista e coleta a duracao da musica correspondente
        for vizinho in musica[1]:
            for proxima in musicas:
                if vizinho == proxima[0]:
                    duracao= proxima[2]
            # Adiciona uma aresta que sai da musica, vai ate o vizinho e possui duracao da musica correspondente ao vizinho
            arestas[(musica[0], vizinho)] = duracao
    
    grafo = [vertices, arestas]
    return grafo

def path_precision_explorer(grafo, musica_inicial, limite_inferior, limite_superior, caminho=[], sequencias=[]):

    # Diminui dos limites inferior e superior a duracao da musica inicial
    limite_superior -=  grafo[0][musica_inicial][1]
    limite_inferior -=  grafo[0][musica_inicial][1]

    # Constroi o algoritmo com os limites atualizados
    def algoritmo(grafo, musica_inicial, limite_inferior, limite_superior, caminho=[], sequencias=[]):
        # Adiciona ao caminho o vertice da iteracao
        caminho = caminho + [musica_inicial]

        # Calcula o comprimento do caminho
        comprimento_caminho = 0
        for i in range(len(caminho)-1):
            comprimento_caminho += grafo[1][(caminho[i], caminho[i+1])]

        # Verifica se o comprimento do caminho esta dentro do intervalo desejado, se for, o adiciona a lista de sequencias possiveis
        if comprimento_caminho >= limite_inferior and comprimento_caminho <= limite_superior:
            sequencias.append(caminho)

        # Verifica se o comprimento do caminho passou do limite superior, se passar, retorna a lista de caminhos sem adicionar esse caminho
        elif comprimento_caminho > limite_superior:
            return sequencias

        # Para cada vizinho do vertice da iteracao, caso o vizinho nao esteja no caminho, realiza o algoritmo com esse vizinho, adicionando os caminhos que estao no intervalo na lista de sequencias possiveis
        for vizinho in grafo[0][musica_inicial][0]:
            if not vizinho in caminho:
                algoritmo(grafo, vizinho, limite_inferior, limite_superior, caminho, sequencias)
                
        # Retorna a lista com todas as sequencias possiveis
        return sequencias
    
    # Retorna a lista com todas as sequencias possiveis 
    return algoritmo(grafo, musica_inicial, limite_inferior, limite_superior)

def gera_arvore(sequencias):
    # Define a arvore inicialmente como um dicionario vazio
    arvore = {}
    # Para cada caminho, define o vertice inicial como a arvore para voltar para o nivel 0
    for caminho in sequencias:
        vertice_atual = arvore
        # Para cada vertice do caminho, verifica se ele ja esta na arvore como filho do vertice atual, se estiver, define esse filho como vertice atual, se nao estiver, insere esse vertice como filho do vertice atual e define esse filho como vertice atual
        for vertice in caminho:
            if not vertice in vertice_atual:
                vertice_atual[vertice] = {}
            vertice_atual = vertice_atual[vertice]
    
    # Retorna a arvore
    return arvore

# Função que converte uma estrutura de árvore em um grafo representado por vértices e arestas
def converter_para_grafo(pre_arvore):
    # Inicializa a lista de vértices do grafo
    vertices = []
    # Inicializa a lista de arestas do grafo
    arestas = []
    # Dicionário usado para rastrear quantas vezes cada vértice foi encontrado, garantindo identificadores únicos
    vertice_counter = {}

    # Função recursiva para processar cada vértice e suas conexões
    def gerar_conexoes(pai, subgrafo):
        # Itera sobre cada filho no subgrafo atual
        for filho in subgrafo:
            # Garante que o filho tenha um contador inicial no dicionário vertice_counter
            if filho not in vertice_counter:
                vertice_counter[filho] = 0
            # Cria um identificador único para o filho, baseado em seu contador
            filho_id = f"{filho}_{vertice_counter[filho]}"
            # Adiciona o identificador do filho à lista de vértices
            vertices.append(filho_id)
            # Incrementa o contador para o próximo identificador do mesmo vértice
            vertice_counter[filho] += 1

            # Adiciona uma aresta conectando o vértice pai ao filho no grafo
            arestas.append((pai, filho_id))

            # Chama recursivamente a função para processar os filhos do vértice atual
            gerar_conexoes(filho_id, subgrafo[filho])

    # Obtém o vértice raiz da árvore (primeira chave do dicionário)
    raiz = list(pre_arvore.keys())[0]
    # Cria um identificador único para o vértice raiz
    raiz_id = f"{raiz}_0"
    # Adiciona a raiz à lista de vértices
    vertices.append(raiz_id)
    # Inicia a construção do grafo a partir da raiz
    gerar_conexoes(raiz_id, pre_arvore[raiz])

    # Retorna as listas de vértices e arestas que representam o grafo
    return vertices, arestas

# Essa função não sei se precisa ser colocada no documento final
def visualicao_arvore(vertices, arestas):
    # Inicializa um grafo direcionado
    arvore = nx.DiGraph()

    # Adiciona os vértices ao grafo
    arvore.add_nodes_from(vertices)

    # Adiciona as arestas ao grafo
    arvore.add_edges_from(arestas)

    #Define a raiz
    raiz = vertices[0]

    def layout_arvore(grafo, raiz, largura= 1, x= 1, y= 1, nivel=0, pos= {}):
        # Define a posição da raiz do grafo
        pos[raiz]= (x, -(nivel * y))
        
        # Cria uma lista com todos os filhos do vertice definido como raiz
        filhos = list(grafo.successors(raiz))

        if len(filhos) > 0:
            # Calcula a largura para cada subárvore
            dx = largura / len(filhos)

            # Itera sobre todos os filhos e posiciona eles recursivamente
            for i, filho in enumerate(filhos):
                # A posição x é calculada com base na posição do pai, ajustando para distribuir os filhos uniformemente dentro da largura determidada, com cada filho centralizado no seu intervalo dx. 
                pos=layout_arvore(grafo = grafo, raiz = filho, largura = dx, x = x - largura / 2 + (i + 0.5) * dx, y = y, nivel=nivel+1, pos= pos)

        return pos
    
    # Difine usando um dicionario de tupla a posição da vértice 
    pos = layout_arvore(arvore, raiz)

    # Desenha os vértices e as arestas no formato de árvore
    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(arvore, pos, node_size=500, node_color="lightblue")
    nx.draw_networkx_edges(arvore, pos, arrowstyle="->", arrowsize=15, edge_color="gray")
    nx.draw_networkx_labels(arvore, pos, font_size=10, font_color="black", font_weight="bold")

    # Exibe o grafo no formato de árvore
    plt.axis("off")
    plt.show()

# Dados das músicas
musicas = [
    ["M1", ["M2", "M3", "M4", "M5"], 100],  # M1 conecta-se a outros, mas tempo é curto.
    ["M2", ["M1", "M3", "M5", "M6"], 450],  # Longo tempo, pode ser um gargalo.
    ["M3", ["M1", "M2", "M4", "M5", "M6"], 80],  # M3 é rápido, mas conectado a muitos.
    ["M4", ["M1", "M2", "M5"], 300],  # Tempo moderado, poucos vínculos.
    ["M5", ["M1", "M3", "M4", "M6"], 200],  # Intermediário, liga muitos.
    ["M6", ["M1", "M2", "M3", "M4"], 700],  # Tempo alto, pode causar conflito de ordem.
    ["B1", ["B2", "B3"], 50],  # Subconjunto desconectado do restante, com tempos baixos.
    ["B2", ["B1", "B3"], 500],  # Tempo elevado dentro de um subconjunto menor.
    ["B3", ["B1", "B2"], 600]   # Outra alta dependência no subconjunto.
]

grafo = gera_grafo_input(musicas)
sequencias = path_precision_explorer(grafo, "M1", 700, 1200)
pre_arvore = gera_arvore(sequencias)
vertices, arestas = converter_para_grafo(pre_arvore)
arvore = {"vertices": vertices, "arestas": arestas}

# Exibe os vértices e arestas do grafo convertido
print(arvore)

# Exibe a visualição da arvore usando networkx e matplotlib
visualicao_arvore(arvore["vertices"], arvore["arestas"])

