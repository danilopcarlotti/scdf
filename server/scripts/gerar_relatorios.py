import os
import re
import sys
import pandas as pd
import pymongo

from dotenv import load_dotenv, find_dotenv
from pathlib import Path

from docx import Document

PATH_ROOT = Path().absolute().parent.parent
sys.path.append(str(PATH_ROOT))

load_dotenv(find_dotenv())
mongo_url = os.getenv("mongo_url")


def gerar_relatorios(
    id_responsavel, id_inv, destination_path=str(PATH_ROOT / "/scdf/server/files")
):
    # checar se já estão criados os arquivos da investigação
    relatorio_emails_xlsx = False
    relatorio_geral_emails = False
    relatorios_indice_arquivos = False
    for f in os.listdir(destination_path):
        if not relatorio_emails_xlsx and re.search(
            r"relatório_emails_investigacao_{}_{}.xlsx".format(id_responsavel, id_inv),
            f,
        ):
            relatorio_emails_xlsx = True
        if not relatorio_geral_emails and re.search(
            r"relatório_geral_emails_{}_{}.docx".format(id_responsavel, id_inv), f
        ):
            relatorio_geral_emails = True
        if not relatorios_indice_arquivos and re.search(
            r"indexação_arquivos_{}_{}.xlsx".format(id_responsavel, id_inv), f
        ):
            relatorios_indice_arquivos = True

    myclient = pymongo.MongoClient(mongo_url)
    mydb = myclient["SCDF_" + id_inv]

    # RELATÓRIOS DE EMAILS
    if not relatorio_emails_xlsx:
        mycol_emails = mydb["relatorios_email_" + id_inv]
        rows_emails = []
        for d in mycol_emails.find({}):
            dic_aux = d.copy()
            del dic_aux["_id"]
            rows_emails.append(dic_aux)
        df_emails = pd.DataFrame(
            rows_emails, index=[i for i in range(len(rows_emails))]
        )
        df_emails.to_excel(
            destination_path
            + "/relatório_emails_investigacao_{}_{}.xlsx".format(
                id_responsavel, id_inv
            ),
            index=False,
        )

    if not relatorio_geral_emails:
        mycol_geral_emails = mydb["relatorios_geral_emails_" + id_inv]
        relatorio_geral_emails = ""
        for d in mycol_geral_emails.find({}):
            relatorio_geral_emails = d["relatorio_geral"]
            break
        doc = Document()
        doc.add_paragraph(relatorio_geral_emails)
        doc.save(
            destination_path
            + "/relatório_geral_emails_{}_{}.docx".format(id_responsavel, id_inv)
        )

    # ÍNDICE DE ARQUIVOS
    if not relatorios_indice_arquivos:
        mycol_indice_arquivos = mydb["relatorios_indice_arquivos_" + id_inv]
        rows_indice_arquivos = []
        for d in mycol_indice_arquivos.find({}):
            dic_aux = d.copy()
            del d["_id"]
            rows_indice_arquivos.append(dic_aux)
        df_indice_arquivos = pd.DataFrame(rows_indice_arquivos)
        df_indice_arquivos.to_excel(
            destination_path
            + "/indexação_arquivos_{}_{}.xlsx".format(
                id_responsavel, id_inv, index=False
            ),
            index=False,
        )


if __name__ == "__main__":
    gerar_relatorios(str(sys.argv[1]), str(sys.argv[2]))
