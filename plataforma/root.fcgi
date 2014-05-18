#!/usr/bin/env python
# coding: utf8

import sys
import os
import shelve
"""Esta pagina possui uma pessima documentacao e foi feita rapidamente
apenas para termos um prototipo.

Nao usamos banco de dados, usamos apenas uma saida compilada dos 
dados dos outros scripts. Os cruzamentos sao feitos manualmente.

Aguarde a continuacao.


"""
class req:
	def __init__(mi, envr, srr=""):
		mi.srr = srr
		mi.pid = envr["UNIQUE_ID"]
		mi.url = envr["PATH_INFO"]
		mi.ip  = envr["REMOTE_ADDR"]
		mi.ua  = envr["HTTP_USER_AGENT"]
		mi.query = {}
		cx = envr["QUERY_STRING"].split("&")
		for i in cx:
			if "=" in i:
				mi.query[i[:i.index("=")]] = i[i.index("=")+1:]
		if "HTTP_COOKIE" in envr:
			cookie = envr["HTTP_COOKIE"].split(";")
			mi.cookie = {}
			for i in cookie:
				if "=" in i:
					mi.cookie[i[:i.index("=")].strip()] = i[i.index("=")+1:].strip()
		else:
			mi.cookie = {}
		mi.resp = []
	def go(mi, st, p=""):
		if st == 200:
			sr = "200 OK"
		elif st == 301 or st == 303:
			sr = "303 See Other"
			if p != "":
				mi.resp.append(("Location", p))
		elif st == 404:
			sr = "404 Not Found"
			if p != "":
				mi.resp.append(("Location", p))
		if not("Content-type" in str(mi.resp)):
			 mi.resp.append(("Content-type", "text/html"))
		mi.srr(sr, mi.resp)
	def setcookie(mi, cn, val):
		mi.resp.append(("Set-cookie", "%s=%s"%(cn,val)))






stp = {}
for i in os.listdir("static"):
	stp["/"+i.split(".")[0]] = "static/%s"%i
	
base = file("static/base.html").read()
br = shelve.open("db/brasil.db", flag='r')
est = shelve.open("db/estados.db", flag='r')
cid = shelve.open("db/cidades.db", flag='r')
esc = shelve.open("db/escolas.db", flag='r')
cachecid = {}
for i in cid:
	cachecid[cid[i]['nome']] = i



