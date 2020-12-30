import os
import sys
import pandas as pd

from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from pymongo import MongoClient

PATH_ROOT = Path().absolute().parent.parent
sys.path.append(str(PATH_ROOT))


from scdf.src.scripts.recursive_folders import recursive_folders

load_dotenv(find_dotenv())
mongo_url = os.getenv("mongo_url")


class index_files:
    def __init__(self, files_path):
        self.files_path = files_path
        self.recursive = recursive_folders()

    def file_type(self, file_name):
        if "/" in file_name:
            file_name = file_name.split("/")[-1].split(".")[-1]
        else:
            file_name = file_name.split(".")[-1]
        return file_name

    def list_paths_df(self, paths):
        rows = []
        contador = 1
        for path in paths:
            if "/" in path:
                nome = path.split("/")[-1]
            else:
                nome = path
            rows.append({"NOME_ARQUIVO": nome, "TIPO_ARQUIVO": self.file_type(path)})
            contador += 1
        data_frame = pd.DataFrame(rows, index=[i for i in range(len(rows))])
        return data_frame

    def paths_df(self):
        paths = self.recursive.find_files(self.files_path)
        rows = []
        contador = 1
        for path in paths:
            if "/" in path:
                nome = path.split("/")[-1]
            else:
                nome = path
            rows.append({"NOME_ARQUIVO": nome, "TIPO_ARQUIVO": self.file_type(path)})
            contador += 1
        data_frame = pd.DataFrame(rows, index=[i for i in range(len(rows))])
        return data_frame

    def save_paths_file(
        self,
        name_file,
        id_inv,
        mydb=None,
        list_paths=False,
        save_file=False,
        csv_file=False,
        excel_file=False,
    ):
        if list_paths:
            df = self.list_paths_df(list_paths)
        else:
            df = self.paths_df()
        if save_file:
            if csv_file:
                df.to_csv(name_file + ".csv", index=False)
            elif excel_file:
                df.to_excel(name_file + ".xlsx", index=False)
        else:
            mycol = mydb["relatorios_indice_arquivos_" + id_inv]
            for _, row in df.iterrows():
                dic_aux = {c: row[c] for c in df.columns}
                mycol.insert_one(dic_aux)


def main(files_path, id_inv):
    myclient = MongoClient(mongo_url)
    mydb = myclient["SCDF_" + id_inv]
    i = index_files(files_path)
    i.save_paths_file("indexação_arquivos_%s" % (str(id_inv),), id_inv, mydb=mydb)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
