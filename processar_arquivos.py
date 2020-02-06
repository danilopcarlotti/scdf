from index_files import index_files
from parse_emails import parse_emails
from mongo_url import mongo_url
from pymongo import MongoClient
from pdf_to_text import pdf_to_text
from recursive_folders import recursive_folders
from remove_accents import remove_accents
import os, pymongo, sys

def insert_words(texto, file, mycol):
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

def process_files(filepaths, destination_path, id_inv, pdf2txt, mydb, mycol):
    PARSER_EMAILS = parse_emails(filepaths, id_inv, destination_path)
    PARSER_EMAILS.email_to_excel(mydb)
    PARSER_EMAILS.relatorio_geral(mydb)
    i = index_files(filepaths)
    i.save_paths_file(destination_path+'/indice_arquivos_investigacao_'+id_inv, id_inv, mydb=mydb)
    r = recursive_folders()
    paths = r.find_files(filepaths)
    for f in paths:
        try:
            insert_words(pdf2txt.convert_Tika(f),str(f).split('/')[-1],mycol)
        except Exception as e:
            print(e)
    return True

def main(filepaths, destination_path, id_inv):
    pdf2txt = pdf_to_text()
    myclient = MongoClient(mongo_url)
    mydb = myclient["SCDF_"+id_inv]
    mycol = mydb["indice_palavras_documentos_"+id_inv]
    process_files(filepaths,destination_path,id_inv,pdf2txt,mydb,mycol)

if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2],sys.argv[3])