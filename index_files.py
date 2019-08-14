from recursive_folders import recursive_folders
from pdf_to_text import pdf_to_text
import pandas as pd, sys, pickle, nltk, re

class index_files():

	def __init__(self, files_path):
		self.files_path = files_path
		self.recursive = recursive_folders()
	
	def file_type(self, file_name):
		if '/' in file_name:
				file_name = file_name.split('/')[-1].split('.')[-1]
		else:
			file_name = file_name.split('.')[-1]
		return file_name
	
	def list_paths_df(self, paths):
		rows = []
		contador = 1
		for path in paths:
			if '/' in path:
				nome = path.split('/')[-1]
			else:
				nome = path
			rows.append({'NOME_ARQUIVO':nome, 'TIPO_ARQUIVO':self.file_type(path), 'PATH_ARQUIVO':path, 'ID':contador})
			contador += 1
		data_frame = pd.DataFrame(rows, index=[i for i in range(len(rows))])
		return data_frame

	def paths_df(self):
		paths = self.recursive.find_files(self.files_path)
		rows = []
		contador = 1
		for path in paths:
			if '/' in path:
				nome = path.split('/')[-1]
			else:
				nome = path
			rows.append({'NOME_ARQUIVO':nome, 'TIPO_ARQUIVO':self.file_type(path), 'PATH_ARQUIVO':path, 'ID':contador})
			contador += 1
		data_frame = pd.DataFrame(rows, index=[i for i in range(len(rows))])
		return data_frame

	def save_paths_file(self, name_file, id_inv, list_paths=False, csv_file=False, excel_file=False):
		if list_paths:
			df = self.list_paths_df(list_paths)
		else:
			df = self.paths_df()
		if csv_file:
			df.to_csv(name_file+'.csv',index=False)
		elif excel_file:
			df.to_excel(name_file+'.xlsx',index=False)
		dicionario_indice_arquivos = {}
		dicionario_indice_palavras = {}
		pdf2txt = pdf_to_text()
		stopwords = nltk.corpus.stopwords.words('portuguese')
		for index, row in df.iterrows():
			if row['TIPO_ARQUIVO'] in ['docx','doc','pdf','txt']:
				text = re.sub(r'\s+',' ',pdf2txt.convert_Tika(row['PATH_ARQUIVO']))
				list_words = list(set([w.strip().lower() for w in text.split(' ') if not (len(w) < 3 or w.isnumeric() or w in stopwords)]))
				for lw in list_words:
					if lw not in dicionario_indice_palavras:
						dicionario_indice_palavras[lw] = []
					dicionario_indice_palavras[lw].append(row['ID'])
				dicionario_indice_arquivos[row['ID']] = row['PATH_ARQUIVO']
		print(dicionario_indice_palavras)
		pickle.dump(dicionario_indice_arquivos,open('dicionario_indice_arquivos_%s.pickle' % (id_inv,),'wb'))
		pickle.dump(dicionario_indice_palavras, open('dicionario_indice_palavras_%s.pickle' % (id_inv,),'wb'))

def main(files_path, id_inv):
	i = index_files(files_path)
	i.save_paths_file('indexação_arquivos_%s' % (str(id_inv),), id_inv, csv_file=True)

if __name__ == '__main__':
	main(sys.argv[1],sys.argv[2])