def dMapa(d, nome):
	mod = """		<div class="center">
						<h2 class="datah">Perfil dos docentes da Rede Municipal de $mun$</h2>
						<div class="datacont1">
							<div class="datacont2">
								<b>%(n)i</b>
							</div>
							<div class="datacont3">
								<b>É o número total de docentes atuando na rede municipal.</b>
							</div>
							<br style="width:100%%;clear:both">
						</div>
	
						<div class="datacont1">
							<div class="datacont2">
								<b>%(turmaspp)s</b>
							</div>
							<div class="datacont3">
								<b>É o número médio de turmas por professor.</b>
							</div>
							<br style="width:100%%;clear:both">
						</div>
						
						<h3 class="datah">Destes %(n)i docentes:</h3>
						<div class="datacont1">
							<div class="datablk2" style="float: left">
								<b>%(genero_p)s%%</b>
								<i>%(genero)i</i>
								Sao Homens
							</div>
							<div class="datablk2" style="float: right">
								<b>%(generof_p)s%%</b>
								<i>%(generof)i</i>
								Sao Mulheres
							</div>
							<br style="width:100%%;clear:both">
						</div>
						<br><br>
						<div class="datacont1">
							<div class="datablk2" style="float: left">
								<b>%(zonar_p)s%%</b>
								<i>%(zonar)i</i>
								estão na zona urbana
							</div>
							<div class="datablk2" style="float: right">
								<b>%(zona_p)s%%</b>
								<i>%(zona)i</i>
								estão na zona rural
							</div>
							<br style="width:100%%;clear:both">
						</div>
						<br><br>
						<div class="datacont1">
							<div class="datacont2">
								<b>%(nec_esp_p)s</b>
								<i>%(nec_esp)i</i>
							</div>
							<div class="datacont3">
								<b>Possuem algum tipo de necessidade especial.</b>
							</div>
							<br style="width:100%%;clear:both">
						</div>
						<br><br>
						<h3 class="datah">Quanto a formação inicial:</h3>
						<div class="datacont1">
							<div class="datablk3">
								EF. Incompleto
								<b>%(esc_fund_inc_p)s%%</b>
								<i>%(esc_fund_inc)i</i>
							</div>
							<div class="datablk3">
								EF. Completo
								<b>%(esc_fund_comp_p)s%%</b>
								<i>%(esc_fund_comp)i</i>
							</div>
							<div class="datablk3">
								Magistério
								<b>%(esc_normmag_p)s%%</b>
								<i>%(esc_normmag)i</i>
							</div>
							<div class="datablk3">
								Mag. Indígena
								<b>%(esc_nm_indigena_p)s%%</b>
								<i>%(esc_nm_indigena)i</i>
							</div>
							<div class="datablk3">
								Ensino Médio
								<b>%(esc_medio_p)s%%</b>
								<i>%(esc_medio)i</i>
							</div>
							<br><br>
							<div class="datablk3">
								Sup. Incompleto
								<b>%(sup_inc_p)s%%</b>
								<i>%(sup_inc)i</i>
							</div>
							<div class="datablk3">
								Superior
								<b>%(superior_p)s%%</b>
								<i>%(superior)i</i>
							</div>

							<br style="width:100%%;clear:both">
						</div>
						<h3 class="datah">Quanto a formação continuada:</h3>
						<div class="datacont1">
							<div class="datablk4" style="float:left">
								Não possui
								<b>%(fc_nenhuma_p)s%%</b>
								<i>%(fc_nenhuma)i</i>
							</div>
							<div class="datablk4">
								Outras
								<b>%(fc_outras_p)s%%</b>
								<i>%(fc_outras)i</i>
							</div>
							<div class="datablk4" style="float: right">
								Específica
								<b>%(fc_especifica_p)s%%</b>
								<i>%(fc_especifica)i</i>
							</div>
							<br style="width:100%%;clear:both">
						</div>

						<h3 class="datah">Quanto a formação continuada específica:</h3>
						<div class="datacont1">
							<div class="datablk3">
								Creche
								<b>%(fc_creche_p)s%%</b>
								<i>%(fc_creche)i</i>
							</div>
							<div class="datablk3">
								Pré-Escola
								<b>%(fc_pre_esc_p)s%%</b>
								<i>%(fc_pre_esc)i</i>
							</div>
							<div class="datablk3">
								Anos Iniciais
								<b>%(fc_anos_inic_p)s%%</b>
								<i>%(fc_anos_inic)i</i>
							</div>
							<div class="datablk3">
								Anos Finais
								<b>%(fc_anos_fin_p)s%%</b>
								<i>%(fc_anos_fin)i</i>
							</div>
							<div class="datablk3">
								Ens. Médio
								<b>%(fc_ens_med_p)s%%</b>
								<i>%(fc_ens_med)i</i>
							</div>
							<div class="datablk3">
								EJA
								<b>%(fc_eja_p)s%%</b>
								<i>%(fc_eja)i</i>
							</div>
							<div class="datablk3">
								Nec. Esp.
								<b>%(fc_nec_esp_p)s%%</b>
								<i>%(fc_nec_esp)i</i>
							</div>
							<div class="datablk3">
								Ed. Indígena
								<b>%(fc_ed_ind_p)s%%</b>
								<i>%(fc_ed_ind)i</i>
							</div>
							<div class="datablk3">
								Ed. Campo
								<b>%(fc_campo_p)s%%</b>
								<i>%(fc_campo)i</i>
							</div>
							<div class="datablk3">
								Ambiental
								<b>%(fc_ambiental_p)s%%</b>
								<i>%(fc_ambiental)i</i>
							</div>
							<div class="datablk3">
								Dir. Humanos
								<b>%(fc_dir_hum_p)s%%</b>
								<i>%(fc_dir_hum)i</i>
							</div>
							<div class="datablk3">
								Div. Sexual
								<b>%(fc_div_sex_p)s%%</b>
								<i>%(fc_div_sex)i</i>
							</div>
							<div class="datablk3">
								Afro
								<b>%(fc_afro_p)s%%</b>
								<i>%(fc_afro)i</i>
							</div>
							<br style="width:100%%;clear:both">
						</div>
						<h3 class="datah">Quanto a pós-graduação:</h3>
						<div class="datacont1">
							<div class="datablk4" style="float:left">
								Especialização
								<b>%(pos_espec_p)s%%</b>
								<i>%(pos_espec)i</i>
							</div>
							<div class="datablk4">
								Mestrado
								<b>%(pos_mestrado_p)s%%</b>
								<i>%(pos_mestrado)i</i>
							</div>
							<div class="datablk4" style="float: right">
								Doutorado
								<b>%(pos_doutorado_p)s%%</b>
								<i>%(pos_doutorado)i</i>
							</div>
							<br style="width:100%%;clear:both">
						</div>
					</div>
	"""
	return (mod%d).replace("%%","%").replace("$mun$", nome)

