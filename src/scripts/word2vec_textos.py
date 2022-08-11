from bs4 import BeautifulSoup
from gensim.models import Word2Vec
from inverse_index import inverse_index
from matplotlib import pyplot
import re, sys, pandas as pd


class word2vec_textos:
    def __init__(self):
        self.modelo = None

    def text_from_html_file(self, filepath):
        f = open(filepath, "r")
        webpage = f.read()
        soup = BeautifulSoup(webpage, "html.parser")
        for script in soup(["script", "style"]):
            script.extract()
        return soup.get_text()

    def create_model(
        self, path_texto=None, path_multiple=None, filepath="word2vec_model.bin"
    ):
        if path_multiple:
            sentences = []
            for p in path_multiple:
                sentences += [str(p).lower().split()]
        else:
            sentences = [str(path_texto).lower().split()]
        model = Word2Vec(sentences, min_count=1, size=150)
        model.save(filepath)

    def load_model(self, filepath="word2vec_model.bin"):
        self.modelo = Word2Vec.load(filepath)

    def pesquisar_palavra(self, palavra, filepath="word2vec_model.bin", topn=30):
        self.load_model(filepath=filepath)
        return sorted(
            self.modelo.most_similar(palavra, topn=topn),
            key=lambda x: abs(float(x[1])),
            reverse=True,
        )


def main():
    pass


if __name__ == "__main__":
    w = word2vec_textos()
    print(w.pesquisar_palavra(sys.argv[1]))
