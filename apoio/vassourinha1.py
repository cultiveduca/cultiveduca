#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     vassourinha.py
#  
# Lic. a ser definida.
# Escrito por Breno Neves em 16/05/2014
# 
# Este aplicativo auxiliar le um arquivo CSV e monta nosso banco de dados sobre
# a formacao dos professores.
# 
# Usamos o termo vassourinha por ser o script que varre de forma
# seletiva dados que nao podem ser considerados uteis no escopo
# do projeto.
# 
# Como entrada temos o arquivo csv.
# 
# Aqui aplicamos diversos filtros e metodologias de tratamento dos dados
# Todos os metodos aplicados sao devidamente descritos.
# 
# Por tratar-se de dados especificos de um arquivo, este script somente
# trata os dados do educacenso 2012 ou 1013 no formato CSV.
# 
# Utilizamos numeros / indices para acessar as variaveis, os nomes
# das mesmas estao em comentarios junto aos locais de acesso.
# 
# 
# 


import sys
import os
try:
	arq = sys.argv[1]
	os.stat(arq)
except:
	print "Precisamos de um arquivo de entrada em csv."
	sys.exit(1)

# vamos definir os indices das variaveis.
# este e o N-1  de acordo com o manual do censo!

# para o filtro de professor unico
FK_COD_DOCENTE = 1
ID_TIPO_DOCENTE = 103
# dados dos professores, escolaridade
FK_COD_ESCOLARIDADE = 26
# para verificacao de "superior completo"
ID_SITUACAO_CURSO_1 = 27
ID_SITUACAO_CURSO_2 = 37
ID_SITUACAO_CURSO_3 = 47
# para pos graduacao
ID_POS_GRADUACAO_NENHUM = 86
ID_ESPECIALIZACAO = 83
ID_MESTRADO = 84
ID_DOUTORADO = 85
# formacao continuada
ID_ESPECIFICO_CRECHE = 87
ID_ESPECIFICO_PRE_ESCOLA = 88
ID_ESPECIFICO_ANOS_INICIAIS = 89
ID_ESPECIFICO_ANOS_FINAIS = 90
ID_ESPECIFICO_ENS_MEDIO = 91
ID_ESPECIFICO_EJA = 92
ID_ESPECIFICO_NEC_ESP = 93
ID_ESPECIFICO_ED_INDIGENA = 94
ID_ESPECIFICO_CAMPO = 95
ID_ESPECIFICO_AMBIENTAL = 96
ID_ESPECIFICO_DIR_HUMANOS = 97
ID_ESPECIFICO_DIV_SEXUAL = 98
ID_ESPECIFICO_DIR_ADOLESC = 99
ID_ESPECIFICO_AFRO = 100
ID_ESPECIFICO_OUTROS = 101
ID_ESPECIFICO_NENHUM = 102

# Dados da escola, estado e municipio
PK_COD_ENTIDADE = 110
SIGLA = 112
FK_COD_MUNICIPIO = 113

# Pode ter um filtro futuramente.
ID_DEPENDENCIA_ADM = 116

# Perfil
NUM_IDADE = 5
ID_ZONA_RESIDENCIAL = 16
TP_SEXO = 6
ID_POSSUI_NEC_ESPECIAL = 17
ID_TIPO_CONTRATACAO = 104 # 1 a 4

# Mapeamento de estado-região
regioes = {
	'BA':'Nordeste',
	'DF':'Centro_Oeste',
	'PR':'Sul',
	'RR':'Norte',
	'RS':'Sul',
	'PB':'Nordeste',
	'TO':'Norte',
	'PA':'Norte',
	'PE':'Nordeste',
	'RN':'Nordeste',
	'PI':'Nordeste',
	'RJ':'Sudeste',
	'AC':'Norte',
	'AM':'Norte',
	'AL':'Nordeste',
	'CE':'Nordeste',
	'AP':'Norte',
	'GO':'Centro_Oeste',
	'ES':'Sudeste',
	'MG':'Sudeste',
	'RO':'Norte',
	'MA':'Nordeste',
	'SP':'Sudeste',
	'MT':'Centro_Oeste',
	'MS':'Centro_Oeste',
	'SC':'Sul',
	'SE':'Nordeste'
}

