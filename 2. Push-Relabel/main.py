import math
import numpy as np

def matrizPesos():
	arquivo = open("grafo.txt","r") #Abrir o arquivo txt para leitura
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
print("MATRIZ DE PESOS INICIAL:")
print(w)
print("")
if(type(q) == int):
	print("Por favor, insira dois números na segunda linha do grafo.")
else:
	s = q[0]
	t = q[1]
	print("FLUXO MÁXIMO:")
	print(pushRelabel(w,s,t))
