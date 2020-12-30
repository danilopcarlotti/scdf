import sys
import base64
import re
import pandas as pd
import subprocess
import networkx as nx
import time
import os
import extract_msg

from docx import Document
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
from pathlib import Path


PATH_ROOT = Path().absolute().parent.parent
sys.path.append(str(PATH_ROOT))


from scdf.src.scripts.recursive_folders import recursive_folders

load_dotenv(find_dotenv())
mongo_url = os.getenv("mongo_url")


class parse_emails:
    """Classe para processamento de emails"""

    def __init__(self, file_list, id_inv, destination_path, save_files=False):
        self.bank_words = ["caixa", "banco", "itaú", "bradesco", "santander"]
        self.save_files = save_files
        self.file_list = file_list
        self.destination_path = destination_path
        self.id_inv = id_inv
        self.nome_relatorio = (
            destination_path
            + "/relatório_emails_investigacao_%s.xlsx" % (str(self.id_inv),)
        )
        pasta_emails = "Emails_{}/".format((id_inv))
        self.nome_pasta = destination_path + "/" + pasta_emails
        subprocess.Popen(
            'mkdir "{}"'.format(self.nome_pasta),
            shell=True,
        )
        self.graph = None
        self.words_of_interest = ["urgente", "comprovante", "extrato", "cuidado"]

    def email_bank_transactions(self, df):
        lista_emails_transacoes = []
        for _, row in df.iterrows():
            try:
                if re.search(
                    r"comprovante.{1,10}transa", row["corpo"], flags=re.I | re.DOTALL
                ):
                    lista_emails_transacoes.append(
                        row["data_envio"] + "_" + row["nome_email"]
                    )
            except Exception as e:
                print(e)
        return lista_emails_transacoes

    def email_contacts(self, df):
        lista_remetentes = list(df["remetente_email"].unique())
        lista_destinatarios = list(df["destinatário_email"].unique())
        if lista_remetentes and lista_destinatarios:
            return lista_remetentes + lista_destinatarios

    def email_names(self, df):
        return list(df["nome_email"].unique())

    def email_subjects(self, df):
        return list(df["assunto_limpo"].unique())

    def email_to_excel(self, mydb):
        rows = []
        for msg in self.file_list:
            (
                body_e,
                date_e,
                from_e,
                recipient_e,
                subject_e,
                subject_e_clean,
                attachments,
            ) = self.parse_msg(msg)
            if body_e != "":
                dicionario_aux = {
                    "nome_email": msg.split("/")[-1][:-4],
                    "corpo": body_e,
                    "data_envio": date_e,
                    "assunto": subject_e,
                    "assunto_limpo": subject_e_clean,
                    "anexos": str(attachments),
                    "remetente_email" : from_e,
                    "destinatário_email" : recipient_e,
                }
                rows.append(dicionario_aux)
        if len(rows):
            df = pd.DataFrame(rows, index=[i for i in range(len(rows))])
            df = df.applymap(
                lambda x: x.encode("unicode-escape", "replace").decode("utf-8")
                if isinstance(x, str)
                else x
            )
            columns = df.columns
            mycol = mydb["relatorios_email_" + self.id_inv]
            for _, row in df.iterrows():
                dic_aux = {column: row[column] for column in columns}
                mycol.insert_one(dic_aux)
            return df

    def email_to_graph(self, df):
        self.graph = nx.DiGraph()
        for _, row in df.iterrows():
            if self.graph.has_edge(row["remetente_email"], row["destinatário_email"]):
                self.graph[row["remetente_email"]][row["destinatário_email"]][
                    "weight"
                ] += 1
                self.graph[row["remetente_email"]][row["destinatário_email"]][
                    "dates"
                ].append(row["data_envio"])
                self.graph[row["remetente_email"]][row["destinatário_email"]][
                    "subjects"
                ].append(row["assunto_limpo"])
            else:
                self.graph.add_edge(
                    row["remetente_email"],
                    row["destinatário_email"],
                    weight=1,
                    dates=[row["data_envio"]],
                    subjects=[row["assunto_limpo"]],
                )

    def email_to_html(self, html_source):
        try:
            arq_html = open(html_source.split("/")[-1].replace(".msg", ".html"), "w")
            arq_html.write(html_source)
            subprocess.Popen(
                'mv "%s" %s'
                % (
                    html_source.split("/")[-1].replace(".msg", ".html"),
                    self.nome_pasta,
                ),
                shell=True,
            )
        except Exception as e:
            print(e)

    def email_to_pdf(self):
        try:
            for f in self.file_list:
                subprocess.Popen(
                    'python3 email2pdf -i "%s" -o "%s" --no-attachments --input-encoding latin_1'
                    % (f, f.split("/")[-1].replace(".msg", ".pdf")),
                    shell=True,
                )
                time.sleep(1)
                subprocess.Popen(
                    'mv "%s" %s'
                    % (
                        f.split("/")[-1].replace(".msg", ".pdf"),
                        self.nome_pasta,
                    ),
                    shell=True,
                )
        except Exception as e:
            print(e)

    def parse_msg(self, msg):
        mail = extract_msg.Message(msg)
        body_e = str(mail.body)
        date_e = str(mail.date)
        from_e = str(mail.sender)
        recipient_e = str(mail.to)
        subject_e = str(mail.subject)
        subject_e_clean = (
            subject_e.replace("Re:", "")
            .replace("Fwd:", "")
            .replace("RE:", "")
            .replace("FWD:", "")
            .replace("FW:", "")
            .replace("Fw:", "")
            .replace("ENC:", "")
            .replace("Enc:", "")
            .strip()
        )
        anexos_nomes = []
        try:
            if len(mail.attachments):
                for att in mail.attachments:
                    anexos_nomes.append(att["filename"])
                    with open(att["filename"], "wb") as f:
                        try:
                            f.write(base64.b64decode(att["payload"]))
                        except:
                            pass
                    subprocess.Popen(
                        'mv "%s" "%s"' % (att["filename"], self.nome_pasta), shell=True
                    )
        except Exception as e:
            print(e)
        return (
            body_e,
            date_e,
            from_e,
            recipient_e,
            subject_e,
            subject_e_clean,
            anexos_nomes,
        )

    def relatorio_entidade(self, df, nome_entidade, nomes_testar):
        colunas_testar = [
            "corpo",
            "destinatário_nome",
            "destinatário_email",
            "remetente_email",
            "assunto_limpo",
            "anexos",
        ]
        rows = []
        for _, row in df.iterrows():
            entidade_encontrada = False
            for col in colunas_testar:
                for nome in nomes_testar:
                    if not entidade_encontrada and re.search(
                        nome.lower(), row[col].lower()
                    ):
                        entidade_encontrada = True
                        dicionario_aux = {
                            "corpo": row["corpo"],
                            "data_envio": row["data_envio"],
                            "destinatário_nome": row["destinatário_nome"],
                            "remetente_nome": row["remetente_nome"],
                            "destinatário_email": row["destinatário_email"],
                            "remetente_email": row["remetente_email"],
                            "assunto": row["assunto"],
                            "assunto_limpo": row["assunto_limpo"],
                            "anexos": row["anexos"],
                        }
                        rows.append(dicionario_aux)
        index = [i for i in range(len(rows))]
        df = pd.DataFrame(rows, index=index)
        df = df.applymap(
            lambda x: x.encode("unicode-escape", "replace").decode("utf-8")
            if isinstance(x, str)
            else x
        )
        df.to_excel(
            self.destination_path + "relatório_" + nome_entidade + ".xlsx", index=False
        )

    def relatorio_geral(self, df, mydb):
        contacts = self.email_contacts(df)
        names_email = self.email_names(df)
        subjects = self.email_subjects(df)
        transactions = self.email_bank_transactions(df)
        text_final = ""
        text_final += "Arquivos de emails disponíveis:\n\n\n"
        for n in names_email:
            text_final += str(n) + "\n"
        text_final += "\n\nAssuntos dos emails:\n\n\n"
        for s in subjects:
            text_final += str(s) + "\n"
        text_final += "\n\nContatos que receberam ou enviaram emails:\n\n\n"
        for c in contacts:
            text_final += str(c) + "\n"
        text_final += (
            "\n\nDatas e nomes dos emails que contém transações bancárias:\n\n\n"
        )
        for t in transactions:
            text_final += str(t) + "\n"
        mycol = mydb["relatorios_geral_emails_" + self.id_inv]
        mycol.insert_one({"relatorio_geral": text_final})

    def text_to_html(self, texto):
        return texto.replace("\t", 4 * "&nbsp;").replace("\n", "<br/>")


def main(file_list, id_inv, destination_path, myclient):
    mydb = myclient["SCDF_" + id_inv]
    p = parse_emails(file_list, id_inv, destination_path)
    df = p.email_to_excel(mydb)
    p.relatorio_geral(df, mydb)


if __name__ == "__main__":
    myclient = MongoClient(mongo_url)
    main(sys.argv[1], sys.argv[2], sys.argv[3], myclient)
