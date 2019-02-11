from index_files import index_files
from networkx_graphs import networkx_graphs
from parse_emails import parse_emails
from recursive_folders import recursive_folders
from tika_textos import tika_textos
from topicModelling import topicModelling
import sys, os, pickle, subprocess, re, time, argparse

TIKA_CLASS = tika_textos()
RECURSIVE_CLASS = recursive_folders()

def indice_arquivos(filepaths, id_inv):
	i = index_files(filepaths)
	i.save_paths_file('indice_arquivos_investigacao_'+str(id_inv),list_paths=filepaths, csv_file=True)

def indice_palavras_arquivos(filepath, id_inv):
	df = pd.read_csv(filepath)
	paths = []
	for index, row in df.iterrows():
		if row['TIPO_ARQUIVO'] == 'txt':
			paths.append((row['ID'], row['PATH_ARQUIVO']))
	inv = inverse_index()
	dicionario_teste = inv.dicionario_invertido_id_texto(paths,path_to_files=True)
	pickle.dump(dicionario_teste,open('indice_invertido_investigacao_%s.pickle' % (str(id_inv),),'wb'))

def mount_files_windows(filepaths, path_inicial):
	for file in filepaths:
		try:
			dir_name = file.split('.')[-1]
			subprocess.Popen('mkdir %s' % (path_inicial+dir_name,), shell=True)
			subprocess.Popen('ewfmount %s %s' % (file,path_inicial+dir_name), shell=True)
			time.sleep(2)
			subprocess.Popen('mount %s/ewf1 %s -o ro,loop,show_sys_files,streams_interace=windows' % (path_inicial+dir_name,path_inicial+dir_nameshow_sys_files,), shell=True)
		except Exception as e:
			print(e)

def processar_arquivo_texto(filepaths):
	for filepath in filepaths:
		if filepath[-4:] == 'docx' or filepath[-3:] == 'pdf' or filepath[-3:] == 'doc':
			texto = TIKA_CLASS.process_file(filepath)
			arq = open(filepath.split('.')[0]+'.txt','w')
			arq.write(texto)
			arq.close()

def processar_email(filepaths, id_inv):
	PARSER_EMAILS = parse_emails()
	PARSER_EMAILS.email_to_excel(filepaths,filename='relatório_emails_investigação_%s.xlsx'%(str(id_inv),))
	PARSER_EMAILS.relatorio_geral(filename='relatório_emails_investigação_%s.xlsx'%(str(id_inv),), report_name='relatório_emails_investigação_%s.txt'%(str(id_inv),))

def processar_interceptacao_telefonica(filepath, id_inv, colunaOrig='Origem/IMEI',colunaDest='Destino/IMEI'):
	nt = networkx_graphs(file_path=filepath)
	nt.df_dir_graph(colunaOrig,colunaDest,investigationID=int(id_inv),excelf=True)
	nx.draw_circular(nt.graph,with_labels=True,edge_color='b')
	plt.savefig(filepath.split('/')[-1][:-5]+'_'+id_inv+'.png')
	relatorio = open('relatório_bilhetagem_%s_investigacao_%s.txt' % (filepath.split('/')[-1],str(id_inv)),'w')
	relatorio.write('Nome do arquivo analisado: '+filepath.split('/')[-1])
	relatorio.write('\nEstes são os números que fazem ou recebem ligações\n')
	for i in nt.graph.nodes:
		relatorio.write(str(i)+'\n')
	relatorio.write('\nAnálise de ciclos fechados - números que fazem e que recebem ligações mutuamente\n')
	relatorio.write(str(nt.simple_cycles()))
	relatorio.write('\nNúmeros que se falam\n')
	relatorio.write(str(nt.degree_edges()))
	relatorio.write('\nQuantidade de ligações entre números\n')
	relatorio.write(str(nt.get_edge_attributes(sorted_tuples=True)))
	relatorio.close()
	dicionario_resultados = {
		'Nome do arquivo analisado' : filepath.split('/')[-1],
		'Nós que interagem entre si' : nt.graph.nodes,
		'Ciclos fechados' : nt.simple_cycles(),
		'Quantidade de arestas que chegam ou saem dos nós' : nt.degree_edges(),
		'Quantidade de arestas entre nós' : nt.get_edge_attributes(sorted_tuples=True)
	}
	pickle.dump(dicionario_resultados,'resultados_bilhetagem_%s_investigacao_%s.pickle' % (filepath.split('/')[-1],str(id_inv), 'wb'))

