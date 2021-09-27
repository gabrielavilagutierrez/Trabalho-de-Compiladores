#!/usr/bin/env python
# -*- coding: utf-8 -*-

palavraReservada = ('$','if','then','while','do','write','read','else','begin','end','real','integer','var','procedure','program')
simboloSimples = ('+','-','<','>','*','/',',','.','(',')',';',':','=')
simboloDuplo = (':=','<>','<=','>=')
delimitador = ('\t','\n',' ','$','+','-','<','>','*','/',',','.','(',')',';',':','=')
isComent1 = False
isComent2 = False
simbolo = ''
isAux = False
isAux2 = False
isVerificarDuplicidade = False
token = ''
tokens = []

class Token:
    def __init__(self, valor, tipo, linha):
        self.valor = valor
        self.tipo = tipo
        self.linha = linha
        self.categoria = None

    def __str__ (self):
        return "Token ({valor}: {tipo} - {linha})".format(
            valor = self.valor, tipo = self.tipo, linha = self.linha)

    __repr__ = __str__

    def __eq__(self, outro):
        return (self.valor, self.tipo) == (outro.valor, outro.tipo)

class Lexico(object):
    def __init__(self, texto): #Construtor da classe.
        self.texto = texto

    def verificarToken(self, i):
        if (token[0].isalpha() and token.isalnum()):
            if(token in palavraReservada):
                tokens.append(Token(token,'reservada',i))
            else:
                tokens.append(Token(token,'identificador',i))
        elif(token.isdigit()):
            tokens.append(Token(token,'inteiro',i))
        elif(token == 'end.'):
            tokens.append(Token('end','reservada',i))
            tokens.append(Token('.','simples',i))
        else:
            try:
                float(token)
                tokens.append(Token(token,'real',i))
            except:
                tokens.append(Token(token,'invalido',i))

    def tokenizar(self):
        texto = self.texto
        global palavraReservada
        global simboloSimples
        global simboloDuplo
        global delimitador
        global simbolo
        global isComent2
        global isComent1
        global isAux
        global isAux2
        global isVerificarDuplicidade
        global token
        global tokens

        for i, linha in enumerate(texto):
            for caracter in linha:
                #identificar se é comentario
                if (isComent2):
                    '''Se isAux leu /* '''
                    if (isAux):
                        if (isAux2):
                            '''Consumiu comentário'''
                            if (caracter == '/'):
                                isAux = False
                                isAux2 = False
                                isComent2 = False
                            else:
                                isAux2 = False
                        elif (caracter == '*'):
                            isAux2 = True
                    elif (caracter == '*'):
                        isAux = True
                    else:
                        if(caracter == '{'):
                            tokens.append(Token('/','simples',i))
                            isComent2 = False
                            isAux = False
                            isAux2 = False
                            isComent1 = True
                        elif(caracter == '/'):
                            tokens.append(Token('/','simples',i))
                            isComent1 = False
                            isAux = False
                            isAux2 = False
                            isComent2 = True
                        elif(caracter.isdigit()):
                            tokens.append(Token('/','simples',i))
                            isComent1 = False
                            isComent2 = False
                            isAux = False
                            isAux2 = False
                        elif(caracter.isalpha()):
                            tokens.append(Token('/','simples',i))
                            isComent1 = False
                            isComent2 = False
                            isAux = False
                            isAux2 = False
                        else:
                            token = token +'/'+ caracter
                            isComent1 = False
                            isComent2 = False
                            isAux = False
                            isAux2 = False
                elif (isComent1):
                    if(caracter == '}'):
                        isComent1 = False
                elif(caracter == '{'):
                    if(token != ''):
                        self.verificarToken(i)
                        token = ''
                    isComent1 = True
                elif(caracter == '/'):
                    if(token != ''):
                        self.verificarToken(i)
                        token = ''
                    isComent2 = True

                elif(caracter in delimitador):
                    if(isVerificarDuplicidade):
                        if(simbolo == '<' and (caracter == '=' or caracter == '>')):
                            token = simbolo + caracter
                            tokens.append(Token(token, 'duplo', i))
                            token = ''
                        elif((simbolo == '>' or simbolo == ':') and caracter == '='):
                            token = simbolo + caracter
                            tokens.append(Token(token, 'duplo', i))
                            token = ''
                        else:
                            tokens.append(Token(simbolo, 'simples', i))
                            if(caracter != ' ' and caracter != '\n' and caracter != '\t'):
                                token = token + caracter
                        isVerificarDuplicidade = False
                        simbolo = ''
                    elif(caracter == '<' or caracter == '>' or caracter == ':'):
                        isVerificarDuplicidade = True
                        simbolo = caracter
                        if(token != ''):
                            self.verificarToken(i)
                            token = ''
                    elif(caracter == '.'):
                        token = token + '.'
                    else:
                        if(token != ''):
                            self.verificarToken(i)
                            token = ''
                        if(caracter != '\n' and caracter != ' ' and caracter != '\t'):
                            tokens.append(Token(caracter, 'simples', i))
                else:
                    if(simbolo != ''):
                        tokens.append(Token(simbolo, 'simples', i))
                        simbolo = ''
                    token = token + caracter
                    isVerificarDuplicidade = False
        return tokens


    def imprimeTokens(self, tokens):
        for t in tokens:
            print('valor: ' + str(t.valor) + ' tipo: ' + str(t.tipo) + ' linha: ' + str(t.linha+1) + '\n')
