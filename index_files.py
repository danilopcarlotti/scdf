from recursive_folders import recursive_folders
import pandas as pd, sys

class index_files():

	def __init__(self, files_path):
		self.files_path = files_path
		self.recursive = recursive_folders()
	
	def file_type(self, file_name):
		return file_name.split('/')[-1].split('.')[-1]
	
	def list_paths_df(self, paths):
		rows = []
		contador = 1
		for path in paths:
			nome = path.split('/')[-1]
			rows.append({'NOME_ARQUIVO':nome, 'TIPO_ARQUIVO':self.file_type(path), 'PATH_ARQUIVO':path, 'ID':contador})
			contador += 1
		data_frame = pd.DataFrame(rows, index=[i for i in range(len(rows))])
		return data_frame

	def paths_df(self):
		paths = self.recursive.find_files(self.files_path)
		rows = []
		contador = 1
		for path in paths:
			nome = path.split('/')[-1]
			rows.append({'NOME_ARQUIVO':nome, 'TIPO_ARQUIVO':self.file_type(path), 'PATH_ARQUIVO':path, 'ID':contador})
			contador += 1
		data_frame = pd.DataFrame(rows, index=[i for i in range(len(rows))])
		return data_frame

	def save_paths_file(self, name_file, list_paths=False, csv_file=False, excel_file=False):
		if list_paths:
			if csv_file:
				self.list_paths_df(list_paths).to_csv(name_file+'.csv',index=False)
			elif excel_file:
				self.list_paths_df(list_paths).to_excel(name_file+'.xlsx',index=False)
		else:
			if csv_file:
				self.paths_df().to_csv(name_file+'.csv',index=False)
			elif excel_file:
				self.paths_df().to_excel(name_file+'.xlsx',index=False)

def main(files_path, id_inv):
	i = index_files(files_path)
	i.save_paths_file('indexação_arquivos_%s' % (str(id_inv),),csv_file=True)

if __name__ == '__main__':
	main(sys.argv[1],sys.argv[2])