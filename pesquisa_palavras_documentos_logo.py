from pymongo import MongoClient
from pdf_to_text import pdf_to_text
from mongo_url import mongo_url

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

import image_logo

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
        self.textBrowser.setGeometry(QtCore.QRect(10, 0, 931, 101))
        self.textBrowser.setObjectName("textBrowser")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 150, 271, 41))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 200, 271, 37))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(360, 160, 271, 41))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(360, 210, 271, 37))
        self.pushButton_3.setObjectName("pushButton_3")
        self.listWid = QtWidgets.QListWidget(self.centralwidget)
        self.listWid.setGeometry(QtCore.QRect(660, 110, 491, 411))
        self.listWid.setObjectName("listWid")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 100, 271, 51))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(380, 120, 231, 29))
        self.label_2.setObjectName("label_2")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(960, 0, 181, 101))
        self.textEdit.setObjectName("textEdit")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(360, 260, 271, 61))
        self.pushButton_4.setObjectName("pushButton_4")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 250, 271, 281))
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

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Garuda\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Solução em ciência de dados forenses 1.0</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Unidade de Inteligência - Ministério Público do Estado de SP</span></p></body></html>"))
        self.pushButton_2.setText(_translate("MainWindow", "Informar ID da investigação"))
        self.pushButton_3.setText(_translate("MainWindow", "Mostrar documentos com esta palavra"))
        self.label.setText(_translate("MainWindow", "  1º passo. Insira o ID da investigação"))
        self.label_2.setText(_translate("MainWindow", "Digite a palavra a ser pesquisada"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Garuda\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> <img src=\":/newPrefix/MPSP.png\" width=\"160\" height=\"80\" /></p></body></html>"))
        self.pushButton_4.setText(_translate("MainWindow", "Mostrar outras palavras que aparecem\n"
"em contextos similares"))
        self.pushButton_6.setText(_translate("MainWindow", "Relatório de bilhetagem"))
        self.pushButton_7.setText(_translate("MainWindow", "Relatório de tópicos presentes \n"
"nos documentos"))
        self.pushButton_8.setText(_translate("MainWindow", "Relatório de emails"))
        self.label_3.setText(_translate("MainWindow", "                  Relatórios"))
        self.pushButton_9.setText(_translate("MainWindow", "Índice de documentos\n"
"e emails"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionSelecionar_pasta.setText(_translate("MainWindow", "Selecionar pasta"))

    def search_word(self):
        self.listWid.clear()
        word = self.lineEdit_2.text().lower()
        self.lineEdit_2.clear()
        mycol = self.mydb["indice_palavras_documentos_"+str(self.id_investigacao)]
        word_db = mycol.find_one({'_id':word})
        if word_db:
            for doc in word_db['documents']:
                self.listWid.addItem(self.dicionario_indice_arquivos[index])

    def search_word_vec(self):
        self.listWid.clear()
        word = self.lineEdit_2.text().lower()
        self.lineEdit_2.clear()
        mycol = self.mydb["vetores_palavras_similares_"+str(self.id_investigacao)]
        word_db = mycol.find_one({'_id':word})
        if word_db:
            for doc in word_db['documents']:
                self.listWid.addItem(self.dicionario_indice_arquivos[index])

    def id_inv(self):
        self.id_investigacao = self.lineEdit.text()
        self.lineEdit.clear()
        self.mydb = self.myclient["SCDF_"+self.id_investigacao]
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
