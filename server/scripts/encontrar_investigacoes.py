import os
import sys

from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from pathlib import Path

PATH_ROOT = Path().absolute().parent.parent
sys.path.append(str(PATH_ROOT))

load_dotenv(find_dotenv())
mongo_url = os.getenv("mongo_url")

def investigacoes_usuario(id_responsavel):
    myclient = MongoClient(mongo_url)
    mydb_master = myclient["SCDF"]
    col = mydb_master["investigacoes"]
    return [i["id_investigacao"] for i in col.find({"id_responsavel":id_responsavel})]