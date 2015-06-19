import time
import os

class Transacao(object):
    def __init__(self, nomeDaTransacao):
        self.nomeDaTransacao = nomeDaTransacao
        if(os.name == 'nt'): #se for Windows
            self.timeStampDaTransacao = time.clock()
        else: #se for Linux ou outro
            self.timeStampDaTransacao = time.time()
    def __cmp__(self, other):
        return cmp(self.timeStampDaTransacao, other.timeStampDaTransacao)