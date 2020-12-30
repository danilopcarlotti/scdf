# SCDF
Solução em Ciência de dados Forense

É necessário instalar:

i) Python >= 3.5
ii) MongoDB
iii) `pip install -r requirements.txt`

O endereço de conexão com o banco de dados fica armazenado no arquivo `.env`, na raiz e que deve ser alterado conforme a necessidade.

## DIVISÃO DA FERRAMENTA EM MÓDULOS

#### Módulo de upload de investigações

- Para fazer upload de uma investigação é necessário gerar id para o investigador e a investigação. Em seguida, rodar o comando:
`cd scdf/src`
`python upload_investigacao.py [PATH DOS DADOS] [ID INVESTIGADOR] [ID INVESTIGACAO]`

#### Módulo de servidor web para acesso às investigações
- Para rodar o servidor do SCDF na porta 8000
`cd scdf/server`
`uvicorn main_api:app`

#### Módulo de administração
- Para verificar usuário, investigações e deletar o que for necessário com o jupyter notebook
`cd scdf/src`
`jupyter lab`