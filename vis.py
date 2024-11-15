import networkx as nx
import matplotlib.pyplot as plt

def visualizar_arvore(vertices, arestas):
    # Inicializa um grafo direcionado
    arvore = nx.DiGraph()

    # Adiciona os vértices ao grafo
    arvore.add_nodes_from(vertices)

    # Adiciona as arestas ao grafo
    arvore.add_edges_from(arestas)

    # Isso é importante para determinar o layout hierárquico
    raiz = vertices[0]

    # Define o layout hierárquico da árvore
    pos = _layout_hierarquico(arvore, raiz)

    # Desenha os vértices e as arestas no formato de árvore
    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(arvore, pos, node_size=500, node_color="lightgreen")
    nx.draw_networkx_edges(arvore, pos, arrowstyle="->", arrowsize=15, edge_color="gray")
    nx.draw_networkx_labels(arvore, pos, font_size=10, font_color="black", font_weight="bold")

    # Exibe o grafo no formato de árvore
    plt.axis("off")
    plt.show()


def _layout_hierarquico(grafo, raiz, largura=1.0, xcentro=0.5, ynivel=0.1, nivel=0, pos=None, pai=None):
    if pos is None:
        pos = {}
    # Define a posição da raiz no layout
    pos[raiz] = (xcentro, -nivel * ynivel)

    # Encontra os filhos da raiz no grafo
    filhos = list(grafo.successors(raiz))
    if len(filhos) > 0:
        # Calcula a largura disponível para cada subárvore
        dx = largura / len(filhos)
        # Posiciona cada filho recursivamente
        for i, filho in enumerate(filhos):
            pos = _layout_hierarquico(
                grafo,
                filho,
                largura=dx,
                xcentro=xcentro - largura / 2.0 + (i + 0.5) * dx,
                ynivel=ynivel,
                nivel=nivel + 1,
                pos=pos,
                pai=raiz,
            )
    return pos

#visualizar_arvore(vertices, arestas)