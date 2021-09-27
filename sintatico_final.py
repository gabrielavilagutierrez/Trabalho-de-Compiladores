#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lexico import Token
from operator import itemgetter
escopoAtual= "main"
tabela={"main":{}}
buffer_var = []
contador = 0
contador_aux = 0
buffer_tipo = None
buffer_funcao = ""
buffer_argumento=[]
buffer_escopo = None
cat = ""


def TS_Busca(cadeia):    
	return cadeia in tabela[escopoAtual]

def TS_Busca_Global(cadeia):    
	return cadeia in tabela["main"]

def TS_Busca_escopo(cadeia, escopo):    
	return cadeia in tabela[escopo]

def VerificaParametros():
	global buffer_argumento
	global escopoAtual
	global tabela
	global buffer_escopo
	tabelaAux = tabela[buffer_escopo]
	listaAux = []
	for linha in tabelaAux:
		if "param" in tabelaAux[linha]:
			listaAux.append(tabelaAux[linha])
	listaAux = sorted(listaAux, key=itemgetter(-1))
	if len(listaAux) != len(buffer_argumento):
		exit("Número de argumentos incompatível, esperado: {}, recebido: {}".format(len(listaAux),len(buffer_argumento)))
	else:
		for a,b in zip(listaAux, buffer_argumento):
			if not a[2] == b[2]:
				exit("Tipo de parametro incompatível, recebido: {}, esperado: {}".format(b[2],a[2]))
	buffer_argumento.clear()

def NovoEscopo(nomedoEscopo):
	contador_aux = 0
	tabela[nomedoEscopo] = {}

def TS_Inserir(cadeia, token, tipo,  escopo, cont):
	global escopoAtual
	global cat
	if TS_Busca(cadeia):
		exit("Variavél {}, já declarada no escopo {}".format(cadeia,escopo))
	tabela[escopoAtual][cadeia] = ([token, cat, tipo, escopoAtual, cont])

def TS_Var_Inserir(tipo):
    global buffer_var
    global escopoAtual
    global contador_aux
    global contador
    for variavel in buffer_var:
        if escopoAtual == "main":
            TS_Inserir(variavel.valor, variavel.tipo, tipo, escopoAtual, cont=contador)
            contador += 1
        else:
            TS_Inserir(variavel.valor, variavel.tipo, tipo , escopoAtual, cont=contador_aux)
            contador_aux += 1
    buffer_var.clear()  

def erro(token, esperado):
    print("Erro de sintaxe: linha {} | esperado: {} | entrada: {}"
          "".format(token.linha+1, esperado, token.valor))
    exit()

def programa(tokens):
	global tabela
	if not tokens:
		token = Token('<null>','<null>',0)
		erro(token,'program')
	if(tokens[0].valor != 'program'):
		erro(tokens.pop(0), 'program')
	else:
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<identificador>')
		if(tokens[0].tipo != 'identificador'):
			erro(tokens.pop(0),'<identificador>')
		else:
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'begin')
			corpo(tokens)
			if(tokens[0].valor != '.'):
				erro(tokens.pop(0), '.')
			else:
				tokens.pop(0)
				if tokens:
					erro(tokens.pop(0),'<fim>')
				else:
					return True


def corpo(tokens):
	dc(tokens)
	if(tokens[0].valor != 'begin'):
		erro(tokens.pop(0), 'begin')
	else:
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<comando>')
		comandos(tokens)
		if(tokens[0].valor != 'end'):
			erro(tokens.pop(0), 'end')
		else:
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'.')

def dc(tokens):
	global cat
	aux = tokens[0]
	if(aux.valor == 'var'):
		cat = "var"
		dc_v(tokens)
		mais_dc(tokens)
	elif(aux.valor == 'procedure'):
		cat = "proc"
		dc_p(tokens)
		mais_dc(tokens)
	else:
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'comando')
		return

def dc_v(tokens):
	if(tokens[0].valor != 'var'):
		erro(tokens.pop(0),'var')
	else:
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<identificador>')
		variaveis(tokens)
		if(tokens[0].valor != ':'):
			erro(tokens.pop(0), ':')
		else:
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'<tipo_var>')
			tipo_var(tokens)

