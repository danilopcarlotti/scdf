from subprocess import check_output
import uuid, subprocess, re, os

path_arquivos = '/mnt/Dados/Documents/scdf/teste/teste1/'
path_scdf = '/mnt/Dados/Documents/scdf/'
path_relatorios = '/mnt/Dados/Documents/scdf/teste/Relatórios/'

try:
	investigacoes_processadas = [line.strip() for line in open(path_scdf+'investigacoes_processadas.txt','r')]
except:
	arq_inv_processadas = open(path_scdf+'investigacoes_processadas.txt','w')
	arq_inv_processadas.close()
	investigacoes_processadas = []

try:
	arq_id_inv = open(path_arquivos+'ids_investigacoes.txt','a')
except:
	arq_id_inv = open(path_arquivos+'ids_investigacoes.txt','w')

investigacoes_a_processar = [j for j in os.listdir(path_arquivos)]
if not len(investigacoes_a_processar) == len(investigacoes_processadas):
	for i in investigacoes_a_processar:
		if i not in investigacoes_processadas and i != 'ids_investigacoes.txt':
			id_inv = str(uuid.uuid4()).split('-')[0]
			arq_id_inv.write('Investigação armazenada na pasta %s recebeu o id: %s\n' % (i, id_inv))

			subprocess.call(['python3','%s/processar_arquivos.py' % (path_scdf,), path_arquivos+i, id_inv, path_relatorios])
			subprocess.call(['python3','%s/topic_modelling_inv.py' % (path_scdf,), path_arquivos+i, id_inv, path_relatorios])
			subprocess.call(['python3','%s/word2vec_textos_inv.py' % (path_scdf,), path_arquivos+i, id_inv])
			
			arq_inv_processadas = open(path_scdf+'investigacoes_processadas.txt','a')
			arq_inv_processadas.write(i+'\n')
			arq_inv_processadas.close()

arq_id_inv.close()