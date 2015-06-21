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
