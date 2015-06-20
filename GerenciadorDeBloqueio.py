from Transacao import Transacao
from Operacao import Operacao
from Objeto import Objeto

class GerenciadorDeBloqueio:
    def __init__(self):
        self.objetosGerenciados = {}

    def pedirBloqueioCompartilhado(self, operacao):
        #if(operacao.objetoDaOperacao in self.objetosGerenciados):
        try:
            objetoDesejado = self.objetosGerenciados[operacao.objetoDaOperacao]
        except KeyError:
            novoObjeto = Objeto()
            self.objetosGerenciados[operacao.objetoDaOperacao] = novoObjeto