def ProcessaArvore(arv, tam):
	"""Eis o nosso algoritmo:
	Esta é uma árvore com dois níveis e no final um vetor de tamanho tam.
	No primeiro temos a categoria, por exemplo o estado, o município,
	uma escola ou até mesmo o Brasil inteiro.
	No segundo nível, temos os docentes únicos, filtrados pelo código
	INEP.
	No terceiro nivel temos um vetor com os dados a serem contabilizados.
	Esta filtragem garante que:
	    - Se o docente trabalha em mais de um local do mesmo nível,
	      este será contabilizado apenas uma vez.
	    - Se o docente trabalha em mais de um local mas em níveis
	      diferentes, este será contabilizado em ambos. Isto garante
	      que os dados serão compatíveis com os dados obtidos pelos
	      órgãos de registro locais, como as secretarias de educação
	      ou até mesmo a diretoria de uma escola.
	Exemplo prático: Se nosso nível de filtragem é escola e um docente
	    está trabalhando em duas escolas diferentes, ele aparecerá em
	    ambas, porém, se nosso nível for por cidade e ambas as escolas
	    forem na mesma cidade, este docente aparecerá apenas uma vez.
	"""
	# Temos os vetores para cada categoria, eles devem possuir o
	# mesmo tamanho especificado na chamada da funcao.
	# Criamos tambem o meta-dado _N contendo a amostragem.
	vets = {"_N":{}}
	for i in arv:
		vets[i] = [0 for hgj in range(tam+2)]
		vets["_N"][i] = len(arv[i])
	# Para cada elemento de primeiro nivel
	for g in arv:
		# Para cada elemento de segundo nivel
		for i in arv[g]:
			# Para cada item no vetor
			for t in range (tam):
				# Se for verdadeiro, incremente o vetor!
				# Optamos por nao converter em int.
				if type(arv[g][i][t]) == str:
					if arv[g][i][t] != '0': vets[g][t]+= 1
				else:
					vets[g][t] += arv[g][i][t]
			vets[g][-2] += len(docesc[i].keys())
			vets[g][-1] += sum(docesc[i].values())
		try: vets[g][-2] = "%.2f"%(float(vets[g][-2])/vets['_N'][g])
		except: vets[g][-2] = "0"
		try: vets[g][-1] = "%.2f"%(float(vets[g][-1])/vets['_N'][g])
		except: vets[g][-1] = '0'
	# Retorna o dicionario contendo os numeros.
	
	return vets


def InsereDocente(arv, i, key, val):
	arv[key][i[FK_COD_DOCENTE]] = val

# docesc auxilia para descobrirmos em quantas escolas o docente trabalha
docesc = {}
def Arquivo(arq):
	global docesc
	"Iterador leitor de arquivo CSV"
	f = file(arq)
	for i in f:
		i = i.split(";")
		# Notamos que algumas faculdades possuem ; no nome
		# corrigimos juntando a var 35 com a 36.
		if len(i) != 128 and len(i) != 129:
			print i
			print len(i)
		if len(i) == 129:
			i[35] += i[36]
			del i[36]
		# Apenas docentes da rede municipal, de acordo com o manual.
		# Estrutura: docente -> escola -> n. turmas
		if i[ID_TIPO_DOCENTE] == '1':
			if not i[FK_COD_DOCENTE] in docesc:
				docesc[i[FK_COD_DOCENTE]] = {}
			if not i[PK_COD_ENTIDADE] in docesc[i[FK_COD_DOCENTE]]:
				docesc[i[FK_COD_DOCENTE]][i[PK_COD_ENTIDADE]] = 0
			docesc[i[FK_COD_DOCENTE]][i[PK_COD_ENTIDADE]] += 1
		if i[ID_TIPO_DOCENTE] == '1' and i[ID_DEPENDENCIA_ADM] == '3':
			yield(i)

