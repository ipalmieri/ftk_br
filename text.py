from word2vec_textos import word2vec_textos

if __name__ == '__main__':
	w = word2vec_textos()
	print(w.pesquisar_palavra(sys.argv[1]))