def topic_modelling(filepath):
	df = pd.read_csv(filepath)
	paths = []
	for index, row in df.iterrows():
		if row['TIPO_ARQUIVO'] == 'txt':
			paths.append(row['PATH_ARQUIVO'])
	texts = [''.join([line for line in open(p,'r')]) for p in paths]
	topicM = topicModelling()
	topicos = topicM.lda_Model(texts, num_topics=15, npasses=10, num_words=20)
	tp.topic_to_txt(topicos)

def unzip_files(filepaths):
	for file in filepaths:
		try:
			subprocess.Popen('unzip -o "%s" -d "%s"' % (file,'/'.join(file.split('/')[:-1])), shell=True)
		except Exception as e:
			print(e)

def vetorizacao_textos(filepath):
	df = pd.read_csv(filepath)
	paths = []
	for index, row in df.iterrows():
		if row['TIPO_ARQUIVO'] == 'txt':
			paths.append(row['PATH_ARQUIVO'])
	w.create_model(path_multiple=paths)

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Argumentos para geração de relatórios - FTK_br')
	parser.add_argument('-b', help='Gerar relatório de bilhetagem a partir de arquivo xlsx', nargs='*')
	args = parser.parse_args()

	# DETERMINAÇÃO DO DIRETÓRIO RAIZ ONDE OS ARQUIVOS SE ENCONTRAM
	path_inicial = sys.argv[1]
	id_inv = sys.argv[2]
	arquivos_iniciais = RECURSIVE_CLASS.find_files(path_inicial)

	# DESCOMPACTAR TODOS OS ARQUIVOS QUE PRECISAM SER DESCOMPACTADOS E DAR MOUNT NOS DEMAIS
	arquivos_descompactar = [f for f in RECURSIVE_CLASS.find_files(path_inicial) if f[-3:] == 'zip']
	unzip_files(arquivos_descompactar)
	arquivos_imagens = [f for f in RECURSIVE_CLASS.find_files(path_inicial) if re.search(r'E\d+',f[-4:],re.I)]
	mount_files_windows(arquivos_imagens,path_inicial)
	arquivos_descompactar = [f for f in RECURSIVE_CLASS.find_files(path_inicial) if f[-3:] == 'zip']
	unzip_files(arquivos_descompactar)

	# CRIAR ROTINA PARA ENCONTRAR TODOS OS ARQUIVOS POSSÍVEIS
	arquivos_final = RECURSIVE_CLASS.find_files(path_inicial)
	
	# PROCESSAR EMAILS
	processar_email(arquivos_final, id_inv)

	# PROCESSAR OS PDF'S E ARQUIVOS DE WORD
	processar_arquivo_texto(arquivos_final)
	
	# GERAR TABELA COM OS ARQUIVOS
	indice_arquivos(arquivos_final, id_inv)

	# VETORIZAÇÃO E TOPIC MODELLING
	vetorizacao_textos('indice_arquivos_investigacao_'+str(id_inv)+'.csv')
	topic_modelling('indice_arquivos_investigacao_'+str(id_inv)+'.csv')

	# ÍNDICE REVERSO PARA PESQUISA DE PALAVRAS E DOCUMENTOS
	indice_palavras_arquivos('indice_arquivos_investigacao_'+str(id_inv)+'.csv',id_inv)

	# PROCESSAR BILHETAGENS E GERAR RELATÓRIO
	if len(args.b == 1):
		processar_interceptacao_telefonica(args.b[0], id_inv, colunaOrig='Origem/IMEI',colunaDest='Destino/IMEI')
	else:
		processar_interceptacao_telefonica(args.b[0], id_inv, colunaOrig=args.b[1],colunaDest=args.b[2])