from Transacao import Transacao

class Escalonador(object):
    def __init__(self, listaDeTransacoes):
        self.listaDeTransacoes = listaDeTransacoes
        self.grafoDeEspera = '' #String marcando o Wait For Graph
        #outros atributos