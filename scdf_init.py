from paths_init import *
from subprocess import check_output
import uuid, subprocess, re, os

print('Bem vindo ao SCDF!')
try:
	investigacoes_processadas = [line.strip() for line in open(path_scdf+'investigacoes_processadas.txt','r')]
	print('Encontrei as seguintes investigacoes ja processadas: ',' '.join(investigacoes_processadas))
except:
	arq_inv_processadas = open(path_scdf+'investigacoes_processadas.txt','w')
	arq_inv_processadas.close()
	investigacoes_processadas = []
	print('Nao ha investigacoes processadas ainda. Criando arquivo...')

try:
	arq_id_inv = open(path_arquivos+'ids_investigacoes.txt','a')
	print('Acessando arquivo com ids das investigacoes!')
except:
	arq_id_inv = open(path_arquivos+'ids_investigacoes.txt','w')
	print('Criano arquivo com ids das investigacoes!')

print('Processando investigacoes...')
investigacoes_a_processar = [j for j in os.listdir(path_arquivos)]
if not len(investigacoes_a_processar) == len(investigacoes_processadas):
	for i in investigacoes_a_processar:
		if i not in investigacoes_processadas and i != 'ids_investigacoes.txt':
			print('Processando a investigacao ',i)
			id_inv = str(uuid.uuid4()).split('-')[0]
			arq_id_inv.write('Investigação armazenada na pasta %s recebeu o id: %s\n' % (i, id_inv))

			print('Rodando o modulo de processamento de arquivos')
			subprocess.call(['python3','%sprocessar_arquivos.py' % (path_scdf,), path_arquivos+i, id_inv, path_relatorios])
			# print('Acabou!\nRodando o modulo de topic modelling')
			# subprocess.call(['python3','%stopic_modelling_inv.py' % (path_scdf,), path_arquivos+i, id_inv, path_relatorios])
			print('Acabou!\nRodando o modulo de word2vec')
			subprocess.call(['python3','%sword2vec_textos_inv.py' % (path_scdf,), path_arquivos+i, id_inv])
			print('Acabou! registrando a investigacao no arquivo respectivo!')

			arq_inv_processadas = open(path_scdf+'investigacoes_processadas.txt','a')
			arq_inv_processadas.write(i+'\n')
			arq_inv_processadas.close()

arq_id_inv.close()