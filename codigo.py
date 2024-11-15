# Dados das músicas
musicas = [
    ["M1", ["M2", "M3"], 134],
    ["M2", ["M1", "M4", "M5"], 112],
    ["M3", ["M1", "M4"], 145],
    ["M4", ["M2", "M5"], 120],
    ["M5", ["M1", "M3"], 138]
]

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

grafo = gera_grafo_input(musicas)
sequencias = path_precision_explorer(grafo, "M1", 375, 400)
pre_arvore = gera_arvore(sequencias)
arvore = converter_para_grafo(pre_arvore)

# Exibe os vértices e arestas do grafo convertido
print(arvore)

