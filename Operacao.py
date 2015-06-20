class Operacao(object):

    def __init__(self, tipoDeOperacao, objetoDaOperacao = ''):
        '''
        Construtor da classe Operacao
            Entradas:
            -tipoDeOperacao: string write/read/commit/...
            -objetoDaOperacao = '': string mostrando o objeto que sofre a transacao, como 'X', 'Y',...
        '''

        self.tipoDeOperacao = tipoDeOperacao    
        self.objetoDaOperacao = objetoDaOperacao
        self.transacaoResponsavel = None


    def setTransacaoResponsavel(self, transacaoResponsavel):
        self.transacaoResponsavel = transacaoResponsavel

    def __cmp__(self, other):
        return cmp(self.transacaoResponsavel, other.transacaoResponsavel)






    #def causaConflito(self,outraOperacao):
    #   if((self.tipoDeOperacao == 'write' or outraOperacao.tipoDeOperacao == 'write') and self.transacaoReponsavel.nomeDaTransacao != outraOperacao.transacaoReponsavel.nomeDaTransacao and self.objetoDaTransacao == outraOperacao.objetoDaTransacao):
    #      return True
    # return False
    #mudar causaConflito para o Gerenciador de Bloqueio
    