def variaveis(tokens):
	global escopoAtual
	global contador
	global contador_aux
	global buffer_var
	if(tokens[0].tipo != 'identificador'):
		erro(tokens.pop(0), '<identificador>')
	else:
		buffer_var.append(tokens[0])
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,':')
		mais_var(tokens)

def mais_var(tokens):
	aux = tokens[0]
	if(aux.valor != ','):
		return
	else:
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<identificador>')
		variaveis(tokens)

def tipo_var(tokens):
	global buffer_var
	global escopoAtual
	global escopos
	aux = tokens[0]
	if(aux.valor == 'real' or aux.valor == 'integer'):
		TS_Var_Inserir(aux.valor)
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,';')
			return
	else:
		erro(aux, '<tipo_var>')

def mais_dc(tokens):
	aux = tokens[0]
	if(aux.valor == ';'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'end')
		dc(tokens)
	else:
		return

def dc_p(tokens):
	global cat
	global escopoAtual
	global contador
	if(tokens[0].valor == 'procedure'):
		cat = "proc"
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<identificador>')
		if(tokens[0].tipo == 'identificador'):
			TS_Inserir(tokens[0].valor, tokens[0].tipo, None, escopoAtual, cont=contador)
			escopoAtual = tokens[0].valor
			NovoEscopo(escopoAtual)
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'<parametros>')
			parametros(tokens)
			corpo_p(tokens)
		else:
			erro(tokens[0], '<identificador>')
	else:
		erro(tokens[0],'procedure')


def parametros(tokens):
	global cat
	aux = tokens[0]
	if(aux.valor == '('):
		cat = "param"
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<tipo_var>')
		lista_par(tokens)
		if(tokens[0].valor != ')'):
			erro(tokens.pop(0), ')')
		else:
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'begin')
	else:
		return

def lista_par(tokens):
	global cat
	cat = "param"
	variaveis(tokens)
	if(tokens[0].valor != ':'):
		erro(tokens.pop(0), ':')
	else:
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<tipo_var>')
		tipo_var(tokens)
		mais_par(tokens)

def mais_par(tokens):
	aux = tokens[0]
	if(aux.valor == ';'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<tipo_var>')
		lista_par(tokens)
	else:
		return

def corpo_p(tokens):
	global cat
	global escopoAtual
	cat = "var"
	dc_loc(tokens)
	if(tokens[0].valor != 'begin'):
		erro(tokens.pop(0), 'begin')
	else:
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<comando>')
		comandos(tokens)
		if(tokens[0].valor != 'end'):
			erro(tokens.pop(0),'end')
		else:
			escopoAtual = "main"
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'begin')

def dc_loc(tokens):
	aux = tokens[0]
	if(aux.valor == 'var'):
		dc_v(tokens)
		mais_dcloc(tokens)
	else:
		return

def mais_dcloc(tokens):
	aux = tokens[0]
	if(aux.valor == ';'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'begin')
		dc_loc(tokens)
	else:
		return

def comandos(tokens):
	comando(tokens)
	mais_comandos(tokens)

buffer_read = []

buffer_write = []

