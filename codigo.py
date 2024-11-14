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

sequencias = path_precision_explorer(grafo, "M1", 475, 500)
print(sequencias)

def gera_arvore(sequencia):
    pass