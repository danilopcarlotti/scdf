from bs4 import BeautifulSoup
from gensim.models import Word2Vec
from inverse_index import inverse_index
from matplotlib import pyplot
import re, sys, pandas as pd

class word2vec_textos():
	def __init__(self):
		self.modelo = None
		inv = inverse_index()
		self.file_to_string = inv.file_to_string

	def text_from_html_file(self,filepath):
		f = open(filepath, 'r')
		webpage = f.read()
		soup = BeautifulSoup(webpage,'html.parser')
		for script in soup(["script", "style"]):
			script.extract()
		return soup.get_text()

	def create_model(self, path_texto=None, path_multiple=None, filepath='word2vec_model.bin'):
		if path_multiple:
			sentences = []
			for p in path_multiple:
				sentences += [self.file_to_string(p).lower().split()]
		else:
			sentences = [self.file_to_string(path_texto).lower().split()]
		model = Word2Vec(sentences, min_count=1, size=150)
		model.save(filepath)

	def load_model(self,filepath='word2vec_model.bin'):
		self.modelo = Word2Vec.load(filepath)

def main():
	w = word2vec_textos()
	
	# GERA O MODELO
	# filepath = 'indexação_arquivos_teste.csv'
	# df = pd.read_csv(filepath, nrows=100)
	# paths = []
	# for index, row in df.iterrows():
	# 	if row['TIPO_ARQUIVO'] == 'txt':
	# 		paths.append(row['PATH_ARQUIVO'])
	# w.create_model(path_multiple=paths)
	
	# VOCABULÁRIO
	# w.load_model()
	# print(list(w.modelo.wv.vocab))

if __name__ == '__main__':
	main()