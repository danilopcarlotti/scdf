import sys
import docx
import os

from dotenv import load_dotenv, find_dotenv
from functools import reduce
from pymongo import MongoClient

from pathlib import Path

PATH_ROOT = Path().absolute().parent.parent
sys.path.append(str(PATH_ROOT))

from scdf.src.scripts.remove_accents import remove_accents

load_dotenv(find_dotenv())
mongo_url = os.getenv("mongo_url")

myclient = MongoClient("mongodb://localhost:27017/")


def search_word(word, id_investigacao):
    mydb = myclient["SCDF_" + id_investigacao]
    mycol = mydb["indice_palavras_documentos_" + id_investigacao]
    word = remove_accents(word).lower()
    documentos_resultados = []
    for w in word.split(" "):
        doc_res_aux = []
        word_db = mycol.find_one({"_id": w})
        if word_db:
            for doc in word_db["documents"]:
                doc_res_aux.append(doc)
        documentos_resultados.append(doc_res_aux)
    lista_consolidada_documentos = list(
        reduce(set.intersection, [set(item) for item in documentos_resultados])
    )
    if len(lista_consolidada_documentos):
        texto = "\n\n\t1) Documentos em que a expressão " + word + " se encontra:\n\n\n"
        for l in lista_consolidada_documentos:
            texto += "\t" + l.split("/")[-1] + "\n"
        return texto
    else:
        return "Expressão não encontrada\n\n"


def save_file(word, id_investigacao, path):
    texto = search_word(word, id_investigacao)
    doc = docx.Document()
    doc.add_paragraph(texto)
    doc.save(path)
