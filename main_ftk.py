from index_files import index_files
from inverse_index import inverse_index
from networkx_graphs import networkx_graphs
from parse_emails import parse_emails
from recursive_folders import recursive_folders
from tika_textos import tika_textos
from topicModelling import topicModelling
from word2vec_textos import word2vec_textos
import sys, os, pickle, subprocess, re, time, argparse, pandas as pd, networkx as nx, matplotlib.pyplot as plt

TIKA_CLASS = tika_textos()
RECURSIVE_CLASS = recursive_folders()

def indice_arquivos(filepaths,id_inv,path_inicial):
	i = index_files(filepaths)
	i.save_paths_file(path_inicial+'indice_arquivos_investigacao_'+str(id_inv),list_paths=filepaths, csv_file=True)

def indice_palavras_arquivos(filepath, id_inv, path_inicial):
	df = pd.read_csv(filepath)
	paths = []
	for index, row in df.iterrows():
		if row['TIPO_ARQUIVO'] == 'txt':
			paths.append((row['ID'], row['PATH_ARQUIVO']))
	if len(paths):
		inv = inverse_index()
		dicionario_teste = inv.dicionario_invertido_id_texto(paths,path_to_files=True)
		pickle.dump(dicionario_teste,open(path_inicial+'indice_invertido_investigacao_%s.pickle' % (str(id_inv),),'wb'))

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
	PARSER_EMAILS.email_to_excel(filepaths,filename='relatório_emails_investigação_%s.xlsx'%(str(id_inv),),lista_emails=True)
	PARSER_EMAILS.relatorio_geral(filename='relatório_emails_investigação_%s.xlsx'%(str(id_inv),), report_name='relatório_emails_investigação_%s.txt'%(str(id_inv),))

def processar_interceptacao_telefonica(filepath, id_inv, path_inicial, colunaOrig='Origem/IMEI',colunaDest='Destino/IMEI'):
	nt = networkx_graphs(file_path=filepath)
	nt.df_dir_graph(colunaOrig,colunaDest,excelf=True)
	nx.draw_circular(nt.graph,with_labels=True,edge_color='b')
	plt.savefig(path_inicial+filepath.split('/')[-1].split('.')[0]+'_'+str(id_inv)+'.png')
	relatorio = open(path_inicial+'relatório_bilhetagem_%s_investigacao_%s.txt' % (filepath.split('/')[-1],str(id_inv)),'w')
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
	pickle.dump(dicionario_resultados,open(path_inicial+'resultados_bilhetagem_'+filepath.split('/')[-1]+'.pickle', 'wb'), pickle.HIGHEST_PROTOCOL)

def topic_modelling(filepath,path_inicial):
	df = pd.read_csv(filepath)
	paths = []
	for index, row in df.iterrows():
		if row['TIPO_ARQUIVO'] == 'txt':
			paths.append(row['PATH_ARQUIVO'])
	if len(paths):
		texts = [''.join([line for line in open(p,'r')]) for p in paths]
		topicM = topicModelling()
		topicos = topicM.lda_Model(texts, num_topics=10, npasses=10, num_words=20)
		topicM.topic_to_txt(topicos,prefix=path_inicial)

def unzip_files(filepaths):
	for file in filepaths:
		try:
			subprocess.Popen('unzip -o "%s" -d "%s"' % (file,'/'.join(file.split('/')[:-1])), shell=True)
		except Exception as e:
			print(e)

def vetorizacao_textos(filepath, path_inicial):
	df = pd.read_csv(filepath)
	paths = []
	for index, row in df.iterrows():
		if row['TIPO_ARQUIVO'] == 'txt':
			paths.append(row['PATH_ARQUIVO'])
	if len(paths):
		w = word2vec_textos()
		w.create_model(filepath=path_inicial+'word2vec_model.bin',path_multiple=paths)

if __name__ == '__main__':

	path_inicial = sys.argv[1]
	id_inv = sys.argv[2]
	arq_bilhetagem = None
	if len(sys.argv) > 3:
		arq_bilhetagem = sys.argv[3]
		col_a_bil = None
		col_b_bil = None
		if len(sys.argv) == 6:
			col_a_bil = sys.argv[4]
			col_b_bil = sys.argv[5]

	# DESCOMPACTAR TODOS OS ARQUIVOS QUE PRECISAM SER DESCOMPACTADOS E DAR MOUNT NOS DEMAIS
	arquivos_descompactar = [f for f in RECURSIVE_CLASS.find_files(path_inicial) if f[-3:] == 'zip']
	unzip_files(arquivos_descompactar)
	arquivos_imagens = [f for f in RECURSIVE_CLASS.find_files(path_inicial) if re.search(r'E\d+',f[-4:],re.I)]
	mount_files_windows(arquivos_imagens,path_inicial)
	arquivos_descompactar = [f for f in RECURSIVE_CLASS.find_files(path_inicial) if f[-3:] == 'zip']
	unzip_files(arquivos_descompactar)

	# PROCESSAR EMAILS
	processar_email([i for i in RECURSIVE_CLASS.find_files(path_inicial) if i[-3:] == 'msg'], id_inv)
	
	# PROCESSAR OS PDF'S E ARQUIVOS DE WORD
	processar_arquivo_texto(RECURSIVE_CLASS.find_files(path_inicial))
	
	# GERAR TABELA COM OS ARQUIVOS
	indice_arquivos([i for i in RECURSIVE_CLASS.find_files(path_inicial) if i[-6:] != 'pickle' and i[-3:] != 'bin'], id_inv, path_inicial)
	
	# VETORIZAÇÃO E TOPIC MODELLING
	vetorizacao_textos(path_inicial+'indice_arquivos_investigacao_'+str(id_inv)+'.csv',path_inicial)
	topic_modelling(path_inicial+'indice_arquivos_investigacao_'+str(id_inv)+'.csv',path_inicial)

	# ÍNDICE REVERSO PARA PESQUISA DE PALAVRAS E DOCUMENTOS
	indice_palavras_arquivos(path_inicial+'indice_arquivos_investigacao_'+str(id_inv)+'.csv',id_inv,path_inicial)

	# PROCESSAR BILHETAGENS E GERAR RELATÓRIO
	if arq_bilhetagem:
		if col_a_bil:
			processar_interceptacao_telefonica(arq_bilhetagem, id_inv, path_inicial, colunaOrig=col_a_bil,colunaDest=col_b_bil)
		else:
			processar_interceptacao_telefonica(arq_bilhetagem, id_inv, path_inicial, colunaOrig='Origem/IMEI',colunaDest='Destino/IMEI')
	
	subprocess.Popen('rm %swordcloud*.txt' % (path_inicial,), shell=True)
