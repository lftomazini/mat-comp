from __future__ import division
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pprint
import sys

pp = pprint.PrettyPrinter(depth=6)

w = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def transitions(A):
	n = len(A)
	p = [sum(A[i]) for i in range(n)]
	P = A

	for i in range (n):
		if p[i] != 0:
			for j in range (n):
				P[i][j] = P[i][j] / p[i]
		else:
			for j in range (n):
				P[i][j] = 1 / n

	return P

def power_method(k, w, P):
	for k in range(k):
	    aux = []
	    for i in range(len(P)):
	        aux.append(0)
	        for j in range(len(P)):
	            aux[i] += w[j]*P[j][i]
	    w = aux
	return w

def print_graph(G, output_name):
	labels= dict([((u,v,), d['weight']) for u, v, d in G.edges(data=True)])
	pos = nx.spring_layout(G)

	plt.clf()
	nx.draw(G, pos, with_labels = True)
	nx.draw_networkx_edge_labels(G, pos, labels)
	plt.savefig(output_name)

if __name__ == "__main__":
	A = np.loadtxt(sys.argv[1]).tolist()
	P = transitions(A)
	G = nx.DiGraph(np.array(P))
	print_graph(G, "states.png")
	pr = nx.pagerank(G, 0.9)
	pp.pprint(pr)
	w = power_method(50, w, P)
	state = 36
	print("Probabilidade do estado %d: %.5f %%" %(state, w[state - 1]*100))