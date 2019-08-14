from index_files import index_files
from topicModelling import topicModelling
from pdf_to_text import pdf_to_text
from word2vec_textos import word2vec_textos
from gensim.models import Word2Vec
from stopwords_pt import stopwords_pt

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

import os, pickle, pandas as pd, re

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(851, 561)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 811, 91))
        self.textBrowser.setObjectName("textBrowser")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 140, 261, 41))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 190, 261, 37))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 310, 271, 41))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 360, 271, 37))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 100, 311, 41))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 280, 311, 29))
        self.label_2.setObjectName("label_2")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(470, 140, 261, 37))
        self.pushButton_4.setObjectName("pushButton_4")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(400, 100, 421, 41))
        self.label_3.setObjectName("label_3")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(400, 240, 431, 261))
        self.listWidget.setObjectName("listWidget")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(430, 200, 381, 29))
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionSelecionar_pasta = QtWidgets.QAction(MainWindow)
        self.actionSelecionar_pasta.setObjectName("actionSelecionar_pasta")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.id_investigacao = 'nao_informado'
        self.pushButton_2.clicked.connect(self.id_inv)
        self.pushButton_3.clicked.connect(self.search_word)
        self.pushButton_4.clicked.connect(self.top_mod)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Garuda\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Este é o programa para geração de relatório usando Machine Learning sobre termos que aparecem nos documentos</span></p></body></html>"))
        self.pushButton_2.setText(_translate("MainWindow", "Informe o ID da investigação"))
        self.pushButton_3.setText(_translate("MainWindow", "Exibir outras palavras semelhantes"))
        self.label.setText(_translate("MainWindow", "1º passo - Insira abaixo o ID da investigação"))
        self.label_2.setText(_translate("MainWindow", "3º passo - Digite a palavra a ser pesquisada"))
        self.pushButton_4.setText(_translate("MainWindow", "Gerar relatório de tópicos dos textos"))
        self.label_3.setText(_translate("MainWindow", "2º passo - Clique para gerar relatório dos tópicos dos textos"))
        self.label_4.setText(_translate("MainWindow", "Estas são as palavras mais similares ao que pesquisou"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionSelecionar_pasta.setText(_translate("MainWindow", "Selecionar pasta"))

    def id_inv(self):
        self.id_investigacao = self.lineEdit.text()
        self.lineEdit.clear()
        self.dicionario_indice_arquivos = pickle.load(open('dicionario_indice_arquivos_%s.pickle' % self.id_investigacao,'rb'))
        try:
            self.model2vec = Word2Vec.load('word2vec_model_%s.bin' % (self.id_investigacao,))
        except:
            self.model2vec = None
        msg = QMessageBox()
        msg.about(msg, "Sucesso!", "Você selecionou a investigação:\n"+ str(self.id_investigacao))

    def top_mod(self):
        pdf2txt = pdf_to_text()
        top_modelling = topicModelling()
        stpw = stopwords_pt()
        stopwords = stpw.stopwords()
        df = pd.read_excel('indice_arquivos_investigacao_'+self.id_investigacao+'.xlsx')
        texts = []
        texts2vec = []
        for index, row in df.iterrows():
            if row['TIPO_ARQUIVO'] in ['docx','doc','pdf','txt']:
                text_str = re.sub(r'\s+',' ',pdf2txt.convert_Tika(row['PATH_ARQUIVO']))
                texts.append(text_str)
                texts2vec.append(text_str.lower().split(' '))
        model = top_modelling.lda_Model(texts)
        top_modelling.topic_to_txt(model)
        self.model2vec = Word2Vec(texts2vec, min_count=1, size=150)
        self.model2vec.save('word2vec_model_%s.bin' % (self.id_investigacao,))
        msg = QMessageBox()
        msg.about(msg, "Sucesso!", "Você processou os textos da investigação:\n"+ str(self.id_investigacao))

    def search_word(self):
        self.listWidget.clear()
        word = self.lineEdit_2.text().lower()
        self.lineEdit_2.clear()
        lista_palavras = sorted(self.model2vec.most_similar(word,topn=20),key=lambda x: abs(float(x[1])),reverse=True)
        for w,n in lista_palavras:
            self.listWidget.addItem('"'+w+'" pontua '+"{0:.2f}".format(n)+'% em similaridade')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