def comando(tokens):
	global buffer_tipo
	global buffer_var
	global buffer_escopo
	global buffer_read
	global escopoAtual
	global buffer_write
	aux = tokens[0]
	if(aux.valor == 'read'):
		tokens.pop(0)
		if(tokens[0].valor != '('):
			erro(tokens.pop(0), '(')
		else:
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'<identificador>')
			variaveis(tokens)
			for i in buffer_var:
				if(TS_Busca(i.valor)):
					buffer_read.append(tabela[escopoAtual][i.valor])
				elif(TS_Busca_Global(i.valor)):
					buffer_read.append(tabela["main"][i.valor])
				else:
					print("Variável: {} não declarada na linha: {}".format(i.valor,aux.linha+1))
					exit()
			if(tokens[0].valor != ')'):
				erro(tokens.pop(0), ')')
			else:
				linha = tokens.pop(0).linha
				if not tokens:
					token = Token('<null>','<null>',linha)
					erro(token,'end')
	elif(aux.valor == 'write'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'(')
		if(tokens[0].valor != '('):
			erro(tokens.pop(0),'(')
		else:
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'<identificador>')
			variaveis(tokens)
			for i in buffer_var:
				if(TS_Busca(i.valor)):
					buffer_read.append(tabela[escopoAtual][i.valor])
				elif(TS_Busca_Global(i.valor)):
					buffer_read.append(tabela["main"][i.valor])
				else:
					print("Variável: {} não declarada na linha: {}".format(i.valor,aux.linha+1))
					exit()
			if(tokens[0].valor != ')'):
				erro(tokens.pop(0),')')
			else:
				linha = tokens.pop(0).linha
				if not tokens:
					token = Token('<null>','<null>',linha)
					erro(token,'end')
	elif(aux.valor == 'while'):
		peek = tokens[1]
		if peek.valor == '(':
			peek = tokens[2]
		buffer_tipo = tabela[escopoAtual][peek.valor]
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
		condicao(tokens)
		if(tokens[0].valor != 'do'):
			erro(tokens.pop(0),'do')
		else:
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'<comando>')
			comandos(tokens)
			if(tokens[0].valor != '$'):
				erro(tokens.pop(0),'$')
			else:
				linha = tokens.pop(0).linha
				if not tokens:
					token = Token('<null>','<null>',linha)
					erro(token,'end')
	elif(aux.valor == 'if'):
		peek = tokens[1]
		if peek.valor == '(':
			peek = tokens[2]
		buffer_tipo = tabela[escopoAtual][peek.valor]
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
		condicao(tokens)
		if(tokens[0].valor != 'then'):
			erro(tokens.pop(0),'then')
		else:
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'<comando>')
			comandos(tokens)
			pfalsa(tokens)
			if(tokens[0].valor != '$'):
				erro(tokens.pop(0),'$')
			else:
				linha = tokens.pop(0).linha
				if not tokens:
					token = Token('<null>','<null>',linha)
					erro(token,'end')
	elif(aux.tipo == 'identificador'):
		# pegar o valor e buscar na TS e jogar no buffer 
		if not(TS_Busca(tokens[0].valor)):
			if not(TS_Busca_Global(tokens[0].valor)):
				print("Variável: {} não declarada na linha: {}".format(aux.valor,aux.linha+1))
				exit()
		buffer_tipo = tabela[escopoAtual][tokens[0].valor] if TS_Busca(tokens[0].valor) else tabela["main"][tokens[0].valor]
		buffer_escopo = tokens[0].valor
		# linha = tokens.pop(0).linha
		# if not tokens:
		# 	token = Token('<null>','<null>',linha)
		# 	erro(token,'<fator')
		restoident(tokens)
	else:
		erro(tokens.pop(0),'<comando>')

def condicao(tokens):
	expressao(tokens)
	relacao(tokens)
	expressao(tokens)

def expressao(tokens):
	termo(tokens) 
	outros_termos(tokens)

def termo(tokens):
	op_un(tokens)
	fator(tokens) 
	mais_fatores(tokens)

