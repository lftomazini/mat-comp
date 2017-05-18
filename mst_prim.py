import sys
import numpy as np
import networkx as nx
import heapq as hq
import matplotlib.pyplot as plt

def prim(G):
    for u in G.nodes():
        G.node[u]['cost'] = float("inf")
        G.node[u]['predecessor'] = None

    r = G.nodes()[0]
    G.node[r]['cost'] = 0

    Q = [(G.node[u]['cost'], u) for u in G.nodes()]
    hq.heapify(Q)

    visited = []
    while len(Q) != 0:
        weight, u = hq.heappop(Q)
        visited.append(u)
        for v in G.neighbors(u):
            v = v.item()
            if v not in visited:
                if G.get_edge_data(u, v)['weight'] < G.node[v]['cost']:
                    G.node[v]['predecessor'] = u
                    G.node[v]['cost'] = G.get_edge_data(u, v)['weight']
                    hq.heappush(Q, (G.node[v]['cost'], v))

    T = nx.Graph()
    for u in G.nodes():
        T.add_node(u)
        v = G.node[u]['predecessor']
        if v is not None:
            T.add_edge(u, v)
            T[u][v]['weight'] = G[u][v]['weight']
    return T

def dijkstra(G):
    for u in G.nodes():
        G.node[u]['cost'] = float("inf")
        G.node[u]['predecessor'] = None

    r = G.nodes()[0]
    G.node[r]['cost'] = 0

    Q = [(G.node[u]['cost'], u) for u in G.nodes()]
    hq.heapify(Q)

    visited = []
    while len(Q) != 0:
        weight, u = hq.heappop(Q)
        visited.append(u)
        for v in G.neighbors(u):
            v = v.item()
            if v not in visited:
                if G.get_edge_data(u, v)['weight'] + G.node[u]['cost'] < G.node[v]['cost']:
                    G.node[v]['predecessor'] = u
                    G.node[v]['cost'] = G.get_edge_data(u, v)['weight'] + G.node[u]['cost']
                    hq.heappush(Q, (G.node[v]['cost'], v))

    T = nx.Graph()
    for u in G.nodes():
        T.add_node(u)
        v = G.node[u]['predecessor']
        if v is not None:
            T.add_edge(u, v)
            T[u][v]['weight'] = G[u][v]['weight'] + G.node[v]['cost']
    return T

def print_graph(G, output_name):
    labels= dict([((u,v,), d['weight']) for u, v, d in G.edges(data=True)])
    pos = nx.circular_layout(G)

    plt.clf()
    nx.draw(G, pos, with_labels = True)
    nx.draw_networkx_edge_labels(G, pos, labels)
    plt.savefig(output_name)

if __name__ == "__main__":
    A = np.loadtxt(sys.argv[1])
    G = nx.from_numpy_matrix(A)
    print_graph(G, 'graph.png')

    prim = prim(G)
    print_graph(prim, 'prim.png')

    dijkstra = dijkstra(G)
    print_graph(dijkstra, 'dijkstra.png')
