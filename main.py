from lexico import Lexico
from sintatico_final import programa
from os.path import exists
import pdb

if __name__ == '__main__':

	# pdb.set_trace()
	#Verfica a existencia do arquivo
	if not exists('entrada.txt'):
		print('Arquivo Inexistente!')
		exit()

	#abrir arquivo
	arquivo = open('entrada.txt','r')
	#lendoo as linhas do arquivo
	texto = arquivo.readlines()

	lexico = Lexico(texto)
	tokens = lexico.tokenizar()
	# for i in tokens:
	# 	print(i)	
	
	sintatico = programa(tokens)
	if (sintatico):
		print("Sucesso na análise sintática.")

	arquivo.close()
