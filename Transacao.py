import time

class Transacao(object):
    def __init__(self, nomeDaTransacao):
        self.nomeDaTransacao = nomeDaTransacao
        self.timeStampDaTransacao = time.time()
    def __cmp__(self, other):
        return cmp(self.timeStampDaTransacao, other.timeStampDaTransacao)