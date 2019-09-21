from recursive_folders import recursive_folders
from topicModelling import topicModelling
from pdf_to_text import pdf_to_text
from stopwords_pt import stopwords_pt
import sys, re

def main(filepaths, id_inv, destination_path, num_topics=15):
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
	model = top_modelling.lda_Model(texts,num_topics=num_topics)
	top_modelling.topic_to_txt(model,prefix=destination_path+'investigacao_'+id_inv+'_')

if __name__ == '__main__':
	main(sys.argv[1],sys.argv[2],sys.argv[3],num_topics=15)