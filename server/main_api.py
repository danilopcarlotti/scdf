import os
import sys

from dotenv import load_dotenv, find_dotenv
from pathlib import Path

from fastapi import (
    FastAPI,
    Request,
    Form,
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse

PATH_ROOT = Path().absolute().parent.parent
sys.path.append(str(PATH_ROOT))


from scdf.server.scripts.encontrar_investigacoes import investigacoes_usuario
from scdf.server.scripts.gerar_relatorios import gerar_relatorios
from scdf.server.scripts.pesquisa_palavra_web import save_file

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

load_dotenv(find_dotenv())
mongo_url = os.getenv("mongo_url")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/{id_responsavel}", response_class=HTMLResponse)
def select_investigation(request: Request, id_responsavel: str):
    lista_investigacoes = investigacoes_usuario(id_responsavel)
    return templates.TemplateResponse(
        "selecionar_inv.html",
        {
            "request": request,
            "lista_investigacoes": lista_investigacoes,
            "id_responsavel": id_responsavel,
        },
    )


@app.post("/relatorios")
def relatorios(request: Request, id_responsavel: str = Form(...), id_inv: str = Form(...)):
    gerar_relatorios(id_responsavel, id_inv)
    links_download = [
        "relatório_emails_investigacao_{}_{}.xlsx".format(id_responsavel, id_inv),
        "relatório_geral_emails_{}_{}.docx".format(id_responsavel, id_inv),
        "indexação_arquivos_{}_{}.xlsx".format(id_responsavel, id_inv),
    ]
    return templates.TemplateResponse(
        "dados_inv.html",
        {"request": request, "id_inv": id_inv, "links_download": links_download},
    )


@app.post("/download")
def download(filename: str = Form(...)):
    return FileResponse(
        str(PATH_ROOT) + "scdf/server/files/" + filename,
        media_type="application/octet-stream",
        filename=filename,
    )

@app.get("/{id_inv}/pesquisar")
def pesquisa(request: Request, id_inv : str):
    return templates.TemplateResponse(
        "pesquisar.html",
        {"request": request, "id_inv":id_inv},
    )

@app.post("/download_pesquisa")
def download_pesquisa(id_inv: str = Form(...), word: str = Form(...)):
    path = str(PATH_ROOT) + "scdf/server/files/investigacao_{}_palavra_{}.docx".format(id_inv, word)
    save_file(word, id_inv, path)
    return FileResponse(
        path,
        media_type="application/octet-stream",
        filename=word+".docx",
    )