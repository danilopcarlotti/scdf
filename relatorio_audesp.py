import pymongo, pandas as pd, pickle, os, re
from docx import Document

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['Audesp']
entidades = mydb['entidades']
licitacoes = mydb['licitacoes']
licitantes = mydb['licitantes']
path_relatorios = ''

def consertar_str_cnpj(cnpj):
    cnpj = cnpj.replace('/','').replace('-','').replace('.','')
    if len(cnpj) == 14:
        return cnpj
    elif len(cnpj) > 14:
        return consertar_str_cnpj(cnpj[:-1])
    else:
        return consertar_str_cnpj('0'+cnpj)

def dados_entidade(id_entidade):
	dic_ent = entidades.find_one({'_id':id_entidade})
	if dic_ent:
		dic_aux = {'nome_completo':dic_ent['nome_completo']}
		municipio = dados_municipio(dic_ent['municipio_id'])
		return [dic_aux,municipio]
	return False

def dados_licitantes(cnpj_licitante):
	dic_licitantes = licitantes.find_one({'_id':cnpj_licitante})
	if dic_licitantes:
		dic_aux = {}
		colunas_interesse = ['cpf_adm','nome_licitante','licitacao_id']
		for c in colunas_interesse:
			dic_aux[c] = dic_licitantes[c]
		return dic_aux
	return False

def dados_municipio(id_municipio):
	return False

def dados_licitacao(id_licitacao):
	dic_licitacao = licitacoes.find_one({'_id':id_licitacao})
	if dic_licitacao:
		dic_aux = {}
		colunas_interesse = ['ano_licitacao','descricao_objeto','valor_total']
		for c in colunas_interesse:
			dic_aux[c] = dic_licitacao[c]
		entidade = dados_entidade(dic_licitacao['entidade_id'])
		return [id_licitacao,dic_aux,entidade]
	return False

def relatorio_geral(cnpj_licitante):
	dados_licitante = dados_licitantes(cnpj_licitante)
	if not dados_licitante:
		document = Document()
		document.add_paragraph('Nada foi encontrado para a empresa')
		document.save(path_relatorios+'relatório_%s.docx' % (cnpj_licitante,))
		return
	dados_licitacoes = []
	for l_id in dados_licitante['licitacao_id']:
		dados_licitacoes.append(dados_licitacao(str(l_id)))
	texto = '\tRELATÓRIO GERAL\n\n\tA empresa com CNPJ %s e razão social %s participou de %s licitações.\n\n' % (str(cnpj_licitante),dados_licitante['nome_licitante'],str(len(dados_licitacoes)))
	if len(dados_licitacoes):
		texto += '\tInformações sobre licitações em que a empresa concorreu:\n'
	else:
		texto += '\tNão há informações sobre licitações em que a empresa concorreu.'
	for dado in dados_licitacoes:
		if dado:
			texto += '\n\n\tLicitação registrada no banco de dados Audesp com id: %s\n' % (str(dado[0]))
			texto += '\tA licitação ocorreu no ano %s, tem como objeto "%s" e está registrada tendo valor total de R$%s\n' % (str(int(float(dado[1]['ano_licitacao']))),str(dado[1]['descricao_objeto']),str(dado[1]['valor_total']))
			if dado[2]:
				texto += '\tA entidade que realizou a licitação se denomina: %s\n' % (dado[2][0]['nome_completo'])
				if dado[2][1]:
					texto += '\tA entidade que realizou a licitação se localiza no município: %s\n' % (dado[2][1])
	document = Document()
	document.add_paragraph(texto)
	document.save(path_relatorios+'relatório_%s.docx' % (cnpj_licitante,))

def relatorio_socios(documento_socio):
    documento_socio = documento_socio.replace('.','').replace('-','')
    empresas_socio = []
    dics = licitantes.find({'cpf_adm':documento_socio})
    for dic in dics:
        empresas_socio.append((dic['_id'],dic['nome_licitante']))
    doc = Document() 
    doc.add_paragraph('A pessoa com documento %s é sócia administradora das seguintes empresas:\n\n' % (documento_socio,))
    if len(empresas_socio):
        for cnpj, e in empresas_socio:
            doc.add_paragraph(cnpj+' empresa de nome comercial '+e+'\n')
    else:
        doc.add_paragraph('Essa pessoa não é administradora de nenhuma empresa')
    doc.save(path_relatorios+'socio_empresas_cpf_%s.docx' % (documento_socio,))

def main(cnpj, cpf):
	cnpj = str(cnpj)
	cpf = str(cpf)
	relatorio_geral(cnpj)
	relatorio_socios(cpf)

if __name__ == '__main__':
	main('11311279000140')