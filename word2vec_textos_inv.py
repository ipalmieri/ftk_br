from gensim.models import Word2Vec
from recursive_folders import recursive_folders
from pdf_to_text import pdf_to_text
from stopwords_pt import stopwords_pt
import sys, re, json, pickle, string

sufixoarqwordtovec ='_Word2Vec_index.pkl'
def main(filepaths,id_investigacao,exitpath):
	indexFilePath = exitpath+'/'+id_investigacao + sufixoarqwordtovec
	id_inv = str(id_investigacao)
	pdf2txt = pdf_to_text()
	stpw = stopwords_pt()
	stopwords = stpw.stopwords()
	r = recursive_folders()
	ind_files = r.find_files(filepaths)
	texts2vec = []
	for f in ind_files:
		if f.split('.')[-1] in ['docx','doc','pdf','txt','html']:
			text_str = re.sub(r'\s+',' ',pdf2txt.convert_Tika(f))
			texts2vec.append(text_str.lower().split(' '))
	model2vec = Word2Vec(texts2vec, min_count=1)
	words = { 
		"brand": {"brand" : "brand" }
	}
	words.clear()
	for word in model2vec.wv.vocab:
		if len(word) > 3:
			for sim_word, similarity in sorted(model2vec.most_similar(word,topn=30),key=lambda x: abs(float(x[1])),reverse=True):
				sim_word = sim_word.replace('.','')
				if len(sim_word) > 3: 
					if word in words.keys():
						#if sim_word in words[word].keys(): 
							words[word][sim_word] = similarity
						#else:
						#	words[word][sim_word] = similarity
					else:
						words[word] = { 
								sim_word:similarity 
						}
	#saida do dicionário original
	with open(indexFilePath, 'wb') as f:
		pickle.dump(words, f, pickle.HIGHEST_PROTOCOL)
	#Como ler 
	#with open(indexFilePath, 'rb') as f:
	#	words2 = pickle.load(f)

def pesquisa(exitpath, id_inv, palavra ):
	indexFilePath = exitpath+'/'+id_inv + sufixoarqwordtovec
	#retira pontuação pq aoprocessar ele tira
	palavra = palavra.translate(str.maketrans('', '', string.punctuation))
	words2 = { 
		"brand": {"brand" : "brand" }
	}
	words2.clear()
	with open(indexFilePath, 'rb') as f:
		words2 = pickle.load(f)

	if palavra in words2.keys():
		return words2[palavra]
	return words2


def sufixo():
	return sufixoarqwordtovec

if __name__ == '__main__':
	main(sys.argv[1],sys.argv[2],sys.argv[3])