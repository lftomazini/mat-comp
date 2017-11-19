

#declaracao de variaveis globais
num_vertices = 6
anteriores =[] #ao percorrer um caminho, vai guardando os anteriores


def buscar_caminho(residual, fonte, terminal, anteriores):

    caminho = [] #array de caminhos que vai sendo montado da fonte ao terminal --> Pst
    visitado = []

    for i in range(0, num_vertices):
        visitado.append(0) #fonte foi visitada

    caminho.append(fonte)
    visitado[fonte] = True
    anteriores[fonte] = -1

    while not len(caminho) == 0: #enquanto o caminho nao acabou de ser montado

        u = caminho.pop(0) #vai tirando os vertices visitados

        for v in range(0, num_vertices): #para cada prox vertice
            if visitado[v] == False and residual[u][v] > 0: #se nao foi visitado e a capacidade é maior que zero
                caminho.append(v) #coloca no caminho
                visitado[v] = True #marca como visitado
                anteriores[v] = u #coloca no array de anteriores (visitados)

    if visitado[terminal]: #quando chegar no terminal, acabou o caminho
        return  True
    else:
        return False

def Ford_Fulkerson(grafo, fonte, terminal):

    u = 0
    v = 0

    residual = grafo

    fluxo_max = 0

    #faz o residual, isto é, volta do terminal pra fonte
    while buscar_caminho(residual, fonte, terminal, anteriores):

        fluxo = 9999999 #começa com o caminho do fluxo infinito

        v = terminal

        while not v == fonte: #enquando não chegar na fonte

            u = anteriores[v] #volta o caminho
            fluxo = min(fluxo, residual[u][v]) #pega o valor minimo
            v = anteriores[v] #troca com o anterior

        v = terminal

        while not v == fonte: #agora vai acrescentando nos valores das arestas pra montar o residual

            u = anteriores[v]
            residual[u][v] -= fluxo
            residual[v][u] += fluxo
            v = anteriores[v]

        fluxo_max += fluxo #para cada caminho, acrescenta o valor do fluxo

    return  fluxo_max


if __name__ == '__main__':

    grafo = [[0, 16, 13, 0, 0, 0],
             [0, 0, 10, 12, 0, 0],
             [0, 4, 0, 0, 14, 0],
             [0, 0, 9, 0, 0, 20],
             [0, 0, 0, 7, 0, 4],
             [0, 0, 0, 0, 0, 0]]
    '''grafo = [[0, 15, 10, 10, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 5, 0, 3, 7, 0, 0, 0, 0, 0],
             [0, 0, 0, 5, 9, 5, 5, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 6, 3, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 5, 8, 0, 0],
             [0, 0, 0, 0, 3, 0, 5, 0, 4, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 15],
             [0, 0, 0, 0, 0, 8, 0, 0, 10, 0, 0],
             [0, 0, 0, 0, 0, 0, 5, 0, 0, 10, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]'''

    for i in range(0, num_vertices):
        anteriores.append(0)

    print("fluxo maximo eh ", (Ford_Fulkerson(grafo, 0, num_vertices - 1)))






