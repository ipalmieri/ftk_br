from index_files import index_files
from parse_emails import parse_emails
from pymongo import MongoClient
from remove_accents import remove_accents
from pdf_to_text import pdf_to_text
from mongo_url import mongo_url
from recursive_folders import recursive_folders
import os, pymongo, sys, pickle

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
	indexFilePath = exitpath+'/'+id_inv + '_indicieDeOcorrenciaEmArquivo.pkl'
	words = { 
		"brand": []
	}
	words.clear()
	try:
		for f in paths:
			#insert_words(exitpath,pdf2txt.convert_Tika(f),str(f).split('/')[-1], id_inv)
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
		pass
	with open(indexFilePath, 'wb') as f:
		pickle.dump(words, f, pickle.HIGHEST_PROTOCOL)


def main(filepaths,id_inv, exitpath):
	pdf2txt = pdf_to_text()
	process_files(filepaths,exitpath,id_inv,pdf2txt)

if __name__ == '__main__':
	main(sys.argv[1],sys.argv[2], sys.argv[3])