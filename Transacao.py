import time
import os

class Transacao(object):
    '''Classe Transacao
        Classe responsavel por representar uma transacao no trabalho.
        O construtor recebe o nome da transacao e se colocam operacoes na transacao atraves dos metodos:
         -adicionarOperacao(operacao): adiciona uma operacao individualmente
         -setListaDeOperacoes(list): inicializa a lista de operacoes com a entrada
    '''
    def __init__(self, nomeDaTransacao):
        '''Construtor da classe Transacao
            Entradas:
            -nomeDaTransacao: string que identifica a transacao, como 'T1'/'Transacao 2'/...
        '''
        self.nomeDaTransacao = nomeDaTransacao
        self.listaDeOperacoes = []
        self.indiceProximaOperacao = 0
        self.isWaiting = False
        if(os.name == 'nt'): #se for Windows
            self.timeStampDaTransacao = time.clock()
        else: #se for Linux ou outro
            self.timeStampDaTransacao = time.time()


    def __cmp__(self, other):
        return cmp(self.timeStampDaTransacao, other.timeStampDaTransacao)

    def adicionarOperacao(self, operacao):
        operacao.transacaoResponsavel = self
        self.listaDeOperacoes.append(operacao)

    def setListaDeOperacoes(self, listaDeOperacoes):
        self.listaDeOperacoes = listaDeOperacoes


    def abort(self):
        return None

