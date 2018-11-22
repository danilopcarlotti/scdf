from recursive_folders import recursive_folders
import pandas as pd

class index_files():
	def __init__(self, files_path):
		self.files_path = files_path
		self.recursive = recursive_folders()
	

	def file_type(self, file_name):
		return file_name.split('/')[-1].split('.')[-1]
	
	def paths_df(self):
		paths = self.recursive.find_files(self.files_path)
		index = [i for i in range(len(paths))]
		rows = []
		contador = 1
		for path in paths:
			nome = path.split('/')[-1]
			rows.append({'NOME_ARQUIVO':nome, 'TIPO_ARQUIVO':self.file_type(path), 'PATH_ARQUIVO':path, 'ID':contador})
			contador += 1
		data_frame = pd.DataFrame(rows, index=index)
		return data_frame

	def save_paths_file(self, name_file, csv_file=False, excel_file=False):
		if csv_file:
			self.paths_df().to_csv(name_file+'.csv',index=False)
		elif excel_file:
			self.paths_df().to_excel(name_file+'.xlsx',index=False)

def main():
	i = index_files('')
	i.save_paths_file('indexação_arquivos_teste',csv_file=True)

if __name__ == '__main__':
	main()