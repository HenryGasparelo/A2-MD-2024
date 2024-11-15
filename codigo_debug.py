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

# Dados das músicas
musicas = [
    ["M1", ["M2", "M3"], 134],
    ["M2", ["M1", "M4", "M5"], 112],
    ["M3", ["M1", "M4"], 145],
    ["M4", ["M2", "M5"], 120],
    ["M5", ["M1", "M3"], 138]
]

grafo = gera_grafo_input(musicas)
#print(grafo)


#[{'M1': [['M2', 'M3'], 134], 'M2': [['M1', 'M4', 'M5'], 112], 'M3': [['M1', 'M4'], 145], 'M4': [['M2', 'M5'], 120], 'M5': [['M1', 'M3'], 138]}, {('M1', 'M2'): 112, ('M1', 'M3'): 145, ('M2', 'M1'): 134, ('M2', 'M4'): 120, ('M2', 'M5'): 138, ('M3', 'M1'): 134, ('M3', 'M4'): 120, ('M4', 'M2'): 112, ('M4', 'M5'): 138, ('M5', 'M1'): 134, ('M5', 'M3'): 145}]

def path_precision_explorer(grafo, musica_inicial, limite_inferior, limite_superior, caminho=[], sequencias=[]):

    # Diminui dos limites inferior e superior a duracao da musica inicial
    limite_superior -=  grafo[0][musica_inicial][1]
    limite_inferior -=  grafo[0][musica_inicial][1]

    # Constroi o algoritmo com os limites atualizados
    def algoritmo(grafo, musica_inicial, limite_inferior, limite_superior, caminho=[], sequencias=[]):
        print(f"Interacao com vertice: {musica_inicial} e caminho: {caminho}")
        # Adiciona ao caminho o vertice da iteracao
        caminho = caminho + [musica_inicial]

        # Calcula o comprimento do caminho
        comprimento_caminho = 0
        for i in range(len(caminho)-1):
            comprimento_caminho += grafo[1][(caminho[i], caminho[i+1])]

        # Verifica se o comprimento do caminho esta dentro do intervalo desejado, se for, o adiciona a lista de sequencias possiveis
        if comprimento_caminho >= limite_inferior and comprimento_caminho <= limite_superior:
            print(f"{caminho} dentro do intervalo")
            sequencias.append(caminho)

        # Verifica se o comprimento do caminho passou do limite superior, se passar, retorna a lista de caminhos sem adicionar esse caminho
        elif comprimento_caminho > limite_superior:
            print(f"Caminho: {caminho} com comprimento maior que o limite superior")
            return sequencias
        else:
            print(f"Caminho: {caminho} com comprimento insuficiente")

        # Para cada vizinho do vertice da iteracao, caso o vizinho nao esteja no caminho, realiza o algoritmo com esse vizinho, adicionando os caminhos que estao no intervalo na lista de sequencias possiveis
        for vizinho in grafo[0][musica_inicial][0]:
            if not vizinho in caminho:
                algoritmo(grafo, vizinho, limite_inferior, limite_superior, caminho, sequencias)
                
        # Retorna a lista com todas as sequencias possiveis
        return sequencias
    
    # Retorna a lista com todas as sequencias possiveis 
    return algoritmo(grafo, musica_inicial, limite_inferior, limite_superior)

sequencias = path_precision_explorer(grafo, "M1", 375, 400)
print(sequencias)
print("="*121)

sequencias= [['M1', 'M2', 'M5'], ['M1', 'M3', 'M2', 'M4']]

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

def converter_para_grafo(dicionario):
    vertices = []
    arestas = []
    vertice_counter = {}

    def gerar_conexoes(pai, subgrafo):
        for filho in subgrafo:
            if filho not in vertice_counter:
                vertice_counter[filho]=0
            filho_id= f"{filho}_{vertice_counter[filho]}"
            vertices.append(filho_id)
            vertice_counter[filho] +=1

            arestas.append((pai, filho_id))

            gerar_conexoes(filho_id, subgrafo[filho])

    raiz = list(dicionario.keys())[0]
    raiz_id = f"{raiz}_0"
    vertices.append(raiz_id)
    gerar_conexoes(raiz_id, dicionario[raiz])

    return vertices, arestas

# Funcao temporaria para imprimir a arvore
def imprimir_arvore(arvore, nivel=0):
    for chave, valor in arvore.items():
        print("  " * nivel + chave)
        imprimir_arvore(valor, nivel + 1)
        
arvore = gera_arvore(sequencias)
print(arvore)
print("="*121)
imprimir_arvore(arvore)

print(converter_para_grafo(gera_arvore(path_precision_explorer(gera_grafo_input(musicas), "M1", 375, 400))))
