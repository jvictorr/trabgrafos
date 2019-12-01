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

	print('ARESTAS DO CORTE MÍNIMO:')
	for i, val in enumerate(w):
		for j, jval in enumerate(w[i]):
			if w[i][j] == 0 and grafoOriginal[i][j] > 0:
				print(i, ' - ', j)

	print("FLUXO MÁXIMO:")
	return fluxoMax

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
	print(fordFulkerson(w,s,t))