def aBr():
	r = "<div class='center'><h2>Gostaria de ver por Estado?</h2>"
	for i in ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']:
		r += "<a class='next' href='estado.%s'>%s</a>"%(i, i)
	return r+"</div>"

def aEst(e):
	r = "<div class='center'><h2>Gostaria de ver por Município?</h2>"
	for i in est[e]['cidades']['cidades']:
		r += "<a class='next2' href='cidade.%s'>%s</a>"%(i[0], i[1])
	return r+"</div>"
def busca(r):
	q = r.query['busca'].upper().replace("+"," ")
	if len(q) == 2 and q in est:
		r.go(301, "estado."+q)
		return []
	elif q.isdigit() and q in cid:
		r.go(301, "cidade."+q)
		return []
	elif q.isdigit() and q in esc:
		r.go(301, "escola."+q)
		return []
	else:
		rr = 0
		if q in cachecid:
			rr = cachecid[q]
		if rr != 0:
			r.go(301, "cidade."+rr)
			return []
		else:
			r.go(301, "busca")
			return []


def myapp(environ, start_response):
	r = req(environ, start_response)
	if r.url == "/busca" and "busca" in r.query:
		return busca(r)
	r.go(200)
	if r.url == "/":
		r.url = "/indice"
	if r.url in stp:
		c = file(stp[r.url]).read().split("\n\n")
		return [base.format(title=c[0],content=c[1])]
	if r.url.startswith('/estado.') and r.url.split('.')[-1] in ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']:
		e = r.url.split('.')[-1]
		return [base.format(title="Estado "+e,content=dMapa(est[e], e)+aBr()+aEst(e))]
	if r.url.startswith('/cidade.') and r.url.split('.')[-1] in cid:
		c = r.url.split('.')[-1]
		return [base.format(title="Cidade "+cid[c]['nome']+" (%s)"%cid[c]['estado'],content=dMapa(cid[c], cid[c]['nome']+" (%s)"%cid[c]['estado'])+aBr()+aEst(cid[c]['estado']))]
	if r.url == "/brasil":
		return [base.format(title="Brasil",content=dMapa(br["BR"], 'BR')+aBr())]
	if r.url == "/busca":
		return [base.format(title="Busca",content="Nenhum resultado encontrado. Tente novamente.")]
	return ["Página em construção: %s"%r.url]

if __name__ == '__main__':
    from fcgi import WSGIServer
    WSGIServer(myapp).run()
