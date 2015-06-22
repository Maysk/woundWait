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
                    operacao.transacaoResponsavel.inserirNoWaitFor(objeto.transacaoXLock)

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
                self.addInTransacoesComExclusiveLock(operacao)

            elif(objeto.isExclusiveLocked()):
                comparacaoDasTransacoes = cmp(operacao.transacaoResponsavel, objeto.transacaoXLock)
                if(comparacaoDasTransacoes == -1):  # wound
                    self.transacoesCanceladas.append(objeto.transacaoXLock)
                    objeto.transacaoXLock = operacao.transacaoResponsavel
                    self.addInTransacoesComExclusiveLock(operacao)

                elif(comparacaoDasTransacoes == 1): # wait
                    objeto.listaDeEspera.append(operacao.transacaoResponsavel)
                    operacao.transacaoResponsavel.isWaiting = True
                    self.transacoesEmWait[operacao.transacaoResponsavel] = operacao.objetoDaOperacao
                    operacao.transacaoResponsavel.inserirNoWaitFor(objeto.transacaoXLock)

                else:   # Precisa colocar algo aqui?
                    pass

            else:
                objeto.listaDeBloqueioCompartilhado.sort(reverse = True)
                tamanhoDaListaDeBloqueioCompartilhado = len(objeto.listaDeBloqueioCompartilhado)

                indexM = -1

                for i in range(tamanhoDaListaDeBloqueioCompartilhado):
                    comparacaoDasTransacoes = cmp(operacao.transacaoResponsavel, objeto.listaDeBloqueioCompartilhado[i])
                    if(comparacaoDasTransacoes == -1):
                        self.transacoesCanceladas.append(objeto.listaDeBloqueioCompartilhado[i])
                        indexM = i
                    if(comparacaoDasTransacoes == 0):
                        indexM = i
                
                if(tamanhoDaListaDeBloqueioCompartilhado == 0):
                    objeto.transacaoXLock = operacao.transacaoResponsavel
                    self.addInTransacoesComExclusiveLock(operacao)

                else:
                    if(indexM == -1):
                        objeto.listaDeEspera.append(operacao.transacaoResponsavel)
                        operacao.transacaoResponsavel.isWaiting = True
                        self.transacoesEmWait[operacao.transacaoResponsavel] = operacao.objetoDaOperacao
                        operacao.transacaoResponsavel.inserirNoWaitFor(objeto.listaDeBloqueioCompartilhado[0])
                    else:
                        comparacaoDasTransacoes = cmp(operacao.transacaoResponsavel, objeto.listaDeBloqueioCompartilhado[indexM])
                        if(comparacaoDasTransacoes == 0 and indexM == tamanhoDaListaDeBloqueioCompartilhado - 1):
                            del objeto.listaDeBloqueioCompartilhado[indexM]
                            objeto.transacaoXLock = operacao.transacaoResponsavel
                            self.transacoesComSharedLock[operacao.transacaoResponsavel].remove(operacao.objetoDaOperacao)
                            self.addInTransacoesComExclusiveLock(operacao)
                        elif(comparacaoDasTransacoes == -1 and indexM == tamanhoDaListaDeBloqueioCompartilhado - 1):
                            objeto.transacaoXLock = operacao.transacaoResponsavel
                            self.addInTransacoesComExclusiveLock(operacao)
                        else:
                            objeto.listaDeEspera.append(operacao.transacaoResponsavel)
                            operacao.transacaoResponsavel.isWaiting = True
                            self.transacoesEmWait[operacao.transacaoResponsavel] = operacao.objetoDaOperacao
                            operacao.transacaoResponsavel.inserirNoWaitFor(objeto.listaDeBloqueioCompartilhado[indexM+1])
                            
        except KeyError:
            objeto = Objeto()
            objeto.transacaoXLock = operacao.transacaoResponsavel
            self.objetosGerenciados[operacao.objetoDaOperacao] = objeto
            self.addInTransacoesComExclusiveLock(operacao)

    def addInTransacoesComSharedLock(self,operacao):
        if(operacao.transacaoResponsavel in self.transacoesComSharedLock):
            self.transacoesComSharedLock[operacao.transacaoResponsavel].append(operacao.objetoDaOperacao)
        else:
            self.transacoesComSharedLock[operacao.transacaoResponsavel] = []
            self.transacoesComSharedLock[operacao.transacaoResponsavel].append(operacao.objetoDaOperacao)

    def addInTransacoesComExclusiveLock(self,operacao):
        if(operacao.transacaoResponsavel in self.transacoesComExclusiveLock):
            self.transacoesComExclusiveLock[operacao.transacaoResponsavel].append(operacao.objetoDaOperacao)
        else:
            self.transacoesComExclusiveLock[operacao.transacaoResponsavel] = []
            self.transacoesComExclusiveLock[operacao.transacaoResponsavel].append(operacao.objetoDaOperacao)