def EscreveCSV(arv, arq):
	o = file(arq,"w")
	print >>o, "key;n;esc_fund_inc;esc_fund_comp;esc_normmag;esc_nm_indigena;esc_medio;sup_inc;superior;pos_nenhuma;pos_espec;pos_mestrado;pos_doutorado;fc_nenhuma;fc_outras;fc_especifica;fc_creche;fc_pre_esc;fc_anos_inic;fc_anos_fin;fc_ens_med;fc_eja;fc_nec_esp;fc_ed_ind;fc_campo;fc_ambiental;fc_dir_hum;fc_div_sex;fc_dir_adolesc;fc_afro;zona;genero;nec_esp;fx_m20;fx_2029;fx_3039;fx_4049;fx_5059;fx_6069;fx_70m;escpp;turmaspp"
	for i in arv:
		if i != "_N":
			print >>o, ";".join([str(i), str(arv["_N"][i])]+[str(l) for l in arv[i]])
	o.close()

def PreparaDocente(i):
	"""Prepara o docente para ser inserido na arvore.
	Separamos os dados úteis ao nosso projeto e os organizamos em
	vetores que podem ter 0 ou 1. Utilizamos o formato char por
	utilizar menos bytes (1) no lugar de 8 (int)
	
	Com o pre-processamento desta funcao, teremos na saida um CSV
	com o seguinte cabecalho:
	
	key;esc_fund_inc;esc_fund_comp;esc_normmag;esc_nm_indigena;esc_medio;sup_inc;superior;pos_nenhuma;pos_espec;pos_mestrado;pos_doutorado;fc_nenhuma;fc_outras;fc_especifica;fc_creche;fc_pre_esc;fc_anos_inic;fc_anos_fin;fc_ens_med;fc_eja;fc_nec_esp;fc_ed_ind;fc_campo;fc_ambiental;fc_dir_hum;fc_div_sex;fc_dir_adolesc;fc_afro
	
	novas
	
	zona;genero;nec_esp;fx_m20;fx_2029;fx_3039;fx_4049;fx_5059;fx_6069;fx_70m
	"""
	# Valida a escolaridade. 0 = fund inc 7 = sup comp 6 = sup inc.
	esc = ['0' for jh in range(0, 7)]
	# Coloca na faixa etaria.
	fxe = ['0', '0', '0', '0', '0', '0', '0']
	ii = int(i[NUM_IDADE])
	# Populamos a faixa etaria.
	if ii < 20:     fxe[0] = '1'
	elif ii < 30:   fxe[1] = '1'
	elif ii < 40:   fxe[2] = '1'
	elif ii < 50:   fxe[3] = '1'
	elif ii < 60:   fxe[4] = '1'
	elif ii < 70:   fxe[5] = '1'
	else:           fxe[6] = '1'
	zona = '0'
	if i[ID_ZONA_RESIDENCIAL] == '2':    zona = '1'
	genero = '0'
	if i[TP_SEXO] == 'M':
		genero = '1'
	nec = i[ID_POSSUI_NEC_ESPECIAL]
	# Marcamos como inteiro a escolaridade
	form = int(i[FK_COD_ESCOLARIDADE])
	# Esta verificacao valida a variavel escolaridade.
	# Apesar de no manual do educacenso a opcao 6 constar como superior
	# completo, cruzamos esta informacao com as variaveis das situacoes
	# dos cursos e descobrimos quem nao possui um curso superior completo
	# mas marcou a opcao no censo. Nestes casos, criamos a opcao de
	# superior incompleto, extra-oficialmente.
	# Este trecho diz que se a escolaridade nao for superior completo
	# decrementa um.
	if not '1' in [
		i[ID_SITUACAO_CURSO_1], 
		i[ID_SITUACAO_CURSO_2], 
		i[ID_SITUACAO_CURSO_3]
	]: form -= 1
	# Agora que temos a escolaridade, setamos o byte.
	esc[form] = '1'
	# Selecionamos o nível de pós-graduação. Sabemos que vários docentes
	# possuem especialização, mestrado e doutorado. Mas vamos considerar
	# como titulação, apenas a mais alta.
	pos = ['0' for jioj in range(0, 4)]
	if form == 6:
		if   i[ID_DOUTORADO] == '1':  pos[3] = '1'
		elif i[ID_MESTRADO ] == '1':  pos[2] = '1'
		elif i[ID_ESPECIALIZACAO] == '1':  pos[1] = '1'
		elif i[ID_POS_GRADUACAO_NENHUM] == '1':  pos[0] = '1'
	# Quem não possui superior completo não pode ter pós graduação!
	# Vamos verificar a situação da formação continuada.
	# Temos três opções simples e diretas:
	# - Possui ao menos uma formação continuada específica
	# - Possui uma formação continuada não especificada (outros)
	# - Não possui formação continuada.
	# Temos que seguir esta ordem para definir o vetor.
	fce = ['0', '0', '0']
	if sum([int(k) for k in i[ID_ESPECIFICO_CRECHE:ID_ESPECIFICO_AFRO+1]]):
		fce[2] = '1'
	elif i[ID_ESPECIFICO_OUTROS] == '1':
		fce[1] = '1'
	else: fce[0] = '1'
	return esc+pos+fce+i[ID_ESPECIFICO_CRECHE:ID_ESPECIFICO_AFRO+1]+[zona,genero,nec]+fxe
