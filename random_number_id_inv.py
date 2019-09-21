import uuid
arq = open('id_investigacao_scdf.txt','w')
arq.write(str(uuid.uuid4()).split('-')[0])
arq.close()