from nltk.tokenize import RegexpTokenizer
from gensim import corpora, models
import gensim, nltk, pickle, pandas as pd, re

class inverse_index():
	"""Manipula topic models"""
	def __init__(self):
		pass

	def dicionario_invertido_id_texto(self,dados,dicionario_i = {},path_to_files=False):
		for id_,texto in dados:
			if path_to_files:
				dicionario_i_text = set(self.normalize_texts(self.file_to_string(texto),one_text=True))
			else:
				dicionario_i_text = set(self.normalize_texts(texto,one_text=True))
			for w in dicionario_i_text:
				if w in dicionario_i:
					dicionario_i[w].append(id_)
				else:
					dicionario_i[w] = [id_]
		return dicionario_i

	def encontra_doc_palavra(self, dicionario, palavra):
		documentos = []
		for k,v in dicionario.items():
			if re.search(palavra,k):
				documentos += v
		return documentos

	def escape_text_insert(self,text):
		return text.replace('"','').replace('/','').replace('\\','').replace('<','').replace('>','')

	def file_to_string(self,arq):
		try:
			arquivo = open(arq, "rb")
			return ''.join([line.decode('latin-1') for line in arquivo])
		except:
			arquivo = open(arq, "r")
			return ''.join([line for line in arquivo])

	def normalize_texts(self,texts,one_text = False):
		normal_texts = []
		tk = self.tokenizer()
		stopwords = nltk.corpus.stopwords.words('portuguese')
		if one_text:
			texts = [texts]
			texto_processado = []
		for t in texts:
			texto_bruto = t.lower()
			tokens = tk.tokenize(texto_bruto)
			texto_processado = []
			for tkn in tokens:
				if not (tkn in stopwords or tkn.isnumeric() or len(tkn) < 3):
					texto_processado.append(tkn)
			normal_texts.append(texto_processado)
		if one_text:
			return texto_processado
		return normal_texts

	def tokenizer(self):
		return RegexpTokenizer(r'\w+')

def main(file_path, csv_file=True, excel_file=False):
	pass

	# CRIAÇÃO DE DICIONÃRIO
	# if csv_file:
	# 	df = pd.read_csv(file_path)
	# paths = []
	# for index, row in df.iterrows():
	# 	if row['TIPO_ARQUIVO'] == 'txt':
	# 		paths.append((row['ID'], row['PATH_ARQUIVO']))
	# inv = inverse_index()
	# dicionario_teste = inv.dicionario_invertido_id_texto(paths,path_to_files=True)
	# pickle.dump(dicionario_teste,open('indice_invertido.pickle','wb'))

	# BUSCA POR PALAVRAS
	# inv = inverse_index()
	# dados = inv.encontra_doc_palavra(pickle.load(open('indice_invertido.pickle','rb')),r'investigado')
	# print(dados)

if __name__ == '__main__':
	main('indexação_arquivos_teste.csv')