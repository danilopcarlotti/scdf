from pdf_to_text import pdf_to_text
from recursive_folders import recursive_folders
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import MultinomialNB
from stopwords_pt import stopwords_pt
import numpy, pandas as pd, nltk, sys, pickle

class mNB_classification_text():
	"""Class to help classify texts with scikit"""
	def __init__(self,dados,target_class=None,classifier_model=False):
		self.dados = dados
		if not classifier_model:
			self.dataframe = self.dataframe_data(target_class = target_class)
			self.count_vectorizer = CountVectorizer(analyzer=self.stemmer)
			self.word_counts = self.count_words()
			self.targets = self.dataframe['class'].values
			self.classifier = self.mNB_classifier()
		else:
			self.dataframe = ''
			self.count_vectorizer = CountVectorizer(analyzer=self.stemmer)
			self.word_counts = self.count_words()
			self.targets = ''
			self.classifier = classifier_model

	def count_words(self):
		word_counts = self.count_vectorizer.fit_transform(self.dataframe['text'].values)
		return word_counts

	def dataframe_data(self, target_class = None):
		# the existence of a "target_class" represents that all other classes should be interpreted as not the target
		rows = []
		index = []
		index_counter = 1
		for text, class_text in self.dados:
			if target_class and class_text != target_class:
				rows.append({'text': text, 'class': 'OTHER'})
				index.append(index_counter)
				index_counter += 1
			else:
				rows.append({'text': text, 'class': class_text})
				index.append(index_counter)
				index_counter += 1
		data_frame = pd.DataFrame(rows, index=index)
		return data_frame

	def mNB_classifier(self):
		classifier = MultinomialNB()
		classifier = classifier.fit(self.word_counts, self.targets)
		return classifier

	def predict_mNB(self,predict_data, as_dict=False):
		example_word_counts = self.count_vectorizer.transform(predict_data)
		predictions = self.classifier.predict(example_word_counts)
		if as_dict:
			predictions_dict = {}
			for index, prediction in numpy.ndenumerate(predictions):
				predictions_dict[predict_data[index[0]]] = prediction
			return predictions_dict
		else:
			return predictions

	def stemmer(self, words):
		analyzer = CountVectorizer().build_analyzer()
		stemmer = nltk.stem.RSLPStemmer()
		stpwrds = stopwords_pt()
		stp = stpwrds.stopwords()
		return (stemmer.stem(w) for w in analyzer(words) if w not in stp)

	def validate_score(self, cv=None, mean=False):
		mNB = MultinomialNB()
		scores = cross_val_score(mNB, self.word_counts, self.targets, cv=cv)
		if mean:
			return numpy.mean(scores)
		return scores

if __name__ == '__main__':
	pdf2txt = pdf_to_text()
	if sys.argv[1] == 'train':
		dados = []
		df = pd.read_csv(sys.argv[2])
		for index, row in df.iterrows():
			dados.append((row['texto'],row['classe']))
		sck = mNB_classification_text(dados)
		modelo = pickle.dump(sck.mNB_classifier(),open(sys.argv[3],'wb'))
	elif sys.argv[1] == 'predict':
		dados = [pdf2txt.convert_Tika(arq) for arq in os.listdir(sys.argv[2])]
		sck = mNB_classification_text('', classifier_model=pickle.load(open(sys.argv[3],'rb')))
		print(sck.predict_mNB(dados))