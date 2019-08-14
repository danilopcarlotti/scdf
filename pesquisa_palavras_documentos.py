from index_files import index_files
from parse_emails import parse_emails
from pymongo import MongoClient
from remove_accents import remove_accents
from pdf_to_text import pdf_to_text

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

import os, pickle, pymongo

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.myclient = MongoClient('mongodb://localhost:27017/')
        self.pdf2txt = pdf_to_text()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(888, 597)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(9, 9, 861, 91))
        self.textBrowser.setObjectName("textBrowser")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 140, 261, 41))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 190, 261, 37))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 410, 271, 41))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 460, 271, 37))
        self.pushButton_3.setObjectName("pushButton_3")
        self.listWid = QtWidgets.QListWidget(self.centralwidget)
        self.listWid.setGeometry(QtCore.QRect(380, 110, 491, 411))
        self.listWid.setObjectName("listWid")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 100, 311, 41))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 370, 311, 29))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 310, 311, 37))
        self.pushButton.setObjectName("pushButton")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 240, 321, 71))
        font = QtGui.QFont()
        font.setItalic(False)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
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
        self.pushButton.clicked.connect(self.process_files)
        self.pushButton_2.clicked.connect(self.id_inv)
        self.pushButton_3.clicked.connect(self.search_word)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "1º Módulo - processamento e pesquisa nos textos"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Garuda\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Este é o programa que irá processar todos os arquivos e prepará-los para pesquisa por palavras-chave</span></p></body></html>"))
        self.pushButton_2.setText(_translate("MainWindow", "Informar ID da investigação"))
        self.pushButton_3.setText(_translate("MainWindow", "Mostrar documentos com esta palavra"))
        self.label.setText(_translate("MainWindow", "1º passo - Insira abaixo o ID da investigação"))
        self.label_2.setText(_translate("MainWindow", "3º passo - Digite a palavra a ser pesquisada"))
        self.pushButton.setText(_translate("MainWindow", "Selecione pasta de arquivos da investigação"))
        self.label_3.setText(_translate("MainWindow", "2º passo - Processar arquivos da investigação\n"
"Passo que deve ser feito só uma vez"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionSelecionar_pasta.setText(_translate("MainWindow", "Selecionar pasta"))

    def search_word(self):
        self.listWid.clear()
        word = self.lineEdit_2.text().lower()
        self.lineEdit_2.clear()
        mydb = self.myclient["SCDF"]
        mycol = mydb["indice_palavras_documentos"]
        # id_inv = str(self.id_investigacao)
        # if word in self.dicionario_indice_palavras:
        #     for index in self.dicionario_indice_palavras[word]:
        #         self.listWid.addItem(self.dicionario_indice_arquivos[index])
        word_db = mycol.find_one({'_id':word})
        if word_db:
            for doc in word_db['documents']:
                self.listWid.addItem(self.dicionario_indice_arquivos[index])

    def insert_words(self, texto, file):
        palavras = list(set([remove_accents(w.strip()).lower() for w in texto.split() if (len(w) > 3 and not w.isnumeric())]))
        for p in palavras:
            try:
                if mycol.find_one({'_id':p}):
                    mycol.update_one({'_id':p},{'$push':
                        {
                            'documents':file
                        }
                    })
                else:
                    mycol.insert_one({
                        '_id':p,
                        'documents':[file]
                    })
            except:
                pass
        return True

    def process_files(self):
        mydb = self.myclient["SCDF"]
        mycol = mydb["indice_palavras_documentos"]
        id_inv = str(self.id_investigacao)
        filepath_class = QtWidgets.QFileDialog()
        filepaths = filepath_class.getExistingDirectory(filepath_class, "Select Directory")
        PARSER_EMAILS = parse_emails(filepaths, id_inv)
        PARSER_EMAILS.email_to_excel()
        PARSER_EMAILS.relatorio_geral()
        i = index_files(filepaths)
        # i.save_paths_file('indice_arquivos_investigacao_'+id_inv, id_inv, excel_file=True)
        # self.dicionario_indice_arquivos = pickle.load(open('dicionario_indice_arquivos_%s.pickle' % id_inv,'rb'))
        # self.dicionario_indice_palavras = pickle.load(open('dicionario_indice_palavras_%s.pickle' % id_inv,'rb'))
        for f in i:
            try:
                self.insert_words(self.pdf2txt.convert_Tika(open(f,'r')),f)
            except:
                pass
        msg = QMessageBox()
        msg.about(msg, "Sucesso!", "Você processou os arquivos da investigação:\n"+ str(self.id_investigacao))

    def id_inv(self):
        self.id_investigacao = self.lineEdit.text()
        self.lineEdit.clear()
        try:
            self.dicionario_indice_arquivos = pickle.load(open('dicionario_indice_arquivos_%s.pickle' % self.id_investigacao,'rb'))
            self.dicionario_indice_palavras = pickle.load(open('dicionario_indice_palavras_%s.pickle' % self.id_investigacao,'rb'))
        except:
            self.dicionario_indice_arquivos = None
            self.dicionario_indice_palavras = None
        msg = QMessageBox()
        msg.about(msg, "Sucesso!", "Você selecionou a investigação:\n"+ str(self.id_investigacao))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
