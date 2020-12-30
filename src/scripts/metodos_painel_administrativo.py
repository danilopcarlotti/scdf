import os

from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient

load_dotenv(find_dotenv())
mongo_url = os.getenv("mongo_url")
myclient = MongoClient(mongo_url)
mydb_master = myclient["SCDF"]
col = mydb_master["investigacoes"]

def usuarios_ativos():
    usuarios = []
    for data in col.find({}):
        usuarios.append(data["id_responsavel"])
    return set(usuarios)

def investigacoes_usuario(id_responsavel):
    investigacoes = []
    for data in col.find({"id_responsavel":id_responsavel}):
        investigacoes.append(data["id_investigacao"])
    return set(investigacoes)

def deletar_investigacao(id_investigacao):
    myclient.db.command("SCDF_" + id_investigacao)
    myclient.db.command("indice_palavras_documentos_" + id_investigacao)
    myclient.db.command("palavras_interesse_" + id_investigacao)
    myclient.db.command("relatorios_indice_arquivos_" + id_investigacao)

def deletar_usuario(id_responsavel):
    for id_investigacao in investigacoes_usuario(id_responsavel):
        deletar_investigacao(id_investigacao)