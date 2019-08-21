from recursive_folders import recursive_folders
from topicModelling import topicModelling
from pdf_to_text import pdf_to_text
from stopwords_pt import stopwords_pt
import sys, re

def main(filepaths, id_inv):
	pdf2txt = pdf_to_text()
	top_modelling = topicModelling()
	stpw = stopwords_pt()
	stopwords = stpw.stopwords()
	texts = []
	rec_files = recursive_folders()
	ind_files = rec_files.find_files(filepaths)
	for f in ind_files:
		if f.split('.')[-1] in ['docx','doc','pdf','txt','html']:
			text_str = re.sub(r'\s+',' ',pdf2txt.convert_Tika(f))
			texts.append(text_str)
	model = top_modelling.lda_Model(texts,num_topics=15)
	top_modelling.topic_to_txt(model,prefix=id_inv)

if __name__ == '__main__':
	main(sys.argv[1],sys.argv[2])