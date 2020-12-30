import sys
from pathlib import Path

PATH_ROOT = Path().absolute().parent.parent
sys.path.append(str(PATH_ROOT))

from scdf.src.scripts.remove_accents import remove_accents


def insert_words(texto, file, mycol):
    texto = remove_accents(texto).lower()
    palavras = list(
        set(
            [
                w
                for w in texto.split()
                if (len(w) > 3 and not w.isdigit())
            ]
        )
    )
    for p in palavras:
        try:
            if mycol.find_one({"_id": p}):
                mycol.update_one({"_id": p}, {"$push": {"documents": file}})
            else:
                mycol.insert_one({"_id": p, "documents": [file]})
        except:
            pass
    return True
