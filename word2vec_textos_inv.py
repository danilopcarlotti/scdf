from gensim.models import Word2Vec
from recursive_folders import recursive_folders
from pdf_to_text import pdf_to_text
from stopwords_pt import stopwords_pt
from pymongo import MongoClient
from mongo_url import mongo_url
import sys, re

def main(filepaths,id_investigacao):
	id_inv = str(id_investigacao)
	myclient = MongoClient(mongo_url)
	mydb = myclient["SCDF_"+id_inv]
	mycollection = mydb['vetores_palavras_similares_'+id_inv]
	pdf2txt = pdf_to_text()
	stpw = stopwords_pt()
	stopwords = stpw.stopwords()
	r = recursive_folders()
	ind_files = r.find_files(filepaths)
	texts2vec = []
	for f in ind_files:
		if f.split('.')[-1] in ['docx','doc','pdf','txt','html']:
			text_str = re.sub(r'\s+',' ',pdf2txt.convert_Tika(f))
			texts2vec.append(text_str.lower().split(' '))
	model2vec = Word2Vec(texts2vec, min_count=1)
	for word in model2vec.wv.vocab:
		for sim_word, similarity in sorted(model2vec.most_similar(word,topn=200),key=lambda x: abs(float(x[1])),reverse=True)[0]:
			if mycol.find_one({'_id':word}):
				mycol.update_one({'_id':word},{'$set':
					{
						sim_word:similarity
					}
				})
			else:
				mycol.insert_one({
					'_id':word,
					sim_word:similarity
				})

if __name__ == '__main__':
	main(sys.argv[1],sys.argv[2])