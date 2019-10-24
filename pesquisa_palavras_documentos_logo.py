from pymongo import MongoClient
from pdf_to_text import pdf_to_text
from mongo_url import mongo_url
from docx import Document
from paths_init import *
from functools import reduce

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

import image_logo_mp

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        self.myclient = MongoClient(mongo_url)
        self.mydb = None
        self.pdf2txt = pdf_to_text()
        self.id_investigacao = None

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1165, 604)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 0, 891, 121))
        self.textBrowser.setObjectName("textBrowser")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 160, 271, 41))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 210, 271, 37))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(350, 310, 291, 41))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(350, 360, 291, 51))
        self.pushButton_3.setObjectName("pushButton_3")
        self.listWid = QtWidgets.QListWidget(self.centralwidget)
        self.listWid.setGeometry(QtCore.QRect(670, 160, 481, 381))
        self.listWid.setObjectName("listWid")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 120, 271, 51))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(380, 270, 231, 29))
        self.label_2.setObjectName("label_2")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(910, 0, 241, 121))
        self.textEdit.setObjectName("textEdit")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(350, 420, 291, 61))
        self.pushButton_4.setObjectName("pushButton_4")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 270, 271, 281))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 269, 279))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_6 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 3, 0, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout.addWidget(self.pushButton_7, 2, 0, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout.addWidget(self.pushButton_8, 4, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout.addWidget(self.pushButton_9, 1, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.listWid2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWid2.setGeometry(QtCore.QRect(360, 160, 271, 41))
        self.listWid2.setObjectName("listWid2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(410, 120, 191, 51))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(850, 120, 151, 51))
        self.label_5.setObjectName("label_5")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 250, 631, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionSelecionar_pasta = QtWidgets.QAction(MainWindow)
        self.actionSelecionar_pasta.setObjectName("actionSelecionar_pasta")

        self.pushButton_2.clicked.connect(self.id_inv)
        self.pushButton_3.clicked.connect(self.search_word)
        self.pushButton_4.clicked.connect(self.search_word_vec)
        self.pushButton_6.clicked.connect(self.msg_button_bilhetagem)
        self.pushButton_7.clicked.connect(self.msg_button_topicos)
        self.pushButton_8.clicked.connect(self.msg_button_relatorio_emails)
        self.pushButton_9.clicked.connect(self.msg_button_indice_arquivos)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Garuda\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">Solução em ciência de dados forenses 1.0</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">Ministério Público do Estado de SP</span></p></body></html>"))
        self.pushButton_2.setText(_translate("MainWindow", "Informar ID da investigação"))
        self.pushButton_3.setText(_translate("MainWindow", "Listar documentos com esta(s) palavra(s)\n"
"Gerar relatório"))
        self.label.setText(_translate("MainWindow", "  1º passo. Insira o ID da investigação"))
        self.label_2.setText(_translate("MainWindow", "Digite a palavra a ser pesquisada"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Garuda\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> <img src=\":/newPrefix/MPSPAtivo 5.png\" /></p></body></html>"))
        self.pushButton_4.setText(_translate("MainWindow", "Mostrar outras palavras que aparecem\n"
"em contextos similares"))
        self.pushButton_6.setText(_translate("MainWindow", "Relatório de bilhetagem"))
        self.pushButton_7.setText(_translate("MainWindow", "Relatório de tópicos presentes \n"
"nos documentos"))
        self.pushButton_8.setText(_translate("MainWindow", "Relatório de emails"))
        self.label_3.setText(_translate("MainWindow", "                  Relatórios"))
        self.pushButton_9.setText(_translate("MainWindow", "Índice de documentos\n"
"e emails"))
        self.label_4.setText(_translate("MainWindow", "Você está na investigação"))
        self.label_5.setText(_translate("MainWindow", "Palavras encontradas"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionSelecionar_pasta.setText(_translate("MainWindow", "Selecionar pasta"))
        self.listWid2.addItem('Favor selecionar investigação')

    def search_word(self):
        word = self.lineEdit_2.text().lower()
        self.lineEdit_2.clear()
        mycol = self.mydb["indice_palavras_documentos_"+str(self.id_investigacao)]
        documentos_resultados = []
        for w in word.split(' '):
            doc_res_aux = []
            word_db = mycol.find_one({'_id':word})
            if word_db:
                for doc in word_db['documents']:
                    doc_res_aux.append(doc)
            documentos_resultados.append(doc_res_aux)
        lista_consolidada_documentos = list(reduce(set.intersection, [set(item) for item in documentos_resultados]))
        self.listWid.clear()
        msg = QMessageBox()
        if len(lista_consolidada_documentos):
            documento_relatorio = Document()
            for l in lista_consolidada_documentos:
                self.listWid.addItem(doc)
                documento_relatorio.add_paragraph(doc+'\n')
            documento_relatorio.save(path_relatorios+'documentos com palavras '+word+'.docx')
            msg.about(msg, "Sucesso!", "Foi gerado um relatório, salvo na pasta de relatórios, com os documentos em que a(s) seguinte(s) palavra(s) aparecem: "+word)
        else:
            msg.about(msg, "Erro!", 'Expressão não encontrada')

    def search_word_vec(self):
        self.listWid.clear()
        word = self.lineEdit_2.text().lower()
        self.lineEdit_2.clear()
        mycol = self.mydb["vetores_palavras_similares_"+str(self.id_investigacao)]
        word_db = mycol.find_one({'_id':word})
        if word_db:
            for doc in word_db:
                if doc != '_id':
                    self.listWid.addItem('"'+doc+'" com índice de similaridade '+str(word_db[doc]))

    def id_inv(self):
        self.id_investigacao = self.lineEdit.text()
        self.lineEdit.clear()
        self.mydb = self.myclient["SCDF_"+self.id_investigacao]
        self.listWid2.clear()
        self.listWid2.addItem(self.id_investigacao)
        msg = QMessageBox()
        msg.about(msg, "Sucesso!", "Você selecionou a investigação:\n"+ str(self.id_investigacao))

    def msg_button_bilhetagem(self):
        if self.id_investigacao:
            msg = QMessageBox()
            msg.about(msg, "Sucesso!", "Se solicitado, foram gerados dois arquivos.O primei\
ro deles é um arquivo com extensão '.png'.Este arquivo contém uma visualização de \
quais são os números que fazem e recebem ligações. O segundo arquivo, cujo nome \
é relatório_bilhetagem_..._investigacao_%s.txt contém informações sobre:\n\
1) Círculos de comunicação (números que fazem e recebem ligações entre si;\n\
2) Lista de todos os números que se falam;\n\
3) Quantidade de ligações entre os números;\n" % (str(self.id_investigacao),))
        else:
            msg = QMessageBox()
            msg.about(msg, "Alerta!", "Informe o ID da investigação")

    def msg_button_relatorio_emails(self):
        if self.id_investigacao:
            msg = QMessageBox()
            msg.about(msg, "Sucesso!", "Se havia emails entre os dados disponibilizados, foram \
gerados dois arquivos de relatório. \nO primeiro se denomina relatório_emails_investigacao_%s.xlsx. Este arquivo\
 contém as seguintes colunas:\n\
 1) nome_email: O nome do arquivo;\n\
 2) corpo: O texto do email;\n\
 3) data_envio: A data em que o email foi enviado;\n\
 4) assunto: O assunto ou título do email;\n\
 5) assunto_limpo: O assunto sem pedaços iniciais como 'Re:', 'Fwd:', etc;\n\
 6) anexos: nome dos arquivos em anexo aos emails;\n\n\
 O segundo arquivo se denomina relatório_geral_emails_%s.txt. Este arquivo\
 contém as seguintes informações:\n\
 1) Lista de todos os arquivos de email que foram analisados;\n\
 2) Assunto dos emails;\n\
 3) Contatos que receberam ou enviaram emails;\n\
 4) Datas e nomes dos emails que contém transações bancárias;\n\n\
 Há um terceiro grupo de imagens que foi gerado. Cada imagem desta representa um tópico importante \
 nos textos dos emails. Cada tópico é um conjunto de palavras encontrado pelo modelo matemático. \
 Todos os arquivos têm a denominação wordcloud_topicos_investigacao_%s_topico_....png" \
 % (str(self.id_investigacao),str(self.id_investigacao),str(self.id_investigacao)))
        else:
            msg = QMessageBox()
            msg.about(msg, "Alerta!", "Informe o ID da investigação")

    def msg_button_topicos(self):
        if self.id_investigacao:
            msg = QMessageBox()
            msg.about(msg, "Sucesso!", "Foram gerados quinze arquivos. Todos eles se denominam\
investigacao_%s_wordcloud_....png. Cada imagem desta representa um tópico importante \
nos textos dos emails. Cada tópico é um conjunto de palavras encontrado \
pelo modelo matemático." % (str(self.id_investigacao),))
        else:
            msg = QMessageBox()
            msg.about(msg, "Alerta!", "Informe o ID da investigação")

    def msg_button_indice_arquivos(self):
        if self.id_investigacao:
            msg = QMessageBox()
            msg.about(msg, "Sucesso!", "Foi gerado um arquivo de Excel denominado indexação_arquivos_%s.xlsx\
 Esse arquivo contém as seguintes colunas:\n\n\
1) 'NOME_ARQUIVO': o nome do arquivo. Este é o nome que deve ser usado para que o usuário possa encontrar o arquivo \
desejado em sua máquina;\n\
2) 'TIPO_ARQUIVO': A extensão do arquivo;\n\
Con estas informações o usuário pode pesquisar pelo nome do arquivo e também pelo tipo de extensão.\
" % (str(self.id_investigacao),))
        else:
            msg = QMessageBox()
            msg.about(msg, "Alerta!", "Informe o ID da investigação")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
