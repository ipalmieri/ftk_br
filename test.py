from word2vec_textos import word2vec_textos
from pdf_to_text import pdf_to_text
import word2vec_textos_inv as word2vec_textos_inv
import processar_arquivos as processar_arquivos
import word2vec_textos_inv as word2vec_textos_inv
import os, subprocess, uuid, pickle

if __name__ == '__main__':
	menuinicial = 1
	menupastaprocessar = ''
	menupastadesaida = ''
	idinvestigacao = str(uuid.uuid4())
	indexFilePath = 'appprocess.cfg'
	appprocess = []
	appprocess.clear()
	if os.path.isfile(indexFilePath):
		with open(indexFilePath, 'rb') as f:
			appprocess = pickle.load(f)
	while int(menuinicial) != 0:
		menuinicial = input('Digite 0 para sair, 1 para processar, ou 2 para pesquisar palavra\n')
		if int(menuinicial) == 1:
			while menupastaprocessar == '' and not os.path.exists(menupastaprocessar) :
				menupastaprocessar = input('Digite o caminho da pasta a ser processada\n')
				while menupastadesaida == '' :
					menupastadesaida = input('Digite o caminho da pasta de saida\n')
					if(not os.path.exists(menupastadesaida)):
						subprocess.Popen('mkdir "%s"' % (menupastadesaida,), shell=True)
					appprocess.append({"menupastaprocessar":menupastaprocessar, "idinvestigacao":idinvestigacao,"menupastadesaida":menupastadesaida})
					processar_arquivos.main(menupastaprocessar, idinvestigacao, menupastadesaida)
					word2vec_textos_inv.main(menupastaprocessar, idinvestigacao, menupastadesaida)
					with open(indexFilePath, 'wb') as f:
						pickle.dump(appprocess, f, pickle.HIGHEST_PROTOCOL)
		elif int(menuinicial) == 2:
			if len(appprocess) > 0 :
				i = 1
				for process in appprocess : 
					print('Digite '+str(i)+' para pesquisar na pasta '+process['menupastaprocessar']+'')
					i = i + 1
				i = int(input())
				process = appprocess[i-1]
				palavra = input('Digite a palavra a ser pesquisada em '+process['menupastaprocessar']+'\n')
				#busca palavra exata e as palavras contenham
				retProcessArq = processar_arquivos.pesquisa(process['menupastadesaida'],process['idinvestigacao'], palavra)
				#exibe palavras correspondentes
				for key, value in retProcessArq.items():
					print('A palavra '+ key + ' consta no arquivo:' + ','.join(value)  )
				#busca palavra exata no contexto do word to vec 
				if any(retProcessArq) :
					retW2Vec  = word2vec_textos_inv.pesquisa(process['menupastadesaida'],process['idinvestigacao'], list(retProcessArq)[0])
				else:
					retW2Vec  = word2vec_textos_inv.pesquisa(process['menupastadesaida'],process['idinvestigacao'], palavra)

				#busca palavra exata no contexto do word to vec 
				#for key, value in retProcessArq.items():
					#busca palavras parecidas e junta numa lista sem repetir
				#	retW2Vec = {**retW2Vec, **word2vec_textos_inv.pesquisa(process['menupastadesaida'],process['idinvestigacao'], key)}
				print('As 10 palavras que constam no mesmo contexto são:')
				i = 0
				for key, value in retW2Vec.items():
					print( '"' + key + '", ranking de proximidade ' + str(value) + ';'  )
					i = i + 1 
					if i >= 10 :
						break
				
				#with open(indexFilePath, 'rb') as f:
				#	words2 = pickle.load(f)
					
