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

##################################################################################
############################## Código principal ####################################
##################################################################################

w, q = matrizPesos()
print("MATRIZ DE PESOS INICIAL:")
print(w)
print("")
if(type(q) == int):
	print("MATRIZ DE MENORES CAMINHOS:")
	print(floydWarshall(w))
else:
    print("Por favor, insira apenas um número na segunda linha do grafo.")