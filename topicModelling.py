from textNormalization import textNormalization
from gensim import corpora, models
import subprocess

class topicModelling(textNormalization):
	"""Creates topic models for normalized texts"""
	def __init__(self):
		super(topicModelling, self).__init__()
		
	def dicionario_corpora(self,textos):
		return corpora.Dictionary(textos)

	def lda_Model(self, texts, num_topics=5, npasses=20, num_words=15):
		'''O input precisa ser uma lista em que cada elemento da lista é uma string correspondendo a um texto'''
		textos = self.normalize_texts(texts)
		dicionario = self.dicionario_corpora(textos)
		corpus = [dicionario.doc2bow(text) for text in textos]
		return models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word = dicionario, passes=npasses).print_topics(num_topics=num_topics,num_words=num_words)

	def topic_to_txt(self, topics, prefix=''):
		for n,top in topics:
			arq = open(prefix+'wordcloud_topico_'+str(n)+'.txt','w')
			for t in top.split('+'):
				t = t.strip().replace('"','')
				n_t, word = t.split('*')
				arq.write(int(float(n_t)*10000)*(word+' '))
			subprocess.Popen('wordcloud_cli --text "%s" --imagefile "%swordcloud_%s.png" --no_collocations' % (prefix+'wordcloud_topico_'+str(n)+'.txt',prefix,str(n)),shell=True)