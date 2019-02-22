from bs4 import BeautifulSoup
from gensim.models import Word2Vec
from recursive_folders import recursive_folders
from pdf_to_text import pdf_to_text
from topicModelling import topicModelling
from word2vec_textos import word2vec_textos
import sys, os, mailparser, base64, re, pandas as pd, subprocess, networkx as nx, matplotlib.pyplot as plt, datetime, time, argparse

class parse_emails():
	"""Classe para processamento de emails"""
	def __init__(self, filepath, id_inv):
		self.bank_words = ['caixa','banco','itaú']
		self.filepath = filepath
		self.id_inv = id_inv
		self.nome_relatorio = 'relatório_emails_investigacao_%s.xlsx' % (str(self.id_inv),)
		self.graph = None
		self.words_of_interest = ['urgente','comprovante','extrato','cuidado']
	
	def docs_to_txt(self):
		r = recursive_folders()
		anexos = r.find_files(self.filepath)
		doc2txt = pdf_to_text()
		for anexo in anexos:
			if (anexo[-4:] == '.doc' or anexo[-4:] == 'docx' or anexo[-4:] == '.pdf'):
				texto = doc2txt.convert_Tika(anexo)
				arquivo = open(anexo[:-4]+'.txt','w')
				arquivo.write(texto)

	def email_bank_transactions(self):
		df = pd.read_excel(self.nome_relatorio)
		lista_emails_transacoes = []
		for index, row in df.iterrows():
			if re.search(r'comprovante.{1,10}transa',row['corpo'],flags=re.I|re.DOTALL):
				lista_emails_transacoes.append(row['data_envio']+'_'+row['nome_email'])
		return lista_emails_transacoes

	def email_contacts(self):
		df = pd.read_excel(self.nome_relatorio)
		df = df.fillna(' ')
		return list(df['remetente_email'].unique()) + list(df['destinatário_email'].unique())

	def email_names(self):
		df = pd.read_excel(self.nome_relatorio)
		df = df.fillna(' ')
		return list(df['nome_email'].unique())

	def email_subjects(self):
		df = pd.read_excel(self.nome_relatorio)
		df = df.fillna(' ')
		return list(df['assunto_limpo'].unique())

	def email_to_excel(self):
		lista_emails = [i for i in self.paths_to_emails(self.filepath) if i[-4:] == '.msg']
		rows = []
		for msg in lista_emails:
			body_e, date_e, from_e, recipient_e, subject_e, subject_e_clean, attachments = self.parse_msg(msg)
			if body_e != '':
				dicionario_aux = {
					'nome_email':msg.split('/')[-1][:-4],
					'corpo':body_e,
					'data_envio':date_e,
					'assunto':subject_e,
					'assunto_limpo':subject_e_clean,
					'anexos':str(attachments)
					}
				if from_e:
					dicionario_aux['remetente_nome'] = from_e[0][0]
					dicionario_aux['remetente_email'] = from_e[0][1]
				else:
					dicionario_aux['remetente_nome'] = ''
					dicionario_aux['remetente_email'] = ''
				if recipient_e:
					dicionario_aux['destinatário_nome'] = recipient_e[0][0]
					dicionario_aux['destinatário_email'] = recipient_e[0][1]
				else:
					dicionario_aux['destinatário_nome'] = ''
				dicionario_aux['destinatário_email'] = ''
				rows.append(dicionario_aux)
		if len(rows):
			index = [i for i in range(len(rows))]
			df = pd.DataFrame(rows,index=index)
			df = df.applymap(lambda x: x.encode('unicode-escape','replace').decode('utf-8') if isinstance(x, str) else x)
			df.to_excel(self.nome_relatorio,index=False)
			self.docs_to_txt()

	def email_to_graph(self):
		df = pd.read_excel(self.nome_relatorio)
		df = df.fillna(' ')
		self.graph = nx.DiGraph()
		for index, row in df.iterrows():
			if self.graph.has_edge(row['remetente_email'], row['destinatário_email']):
				self.graph[row['remetente_email']][row['destinatário_email']]['weight'] += 1
				self.graph[row['remetente_email']][row['destinatário_email']]['dates'].append(row['data_envio'])
				self.graph[row['remetente_email']][row['destinatário_email']]['subjects'].append(row['assunto_limpo'])
			else:
				self.graph.add_edge(row['remetente_email'], row['destinatário_email'], weight=1, dates=[row['data_envio']], subjects=[row['assunto_limpo']])
				print(type(row['data_envio']))

	def email_to_html(self,html_source, nome_pasta):
		try:
			arq_html = open(self.filepath.split('/')[-1].replace('.msg','.html'),'w')
			arq_html.write(html_source)
			subprocess.Popen('mv "%s" %s' % (self.filepath.split('/')[-1].replace('.msg','.html'),nome_pasta), shell=True) 
		except Exception as e:
			print(e)

	def email_to_pdf(self):
		nome_pasta = self.filepath.split('/')[-1][:-4]
		try:
			subprocess.Popen('python3 email2pdf -i "%s" -o "%s" --no-attachments --input-encoding latin_1' % (self.filepath,self.filepath.split('/')[-1].replace('.msg','.pdf')), shell=True) 
			time.sleep(1)
			subprocess.Popen('mv "%s" %s' % (self.filepath.split('/')[-1].replace('.msg','.pdf'),nome_pasta), shell=True) 
		except Exception as e:
			print(e)

	def parse_msg(self):
		mail = mailparser.parse_from_file(self.filepath)
		soup = BeautifulSoup(mail.body,'html.parser')
		for script in soup(["script", "style"]):
			script.extract()
		body_e = soup.get_text().lower()
		date_e = mail.date
		from_e = mail.from_	
		recipient_e = mail.delivered_to
		subject_e = mail.subject
		subject_e_clean = mail.subject.replace('Re:','').replace('Fwd:','').replace('RE:','').replace('FWD:','').replace('FW:','').replace('Fw:','').replace('ENC:','').replace('Enc:','').strip()
		anexos_nomes = []
		if date_e:
			date_e = date_e.strftime("%d/%m/%Y")
		nome_pasta = self.filepath[:-4]
		subprocess.Popen('mkdir "%s"' % (nome_pasta,), shell=True)
		self.email_to_html(mail.body, self.filepath, nome_pasta)
		if len(mail.attachments):
			for att in mail.attachments:
				anexos_nomes.append(att['filename'])
				with open(att['filename'], 'wb') as f:
					try:
						f.write(base64.b64decode(att['payload']))
					except: 
						pass
				subprocess.Popen('mv "%s" "%s"' % (att['filename'],nome_pasta), shell=True) 
		return (body_e, date_e, from_e, recipient_e, subject_e, subject_e_clean, anexos_nomes)

	def paths_to_emails(self):
		r = recursive_folders()
		return r.find_files(self.filepath)

	def relatorio_entidade(self,nome_entidade,nomes_testar):
		df = pd.read_excel(self.nome_relatorio)
		colunas_testar = ['corpo','destinatário_nome','destinatário_email','remetente_email','assunto_limpo','anexos']
		rows = []
		for ind,row in df.iterrows():
			entidade_encontrada = False
			for col in colunas_testar:
				for nome in nomes_testar:
					if not entidade_encontrada and re.search(nome.lower(),row[col].lower()):
						entidade_encontrada = True
						dicionario_aux = {
						'corpo':row['corpo'],
						'data_envio':row['data_envio'],
						'destinatário_nome':row['destinatário_nome'],
						'remetente_nome':row['remetente_nome'],
						'destinatário_email':row['destinatário_email'],
						'remetente_email':row['remetente_email'],
						'assunto':row['assunto'],
						'assunto_limpo':row['assunto_limpo'],
						'anexos':row['anexos']
						}
						rows.append(dicionario_aux)
		index = [i for i in range(len(rows))]
		df = pd.DataFrame(rows,index=index)
		df = df.applymap(lambda x: x.encode('unicode-escape','replace').decode('utf-8') if isinstance(x, str) else x)
		df.to_excel('relatório_'+nome_entidade+'.xlsx',index=False)

	def relatorio_geral(self, report_name='relatório_geral.txt'):
		try:
			df = pd.read_excel(self.nome_relatorio)
		except:
			return
		df = df.fillna(' ')
		contacts = self.email_contacts()
		names_email = self.email_names()
		subjects = self.email_subjects()
		transactions = self.email_bank_transactions()
		relatorio_txt = open('relatório_geral_%s' % (str(self.id_inv),),'w')
		relatorio_txt.write('Arquivos de emails disponíveis:\n\n\n')
		for n in names_email:
			relatorio_txt.write(str(n)+'\n')
		relatorio_txt.write('\n\nAssuntos dos emails:\n\n\n')
		for s in subjects:
			relatorio_txt.write(str(s)+'\n')
		relatorio_txt.write('\n\nContatos que receberam ou enviaram emails:\n\n\n')
		for c in contacts:
			relatorio_txt.write(str(c)+'\n')
		relatorio_txt.write('\n\nDatas e nomes dos emails que contém transações bancárias:\n\n\n')
		for t in transactions:
			relatorio_txt.write(str(t)+'\n')
		relatorio_txt.close()

	def text_to_html(self, texto):
		return texto.replace('\t',4*'&nbsp;').replace('\n','<br/>')

	def topics(self, prefix='wordcloud_topico_'):
		doc2txt = pdf_to_text()
		topM = topicModelling()
		r = recursive_folders()
		textos = [doc2txt.convert_Tika(t) for t in r.find_files(self.filepath) if t[-4:] == '.txt' or t[-5:] == '.html']
		topicos = topM.lda_Model(textos, npasses=1, num_words=10)
		topM.topic_to_img(topicos, prefix=prefix)

	def word_to_vec_textos(self):
		doc2txt = pdf_to_text()
		r = recursive_folders()
		w2v = word2vec_textos()
		textos = [doc2txt.convert_Tika(t) for t in r.find_files(self.filepath) if t[-4:] == '.txt' or t[-5:] == '.html']
		df = pd.read_excel(self.nome_relatorio)
		for index, row in df.iterrows():
			textos.append(str(row['corpo']))
		sentencas = [w2v.split_sentences(texto) for texto in textos]
		w2v.create_model(sentencas)

def main(filepath, id_inv):
	p = parse_emails(filepath, id_inv)
	p.email_to_excel()
	p.docs_to_txt()
	p.relatorio_geral()

if __name__ == '__main__':
	filepath = sys.argv[1]
	id_inv = sys.argv[2]
	main(filepath, id_inv)