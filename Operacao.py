class Operacao(object):
    def __init__(self, tipoDeOperacao, transacaoResposavel, objetoDaTransacao):
        self.tipoDeOperacao = tipoDeOperacao
        self.transacaoReponsavel = transacaoResposavel
        self.objetoDaTransacao = objetoDaTransacao
    def causaConflito(self,outraOperacao):
        if((self.tipoDeOperacao == 'write' or outraOperacao.tipoDeOperacao == 'write') and self.transacaoReponsavel != outraOperacao.transacaoReponsavel and self.objetoDaTransacao == outraOperacao.objetoDaTransacao):
            return True
        return False
