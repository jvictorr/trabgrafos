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

	#Criação da matriz de adjacencia com todos os pesos infinitos inicialmente
	w = np.ones((v,v))*math.inf
	for i in range(v):
		w[i][i] = 0

	#Criação da matriz de arestas e pesos, conforme o arquivo
	t = np.zeros((len(texto)-2,3),int)
	for i in range(len(texto)-2):
		a = texto[i+2].split(" ")
		for j in range(3):
			t[i,j] = int(a[j])

	#Atribuição dos pesos na matriz de adjacencia
	for i in range(len(t)):
		w[t[i,0],t[i,1]] = t[i,2]

	return w, q, v #Retorna

################################################################################
###################### Algoritmo de Floyd-Warshall #############################
################################################################################

def floydWarshall(w):
	d = w
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
	l = w
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
	l = w
	for i in range(len(w)):
		l = ShortPath(l,w)
	return l

# The main function that finds shortest distances from src to
# all other vertices using Bellman-Ford algorithm.  The function
# also detects negative weight cycle


def BellmanFord(v,w,src):

	# Step 1: Initialize distances from src to all other vertices
	# as INFINITE
	dist = [float("Inf")] * v
	dist[src] = 0

	# Step 2: Relax all edges |V| - 1 times. A simple shortest
	# path from src to any other vertex can have at-most |V| - 1
	# edges
	for i in range(v - 1):
		# Update dist value and parent index of the adjacent vertices of
		# the picked vertex. Consider only those vertices which are still in
		# queue
		for i in range(v):
			for j in range (v):
				if dist[i] != float("Inf") and dist[i] + w[i,j] < dist[j]:
					dist[j] = dist[i] + w[i,j]

	# Step 3: check for negative-weight cycles.  The above step
	# guarantees shortest distances if graph doesn't contain
	# negative weight cycle.  If we get a shorter path, then there
	# is a cycle.

	for i in range(v):
		for j in range (v):
			if dist[i] != float("Inf") and dist[i] + w[i,j] < dist[j]:
				print("Graph contains negative weight cycle")
				return
	# print all distance
	print(dist)

w, q, v = matrizPesos()
BellmanFord(v,w,0)
print(w)
print(floydWarshall(w))
menorRecSP(w)
#print(mainSP(w))
