import pymongo, pandas as pd, pickle, os, re
from docx import Document

myclient = pymongo.MongoClient('mongodb://localhost:27017/')

mydb = myclient['TCE']
# desp_emp_col = mydb['%s_desp_empresas_%s' % (ano, counter)]

path_relatorios = ''

dicionario_collections_transparencia = {2018:(1,307),2019:(1,87)}

def consertar_str_cnpj(cnpj):
    cnpj = cnpj.replace('/','').replace('-','').replace('.','')
    if len(cnpj) == 14:
        return cnpj
    elif len(cnpj) > 14:
        return consertar_str_cnpj(cnpj[:-1])
    else:
        return consertar_str_cnpj('0'+cnpj)

def relatorio_cnpj(cnpj):
    # texto = ''
    # dicionarios_despesas_empresa = []
    rows_despesas_empresa = []
    for k,v in dicionario_collections_transparencia.items():
        ini, fim = v
        for counter in range(ini,fim+1):
            collection_desp = mydb['%s_desp_empresas_%s' % (str(k), str(counter))]
            dicionario_despesas = collection_desp.find_one({'_id':cnpj})
            if dicionario_despesas:
                for k in range(len(dicionario_despesas['historico_despesa'])):
                    # dicionarios_despesas_empresa.append('\n\n\tDESPESA\n\nData despesa: %s\nMunicípio:%s\nÓrgão:%s\nModalidade de licitação:%s\nDescrição da despesa:%s\nValor da despesa:%s\n' % 
                    # (dicionario_despesas['dt_emissao_despesa'][k],dicionario_despesas['ds_municipio'][k],dicionario_despesas['ds_orgao'][k],dicionario_despesas['ds_modalidade_lic'][k],dicionario_despesas['historico_despesa'][k],dicionario_despesas['vl_despesa'][k]))
                    try:
                        valor = float(dicionario_despesas['vl_despesa'][k].replace(',','.'))
                    except:
                        valor = 0.0
                    rows_despesas_empresa.append({
                        'Data da despesa':dicionario_despesas['dt_emissao_despesa'][k],
                        'Município':dicionario_despesas['ds_municipio'][k],
                        'Órgão':dicionario_despesas['ds_orgao'][k],
                        'Modalidade licitação':dicionario_despesas['ds_modalidade_lic'][k],
                        'Descrição da despesa':dicionario_despesas['historico_despesa'][k],
                        'Valor da despesa':valor
                    })
    # if len(dicionarios_despesas_empresa):
    #     texto += 'Relatório para a empresa com CNPJ: %s\n\n' % (cnpj,)
    #     for d in dicionarios_despesas_empresa:
    #         texto += d
    # else:
    #     texto += 'Não foram encontradas despesas públicas associadas a esta empresa com CNPJ: %s\n\n' % (cnpj,)
    df = pd.DataFrame(rows_despesas_empresa,index=[i for i in range(len(rows_despesas_empresa))])
    if len(rows_despesas_empresa):
        # return (texto,df)
        return True, df
    else:
        return False, df

def main(cnpj):
    cnpj = consertar_str_cnpj(str(cnpj))
    res, df = relatorio_cnpj(cnpj)
    if res:
        df.to_excel('relatorios/relatorio_despesas_publicas_com_%s.xlsx' % (cnpj,),index=False)

if __name__ == '__main__':
	# main('01704233000138')
    for i in []:
        main(i)