def op_un(tokens):
	aux = tokens[0]
	if(aux.valor == '+'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	elif(aux.valor == '-'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	else:
		return

def fator(tokens):
	global buffer_var
	global buffer_tipo
	global escopoAtual
	global tabela
	aux = tokens[0]
	if(aux.tipo == 'identificador'):
		if(TS_Busca(tokens[0].valor)):
			if(buffer_tipo[2] != tabela[escopoAtual][tokens[0].valor][2]):
				exit("Variável: {} de tipo não permitido na linha: {}".format(tokens[0].valor,tokens[0].linha+1))
		elif(TS_Busca_Global(tokens[0].valor)):
			if(buffer_tipo[2] != tabela["main"][tokens[0].valor][2]):
				exit("Variável: {} de tipo não permitido na linha: {}".format(tokens[0].valor,tokens[0].linha+1))
		else:
			exit("Variável: {} não declarada na linha: {}".format(tokens[0].valor,tokens[0].linha+1))
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<relação>')
	elif(aux.tipo == 'inteiro'):
		if(buffer_tipo[2] != "integer"):
			exit("Variável: {} de tipo não permitido na linha: {}".format(tokens[0].valor,tokens[0].linha+1))
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<relação>')
	elif(aux.tipo == 'real'):
		if(buffer_tipo[2] != "real"):
			exit("Variável: {} de tipo não permitido na linha: {}".format(tokens[0].valor,tokens[0].linha+1))
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<relação>')
	else:
		if(tokens[0].valor == '('):
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'<expressao>')
			expressao(tokens) 
			if(tokens[0].valor == ')'):
				linha = tokens.pop(0).linha
				if not tokens:
					token = Token('<null>','<null>',linha)
					erro(token,'<expressao>')
			else:
				erro(tokens.pop(0), ')')
		else:
			erro(tokens.pop(0), '(')

def mais_fatores(tokens):
	aux = tokens[0]
	if(aux.valor == '*' or aux.valor == '/'):
		op_mul(tokens)
		fator(tokens)
		mais_fatores(tokens)
	else:
		return

def op_mul(tokens):
	if(tokens[0].valor == '*'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	elif(tokens[0].valor == '/'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	else:
		erro(tokens.pop(0), '<op_mul>')

def outros_termos(tokens):
	aux = tokens[0]
	if(aux.valor == '+' or aux.valor == '-'):
		op_ad(tokens)
		termo(tokens)
		outros_termos(tokens)
	else:
		return

def op_ad(tokens):
	if(tokens[0].valor == '+'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	elif(tokens[0].valor == '-'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	else:
		erro(tokens.pop(0), 'op_ad')

def relacao(tokens):
	if(tokens[0].valor == '='):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	elif(tokens[0].valor == '<>'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	elif(tokens[0].valor == '>='):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	elif(tokens[0].valor == '<='):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	elif(tokens[0].valor == '>'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	elif(tokens[0].valor == '<'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	else:
		erro(tokens.pop(0), 'relação')

def restoident(tokens):
	global tabela
	global buffer_escopo
	linha = tokens.pop(0).linha
	if not tokens:
		token = Token('<null>','<null>',linha)
		erro(token,'<fator')
	if(tokens[0].valor == ':='):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<expressao>')
		expressao(tokens)
	else:
		if tabela["main"][buffer_escopo][1] != "proc":
			exit("Procedimento: {}. Não declarado na linha: {}".format(buffer_escopo, tokens[0].linha+1))
		lista_arg(tokens)


def argumentos(tokens):
	global buffer_argumento
	global tabela
	global escopoAtual
	global buffer_escopo
	if(tokens[0].tipo != 'identificador'):
		erro(tokens.pop(0),'<identificador>')
	else:
		# mais_ident(tokens)
		if not TS_Busca_escopo(tokens[0].valor, buffer_escopo):
			if not TS_Busca_Global(tokens[0].valor):
				exit("Variavel não declarada!!!!!")
		buffer_argumento.append(tabela[buffer_escopo][tokens[0].valor] if TS_Busca_escopo(tokens[0].valor,buffer_escopo) else tabela["main"][tokens[0].valor])
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<argumento>')
		mais_ident(tokens)

def mais_ident(tokens):
	if(tokens[0].valor == ';'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<argumento>')
		argumentos(tokens)
	else:
		return

def pfalsa(tokens):
	if(tokens[0].valor == 'else'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<argumento>')
		comandos(tokens)
	else:
		return

def mais_comandos(tokens):
	if(tokens[0].valor == ';'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<comando>')
		comandos(tokens)
	else:
		return

def lista_arg(tokens):
	if(tokens[0].valor == '('):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<argumento>')
		argumentos(tokens)
		if(tokens[0].valor != ')'):
			erro(tokens.pop(0),')')
		else:
			VerificaParametros()
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'comando')
	else:
		return


