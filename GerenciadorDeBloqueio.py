from Transacao import Transacao
from Operacao import Operacao
from Objeto import Objeto


class GerenciadorDeBloqueio:
    def __init__(self):
        self.objetosGerenciados = {}  # Key: Nome do Objeto, Value: Objeto; Aqui vao ficar todos os objetos gerenciados
        self.transacoesComSharedLock = {}   # Key: Transacao, Value: Objetos
        self.transacoesComExclusiveLock = {}    # Key: Transacao, Value: Objetos
        self.transacoesEmWait = {}  # Key Transacao, Value: Objeto
        self.transacoesCanceladas = []  # transacoes canceladas

    def pedirBloqueioCompartilhado(self, operacao):
        try:
            objeto = self.objetosGerenciados[operacao.objetoDaOperacao]
            if(objeto.isExclusiveLocked()):
                comparacaoDasTransacoes = cmp(operacao.transacaoResponsavel, objeto.transacaoXLock)
                if(comparacaoDasTransacoes == -1): # wound
                    self.transacoesCanceladas.append(objeto.transacaoXLock)
                    objeto.transacaoXLock = None
                    objeto.listaDeBloqueioCompartilhado.append(operacao.transacaoResponsavel)
                    self.addInTransacoesComSharedLock(operacao)

                elif(comparacaoDasTransacoes == 1): # wait
                    objeto.listaDeEspera.append(operacao.transacaoResponsavel)
                    operacao.transacaoResponsavel.isWaiting = True
                    self.transacoesEmWait[operacao.transacaoResponsavel] = operacao.objetoDaOperacao

                else:   # comparacaoDasTransacoes == 0
                    pass
            # Caso ja exista um bloqueio compartilhado ou o objeto ta livre
            else:# Tenta achar a transacao na lista, caso ela nao exista ele adiciona
                if(operacao.transacaoResponsavel not in objeto.listaDeBloqueioCompartilhado):
                    objeto.listaDeBloqueioCompartilhado.append(operacao.transacaoResponsavel)
                    self.addInTransacoesComSharedLock(operacao)

        except KeyError:
            objeto = Objeto()
            objeto.listaDeBloqueioCompartilhado.append(operacao.transacaoResponsavel)
            self.objetosGerenciados[operacao.objetoDaOperacao] = objeto
            self.addInTransacoesComSharedLock(operacao)

    def pedirBloqueioExclusivo(self, operacao):
        try:
            objeto =  self.objetosGerenciados[operacao.objetoDaOperacao]
            if(not(objeto.isSharedLocked() or objeto.isExclusiveLocked())): #Objeto livre, sem locks
                objeto.transacaoXLock = operacao.transacaoResponsavel
                self.addInTrasacoesComExclusiveLock(operacao)

            elif(objeto.isExclusiveLocked()):
                comparacaoDasTransacoes = cmp(operacao.transacaoResponsavel, objeto.transacaoXLock)
                if(comparacaoDasTransacoes == -1):  # wound
                    self.transacoesCanceladas.append(objeto.transacaoXLock)
                    objeto.transacaoXLock = operacao.transacaoResponsavel
                    self.addInTrasacoesComExclusiveLock(operacao)

                elif(comparacaoDasTransacoes == 1): # wait
                    objeto.listaDeEspera.append(operacao.transacaoResponsavel)
                    operacao.transacaoResponsavel.isWaiting = True
                    self.transacoesEmWait[operacao.transacaoResponsavel] = operacao.objetoDaOperacao

                else:   # Precisa colocar algo aqui?
                    pass

            else:
                objeto.listaDeBloqueioCompartilhado.sort()
                tamanhoDaListaDeBloqueioCompartilhado = len(objeto.listaDeBloqueioCompartilhado)
                i = 0
                comparacaoDasTransacoes = -1
                while(i<tamanhoDaListaDeBloqueioCompartilhado and comparacaoDasTransacoes!=-1):
                    comparacaoDasTransacoes = cmp(operacao.transacaoResponsavel, objeto.listaDeBloqueioCompartilhado[i])
                    if(comparacaoDasTransacoes == -1):
                        self.transacoesCanceladas.append(objeto.listaDeBloqueioCompartilhado[i])

                    i=i+1

                tamanhoDaListaDeBloqueioCompartilhado = len(objeto.listaDeBloqueioCompartilhado)
                if(tamanhoDaListaDeBloqueioCompartilhado == 0):
                    objeto.transacaoXLock = operacao.transacaoResponsavel
                    self.addInTransacoesComSharedLock(operacao)

                elif(tamanhoDaListaDeBloqueioCompartilhado == 1):
                    comparacaoDasTransacoes = cmp(operacao.transacaoResponsavel, objeto.listaDeBloqueioCompartilhado[0])
                    if(comparacaoDasTransacoes == 0):
                        del objeto.listaDeBloqueioCompartilhado[0]
                        objeto.transacaoXLock = operacao.transacaoResponsavel
                        self.transacoesComSharedLock[operacao.transacaoResponsavel].remove(operacao.objetoDaOperacao)
                        self.addInTrasacoesComExclusiveLock(operacao)

                    else:
                        objeto.listaDeEspera.append(operacao.transacaoResponsavel)
                        operacao.transacaoResponsavel.isWaiting = True
                        self.transacoesEmWait[operacao.transacaoResponsavel] = operacao.objetoDaOperacao

                else:
                    objeto.listaDeEspera.append(operacao.transacaoResponsavel)
                    operacao.transacaoResponsavel.isWaiting = True
                    self.transacoesEmWait[operacao.transacaoResponsavel] = operacao.objetoDaOperacao

        except KeyError:
            objeto = Objeto()
            objeto.transacaoXLock = operacao.transacaoResponsavel
            self.objetosGerenciados[operacao.objetoDaOperacao] = objeto
            self.addInTrasacoesComExclusiveLock(operacao)

    def addInTransacoesComSharedLock(self,operacao):
        if(operacao.transacaoResponsavel in self.transacoesComSharedLock):
            self.transacoesComSharedLock[operacao.transacaoResponsavel].append(operacao.objetoDaOperacao)
        else:
            self.transacoesComSharedLock[operacao.transacaoResponsavel] = []
            self.transacoesComSharedLock[operacao.transacaoResponsavel].append(operacao.objetoDaOperacao)

    def addInTrasacoesComExclusiveLock(self,operacao):
        if(operacao.transacaoResponsavel in self.transacoesComSharedLock):
            self.transacoesComExclusiveLock[operacao.transacaoResponsavel].append(operacao.objetoDaOperacao)
        else:
            self.transacoesComSharedLock[operacao.transacaoResponsavel] = []
            self.transacoesComSharedLock[operacao.transacaoResponsavel].append(operacao.objetoDaOperacao)
