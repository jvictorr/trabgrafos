import math
import numpy as np

def matrizPesos():
	arquivo = open("grafos.txt","r") #Abrir o arquivo txt para leitura
	texto = arquivo.readlines() #lista com todas as linhas do arquivo
	v = int(texto[0]) #Quantidade de vertices
	q = texto[1].split(" ")
	if(len(q)==1):
		q = int(q[0])
	else:
		q[0] = int(q[0])
		q[1] = int(q[1])

	arquivo.close() #Fecha o arquivo

	if(type(q) == int): #Opção de grafo para menores caminhos
		#Criação da matriz de adjacencia com todos os pesos infinitos inicialmente infinitos
		w = np.ones((v,v))*math.inf
		for i in range(v):
			w[i][i] = 0
	else: #Opção de grafo para problemas de fluxo
		w = np.zeros((v,v))

	#Criação da matriz de arestas e pesos, conforme o arquivo
	t = np.zeros((len(texto)-2,3),int)
	for i in range(len(texto)-2):
		a = texto[i+2].split(" ")
		for j in range(3):
			t[i,j] = int(a[j])

	#Atribuição dos pesos na matriz de adjacencia
	for i in range(len(t)):
		w[t[i,0],t[i,1]] = t[i,2]

	return w, q #Retorna

################################################################################
###################### Algoritmo de Floyd-Warshall #############################
################################################################################

def floydWarshall(w):
	d = w.copy()
	n = len(w)

	for k in range(n):
		for i in range(n):
			for j in range(n):
				if (d[i,j] > (d[i,k] + d[k,j])):
					d[i,j] = d[i,k] + d[k,j]
	return d

################################################################################
############## Algoritmo Genérico Recursivo de menor caminho ###################
################################################################################

def calcSP(w,i,j,m):
	if i == j:
		return 0
	if m == 1:
		return w[i,j]

	c = math.inf
	for k in range(len(w)):
		if c > (calcSP(w,i,k,m-1) + w[k,j]):
			c = calcSP(w,i,k,m-1) + w[k,j]
	return c


def menorRecSP(w):
	l = w.copy()
	for i in range(len(w)):
		for j in range(len(w)):
			l[i,j] = calcSP(w,i,j,len(w))
	return l

################################################################################
############################## Shortest-Path ###################################
################################################################################

def ShortPath(l, w):
	nVertices = len(w)
	l2 = np.ones((nVertices,nVertices))*math.inf
	for i in range(nVertices):
		l2[i,i] = 0

	for i in range(nVertices):
		for j in range(nVertices):
			c = math.inf
			for k in range(nVertices):
				if c > (l[i,k] + w[k,j]):
					c = l[i,k] + w[k,j]
			l2[i,j] = c

	return l2


def mainSP(w):
	l = w.copy()
	for i in range(len(w)):
		l = ShortPath(l,w)
	return l

################################################################################
############################## Bellman-Ford ####################################
################################################################################

def bellmanFord(w,q):
	d = np.ones((len(w),1))*math.inf
	pai = len(w)*[None]
	d[q] = 0

	for i in range(len(w)):
		for u in range(len(w)):
			for v in range(len(w)):
				if d[v] > d[u]+w[u,v]:
					d[v] = d[u]+w[u,v]
					pai[v] = u

	for u in range(len(w)):
		for v in range(len(w)):
			if d[v] > d[u]+w[u,v]:
				print("Possui circuito negativo!")
				return False

	for i in range(len(w)):
		if i!=q and pai[i] != None:
			aux = pai[i]
			p = []
			p.append(i)

			while aux != q:
				p.append(aux)
				aux = pai[aux]
			p.append(q)
			p.reverse()
			aux = p
			for i in range(len(aux)):
				print(aux[i],end="")
				if i != len(aux)-1:
					print("->",end="")
				else:
					print("")

	return True;


##################################################################################
############################## Busca em Profundidade #############################
##################################################################################

#Função necessária para os próximos algortimos
#Ela foi modificada para retornar se existe caminho entre dois vértices em específico

