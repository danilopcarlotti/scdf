import re
import sys
import os
import subprocess
import uuid

from glob import glob
from zipfile import ZipFile
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from pathlib import Path


PATH_ROOT = Path().absolute().parent.parent
sys.path.append(str(PATH_ROOT))

from scdf.src.scripts.bilhetagem import processar_interceptacao_telefonica
from scdf.src.scripts.index_files import index_files
from scdf.src.scripts.parse_emails import parse_emails
from scdf.src.scripts.tika_textos import tika_textos
from scdf.src.scripts.processar_arquivos import insert_words

TIKA_CLASS = tika_textos()
load_dotenv(find_dotenv())
mongo_url = os.getenv("mongo_url")


def inserir_investigacao(id_inv, id_responsavel, myclient):
    mydb_master = myclient["SCDF"]
    col = mydb_master["investigacoes"]
    inv = col.find_one(
        {
            "id_investigacao": id_inv,
            "id_responsavel": id_responsavel,
        }
    )
    if not inv:
        col.insert_one(
            {
                "id_investigacao": id_inv,
                "id_responsavel": id_responsavel,
            }
        )


def indice_arquivos(filepaths, id_inv, path_inicial, mydb):
    i = index_files(filepaths)
    i.save_paths_file(
        path_inicial + "indice_arquivos_investigacao_" + str(id_inv),
        id_inv,
        list_paths=filepaths,
        csv_file=True,
        mydb=mydb,
    )


def processar_arquivo_texto(filepaths, mydb):
    mascaras = {
        "RG": r"\d{1,2}\.\d{6}\-\w|\d{1,2}\.\d{3}\.\d{3}\-\w",
        "CPF": r"\d{3}\.\d{3}\.\d{3}\-\d{2}",
        "Email": r"[^@]+@[^@]+\.[^@\s\.]+",
        "Telefone": r"[\s\.\,]\d{8,9}[\s\.\,]|[\s\.\,]\d{4,5}[\-\.\s]\d{4}[\s\.\,]",
        "Data": r"\d{2}[\./\\]\d{2}[\./\\]\d{4}",
    }
    mycol = mydb["indice_palavras_documentos_" + id_inv]
    col_palavras_interesse = mydb["palavras_interesse_" + id_inv]
    for filepath in filepaths:
        if filepath[-4:] == "docx" or filepath[-3:] == "pdf" or filepath[-3:] == "doc":
            try:
                texto = TIKA_CLASS.process_file(filepath)
                insert_words(texto, filepath, mycol)
                for nome_r, reg in mascaras.items():
                    lista_regex = re.findall(reg, texto)
                    for l in lista_regex:
                        col_palavras_interesse.insert_one(
                            {
                                "arquivo": filepath,
                                "tipo_expressão": nome_r,
                                "resultado_encontrado": l,
                            }
                        )
            except Exception as e:
                print("Erro {} em processar arquivo ".format(e), filepath)


def processar_emails(file_list, id_inv, destination_path, myclient):
    if len(file_list) > 0:
        PARSER_EMAILS = parse_emails(file_list, id_inv, destination_path, myclient)
        df = PARSER_EMAILS.email_to_excel(myclient["SCDF_" + id_inv])
        PARSER_EMAILS.relatorio_geral(df, myclient["SCDF_" + id_inv])


def unzip_files(filepaths):
    for file in filepaths:
        with ZipFile(file, "r") as zip_ref:
            zip_ref.extractall("/".join(file.split("/")[:-1]))


# def vetorizacao_textos(filepath, path_inicial):
#     df = pd.read_csv(filepath)
#     paths = []
#     for _, row in df.iterrows():
#         if row["TIPO_ARQUIVO"] == "txt":
#             paths.append(row["PATH_ARQUIVO"])
#     if len(paths):
#         w = word2vec_textos()
#         w.create_model(
#             filepath=path_inicial + "word2vec_model.bin", path_multiple=paths
#         )


if __name__ == "__main__":

    path_inicial = sys.argv[1]
    id_responsavel = sys.argv[2]
    id_inv = sys.argv[3]
    if id_inv == 0:
        id_inv = str(uuid.uuid4()).split("-")[0]

    myclient = MongoClient(mongo_url)
    mydb = myclient["SCDF_" + id_inv]

    print("Id da investigação registrado: ", id_inv)
    inserir_investigacao(id_inv, id_responsavel, myclient)
    arq_bilhetagem = None
    col_a_bil = None
    col_b_bil = None
    if len(sys.argv) > 4:
        arq_bilhetagem = sys.argv[4]
        if len(sys.argv) == 7:
            col_a_bil = sys.argv[5]
            col_b_bil = sys.argv[6]

    # print("Descompactando os arquivos")
    # arquivos_descompactar = [
    #     f for f in glob(path_inicial, recursive=True) if f[-3:] == "zip"
    # ]
    # unzip_files(arquivos_descompactar)

    list_files = glob(path_inicial, recursive=True)

    # PROCESSAR EMAILS
    print("Processando os emails e gerando relatório")
    processar_emails(
        [i for i in list_files if i[-3:] == "msg"], id_inv, path_inicial, myclient
    )

    # PROCESSAR OS PDF'S E ARQUIVOS DE WORD
    print("Processando os arquivos de texto")
    processar_arquivo_texto(
        list_files,
        mydb,
    )
    indice_arquivos(list_files, id_inv, path_inicial, mydb)

    # # VETORIZAÇÃO
    # vetorizacao_textos(path_inicial+'indice_arquivos_investigacao_'+str(id_inv)+'.csv',path_inicial)

    # PROCESSAR BILHETAGENS E GERAR RELATÓRIO
    if arq_bilhetagem:
        print("Processando arquivo de bilhetagem")
        if col_a_bil:
            processar_interceptacao_telefonica(
                arq_bilhetagem,
                id_inv,
                path_inicial,
                colunaOrig=col_a_bil,
                colunaDest=col_b_bil,
            )
        else:
            processar_interceptacao_telefonica(
                arq_bilhetagem,
                id_inv,
                path_inicial,
                colunaOrig="Origem/IMEI",
                colunaDest="Destino/IMEI",
            )