# DadosPorRegiao()
# - Filtra os dados do censo usando a estrutura de arvore.
# - Tem como saida um vetor no formato csv.
def DadosPorRegiao():
	# Aqui inicializamos o dicionario das regioes. Dentro de cada
	# regiao temos um outro dicionario dos docentes.
	arv = {}
	# Populamos o primeiro nivel com as regioes.
	for i in regioes.values():
		arv[i] = {}
	# Lemos o arquivo de entrada / CSV
	for i in Arquivo(arq):
		# Apenas docentes. Ver ID_TIPO_DOCENTE no manual.
		InsereDocente(arv, i, regioes[i[SIGLA]], PreparaDocente(i))
	print len(arv[arv.keys()[0]][arv[arv.keys()[0]].keys()[0]])
	EscreveCSV(ProcessaArvore(arv, 28) , "out.regioes.csv"  )

#~ DadosPorRegiao()


def DadosTudo():
	# Aqui inicializamos o dicionario das regioes. Dentro de cada
	# regiao temos um outro dicionario dos docentes.
	abr = {'BR':{}}
	arvr = {}
	abe = {}
	abm = {}
	abi = {}
	for i in regioes.keys():
		abe[i] = {}
	# Populamos o primeiro nivel com as regioes.
	for i in regioes.values():
		arvr[i] = {}
	# Lemos o arquivo de entrada / CSV
	for i in Arquivo(arq):
		d = PreparaDocente(i)
		InsereDocente(arvr, i, regioes[i[SIGLA]], d)
		InsereDocente(abr, i, 'BR', d)
		InsereDocente(abe, i, i[SIGLA], d)
		if not i[FK_COD_MUNICIPIO] in abm: abm[i[FK_COD_MUNICIPIO]] = {}
		InsereDocente(abm, i, i[FK_COD_MUNICIPIO], d)
		if not i[PK_COD_ENTIDADE] in abi: abi[i[PK_COD_ENTIDADE]] = {}
		InsereDocente(abi, i, i[PK_COD_ENTIDADE], d)
	#~ print len(arv[arv.keys()[0]][arv[arv.keys()[0]].keys()[0]])
	# 28 mais as novas
	EscreveCSV(ProcessaArvore(arvr, 38) , "out/regioes.csv"  )
	EscreveCSV(ProcessaArvore(abr, 38) , "out/brasil.csv"  )
	EscreveCSV(ProcessaArvore(abe, 38) , "out/estados.csv"  )
	EscreveCSV(ProcessaArvore(abm, 38) , "out/cidades.csv"  )
	EscreveCSV(ProcessaArvore(abi, 38) , "out/escolas.csv"  )

DadosTudo()