def buscaProfundidade(w,s,t,pai):
	# s = fonte
	# t = sorvedouro
	# pai = vetor de precedentes
	visitado = len(w)*[False]
	fila = []

	#Inicializando a fila com o vértice fonte e o marcando como visitado
	fila.append(s)
	visitado[s] = True

	while fila:

		x = fila.pop(0)

		for index,peso in enumerate(w[x]):
			if visitado[index] == False and peso > 0:
				fila.append(index)
				visitado[index] = True
				pai[index] = x
	if visitado[t]:
		return True
	else:
	   return False



##################################################################################
############################## Ford-Fulkerson ####################################
##################################################################################


def fordFulkerson(w,s,t):

	pai = len(w)*[-1]
	fluxoMax = 0
	grafoOriginal = np.copy(w)


	while buscaProfundidade(w,s,t,pai):

		fluxoCaminho = float('inf')
		x = t


		#Enquanto o vértice visitado não for a fonte
		while (x != s):
			#Certifica de encontrar a menor capacidade residual do reverso da aresta, ou seja, o maior fluxo da aresta.
			fluxoCaminho = min(fluxoCaminho, w[pai[x]][x])
			x = pai[x]

		fluxoMax += fluxoCaminho

		x = t
		while (x != s):
			y = pai[x]
			w[y][x] -= fluxoCaminho
			w[x][y] += fluxoCaminho
			x = pai[x]

	print('Arestas do corte mínimo:')
	for i, val in enumerate(w):
		for j, jval in enumerate(w[i]):
			if w[i][j] == 0 and grafoOriginal[i][j] > 0:
				print(i, ' - ', j)


	return fluxoMax


##################################################################################
################################ Push-Relabel ####################################
##################################################################################

def preflow(w, s):

    n = len(w)
    c = w.copy()
    f = [[0]*len(w) for i in range(n)]

    h = [0]*n
    e = [0]*n
    h[s] = n

    # push some substance to graph
    for i, p in enumerate(w[s]):
        f[s][i] += p
        f[i][s] -= p
        e[i] += p

    return f,c,h,e,n

def pushRelabel(w,s,t):

    f,c,h,e,n = preflow(w,s)
    # Relabel-to-front selection rule
    verticesList = [i for i in range(n) if i != s and i != t]

    # move through list
    i = 0
    while i < len(verticesList):
        vertexIndex = verticesList[i]
        previousHeight = h[vertexIndex]
        while e[vertexIndex] > 0:
            for neighbourIndex in range(n):
                # if it's neighbour and current vertex is higher
                if c[vertexIndex][neighbourIndex] - f[vertexIndex][neighbourIndex] > 0 and h[vertexIndex] > h[neighbourIndex]:
                    push(c,f,e,vertexIndex,neighbourIndex)
            relabel(c,f,h,n,vertexIndex)

            
        if h[vertexIndex] > previousHeight:
            # if it was relabeled, swap elements
            # and start from 0 index
            verticesList.insert(0, verticesList.pop(i))
            i = 0
        else:
            i += 1

    fluxoMax = sum(f[s])
    return fluxoMax
    

def push(c, f, e, fromIndex, toIndex):
    preflowDelta = min(e[fromIndex], c[fromIndex][toIndex] - f[fromIndex][toIndex])
    f[fromIndex][toIndex] += preflowDelta
    f[toIndex][fromIndex] -= preflowDelta
    e[fromIndex] -= preflowDelta
    e[toIndex] += preflowDelta

def relabel(c,f,h,n,vertexIndex):
    minHeight = None
    for toIndex in range(n):
        if c[vertexIndex][toIndex] - f[vertexIndex][toIndex] > 0:
            if minHeight is None or h[toIndex] < minHeight:
                minHeight = h[toIndex]

    if minHeight is not None:
        h[vertexIndex] = minHeight + 1



##################################################################################
############################## Código principal ####################################
##################################################################################



w, q = matrizPesos()
print(w)
if(type(q) == int):
	print(floydWarshall(w))
	print("")
	print(menorRecSP(w))
	print("")
	print(mainSP(w))
	bellmanFord(w,q)
else:
	s = q[0]
	t = q[1]
	print(pushRelabel(w,s,t))
