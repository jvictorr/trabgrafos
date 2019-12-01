Este trabalho é composto de duas partes, onde a primeira parte consiste em algoritmos de menores caminhos
e a segunda parte de algoritmos de fluxos máximos.

Por padrão o Ubuntu 18.04 tem o Python 2 e o Python 3 instalados.

Para executar os algoritmos deve-se seguir os seguintes passos.
1. Instalar o pip3 no Python 3 conforme os seguintes passos:
	- Executar o comando para atualizar a lista de pacotes:
		$ sudo apt update

	- Executar o comando para instalar o pip no Python 3:
		$ sudo apt install python3-pip

	- Verificar se o pip foi instalado corretamente com o seguinte comando:
		$ pip3 --version

	- Qualquer dúvida verificar o seguinte link:
		https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/

2. Instalar a biblioteca NumPy:
	- O NumPy é uma biblioteca do Python que é usada principalmente para realizar cálculos em Arrays 
	  Multidimensionais.

	- Executar o comando para instalar a biblioteca:
		$ sudo pip install numpy

3. Para executar os algoritmos rodar o comando seguinte na pasta correspondente do algoritmo desejado:
	$ python main.py

4. Um arquivo txt com o modelo de grafo está dentro de cada pasta dos algoritmos.