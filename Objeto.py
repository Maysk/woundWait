
class Objeto:
    def __init__(self):
        self.listaDeEspera = []
        self.listaDeBloqueioCompartilhado = []
        self.isSBlock = False
        self.isXBlock = False
        self.opXBlock = None

    def avaliarOperacao(self, operacao):

        if(operacao.tipoDeOperacao == 'r'):
            self.listaDeBloqueioCompartilhado.append(operacao)
            self.listaDeBloqueioCompartilhado.sort()
            self.isSBlock = True
        elif(operacao.tipoDeOperacao == 'w'):
            self.opXBlock = operacao
            self.isXBlock = True

