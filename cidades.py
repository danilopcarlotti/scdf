from cursorConexao import cursorConexao
import re, pickle, geopy.distance

class cidades():
	"""API para trabalhar com dados georreferenciados de cidades"""
	def __init__(self, dicionario_cidades=None):
		self.dicionario_cidades = dicionario_cidades
		self.cursor = cursorConexao()
		self.dados_comp = None

	def dados_completos(self):
		query = 'SELECT ID, ID_IBGE, NM_CIDADE, NM_ESTADO, NM_BAIRRO, COORD_1, COORD_0, IBGE FROM cidades_brasil.cidades;'
		self.cursor.execute(query)
		return self.cursor.fetchall()

	def dados_distancias_cidade(self, cidade, estado):
		query = 'SELECT ID, NM_CIDADE, NM_ESTADO, COORD_1, COORD_0 FROM cidades_brasil.cidades where (NM_CIDADE like "%{}%" and NM_ESTADO like "%{}%");'.format(cidade.upper(),estado.upper())
		self.cursor.execute(query)
		dados = self.cursor.fetchall()
		cidade = dados[0][1]+'_'+dados[0][2]
		coordenadas_cidade = (dados[0][3],dados[0][4])
		query = 'SELECT ID, NM_CIDADE, NM_ESTADO, COORD_1, COORD_0 FROM cidades_brasil.cidades'
		self.cursor.execute(query)
		distancias = {}
		for id_p, nm_cid, nm_est, c1, c0 in self.cursor.fetchall():
			cidade_atual = nm_cid+'_'+nm_est
			if cidade_atual != cidade and cidade_atual not in distancias:
				distancias[cidade_atual] = geopy.distance.distance((float(c1), float(c0)),coordenadas_cidade).km
		return distancias

	def dicionario_todas_cidades(self):
		query = 'SELECT nm_cidade,nm_estado FROM cidades_brasil.cidades;'
		self.cursor.execute(query)
		dados = self.cursor.fetchall()
		dicionario = {}
		for nm_c, nm_e in dados:
			cidade_atual = nm_c+'_'+nm_e
			if cidade_atual not in dicionario:
				dicionario[cidade_atual] = {'distância_outras_cidades' : self.dados_distancias_cidade(nm_c, nm_e)}
		pickle.dump(dicionario, open("distancia_cidades.pickle", "wb"))

	def distancia_maxima(self, dicionario_cidade, distancia_minima, distancia_maxima):
		cidades_no_intervalo = []
		for k,v in dicionario_cidade['distância_outras_cidades']:
			if v > distancia_minima and v < distancia_maxima:
				cidades_no_intervalo.append((k,v))
		return cidades_no_intervalo

def main():
	cid = cidades()
	# for k,v in cid.dados_distancias_cidade('RIBEIRÃO PRETO','SÃO PAULO').items():
	# 	print(k,v)
	cid.dicionario_todas_cidades()

if __name__ == '__main__':
	main()