#!/usr/bin/python
#coding: utf8

import shelve
def csv2dict(f):
	f = file(f)
	fs = f.readline().strip().split(";")
	d = {}
	for i in f:
		i = i.strip().split(";")
		if i[0] != 'DF':
			d[i[0]] = {}
			for k in range(1, len(fs)):
				try: i[k] = int(i[k])
				except:pass
				d[i[0]][fs[k]] = i[k]
			d[i[0]]['generof'] = d[i[0]]['n'] - d[i[0]]['genero']
			d[i[0]]['zonar'] = d[i[0]]['n'] - d[i[0]]['zona']
			for l in d[i[0]].keys():
				if type(d[i[0]][l] == int):
					d[i[0]][l+'_p'] = "%.2f%%"%(100*float(d[i[0]][l])/d[i[0]]['n'])
	return d


tab = [i.strip().split(";") for i in file("TAB_MUNICIPIO_2013.txt").readlines()[1:]]

br = shelve.open("brasil.db")
brd = csv2dict("brasil.csv")
for i in brd:
	br[i] = brd[i] 

est = {}
ci = {}
for i in tab:
	if not i[2] in est:
		est[i[2]] = {'regiao':i[0],'cidades':[]}
	if not (i[3],i[4]) in est[i[2]]['cidades']:
		est[i[2]]['cidades'].append((i[3],i[4]))
	ci[i[3]] = (i[4], i[2])


br = shelve.open("estados.db")
brd = csv2dict("estados.csv")
for i in brd:
	brd[i]['cidades'] = est[i]
	br[i] = brd[i]
	br[i]['estado'] = est[i]

br = shelve.open("cidades.db")
brd = csv2dict("cidades.csv")
for i in brd:
	brd[i]['nome'] = ci[i][0]
	brd[i]['estado'] = ci[i][1]
	br[i] = brd[i]

br = shelve.open("escolas.db")
brd = csv2dict("escolas.csv")
for i in brd:
	br[i] = brd[i]

