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

	return w, q #Retorna 

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


w, q = matrizPesos()
print(w)
print(floydWarshall(w))
menorRecSP(w)
#print(mainSP(w))

