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
############################## Código principal ####################################
##################################################################################

w, q = matrizPesos()
print("MATRIZ DE PESOS INICIAL:")
print(w)
print("")
if(type(q) == int):
	print("MENORES CAMINHOS A PARTIR DO VÉRTICE INICIAL:")
	bellmanFord(w,q)
else:
    print("Por favor, insira apenas um número na segunda linha do grafo.")
