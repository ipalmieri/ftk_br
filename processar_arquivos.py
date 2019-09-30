from index_files import index_files
from parse_emails import parse_emails
from remove_accents import remove_accents
from pdf_to_text import pdf_to_text
from recursive_folders import recursive_folders
import os, pymongo, sys, pickle

sufixoarqwords = '_indicieDeOcorrenciaEmArquivo.pkl'
def process_files(filepaths, exitpath, id_inv, pdf2txt):
	#Inicializa o processador de emails 
	PARSER_EMAILS = parse_emails(filepaths, id_inv, exitpath)
	#realmente processa o conteudo
	PARSER_EMAILS.email_to_excel(exitpath)
	#deveria gerar um relatório com os email mas não gera pq ta bugado
	PARSER_EMAILS.relatorio_geral(exitpath)
	i = index_files(filepaths)
	#Gera um arquivo com todos os arquivos 
	i.save_paths_file('indice_arquivos_investigacao_'+id_inv, exitpath, id_inv, excel_file=True)
	r = recursive_folders()
	paths = r.find_files(filepaths)
	indexFilePath = exitpath+'/'+id_inv + sufixoarqwords
	errorFilePath = exitpath+'/'+id_inv + "Errecursive_folders.txt"
	arquivosnaoprocessados = []
	words = { 
		"brand": []
	}
	words.clear()
	for f in paths:
		try:
			#Grava um indice indicando em quais arquivos aparece a palavra
			texto = pdf2txt.convert_Tika(f)
			file = str(f).split('/')[-1]
			palavras = list(set([remove_accents(w.strip()).lower() for w in texto.split() if (len(w) > 3 and not w.isnumeric())]))
			for p in palavras:
				if not p in words.keys():
					words[p] = []
					words[p].append(file)
				else:
					words[p].append(file)
		except Exception as e:
			arquivosnaoprocessados.append(str(f))
			pass
			
	with open(indexFilePath, 'wb') as f:
		pickle.dump(words, f, pickle.HIGHEST_PROTOCOL)

	with open(errorFilePath, 'w') as f:
		for item in arquivosnaoprocessados:
			f.write("%s\n" % item)

def main(filepaths,id_inv, exitpath):
	pdf2txt = pdf_to_text()
	process_files(filepaths,exitpath,id_inv,pdf2txt)

def pesquisa(exitpath, id_inv, palavra ):
	indexFilePath = exitpath+'/'+id_inv + sufixoarqwords
	palavra = remove_accents(palavra)
	ret = {'':[]}
	ret.clear()
	with open(indexFilePath, 'rb') as f:
		words2 = pickle.load(f)
	for key, value in words2.items():
		if palavra.lower() == key.lower():
			first = {key:value}
			ret = {**ret, **first}
		elif palavra.lower() in key.lower():
			ret[key] = words2[key]

	return ret


def sufixo():
	return sufixoarqwords

if __name__ == '__main__':
	main(sys.argv[1],sys.argv[2], sys.argv[3])