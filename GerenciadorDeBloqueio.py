from Transacao import Transacao
from Operacao import Operacao
from Objeto import Objeto


class GerenciadorDeBloqueio:
    def __init__(self):
        self.objetosGerenciados = {}    ##Key: Nome do Objeto, Value: Objeto
        self.transacoesComSharedLock = {}   ##Key: Transacao, Value: Objetos
        self.transacoesComExclusiveLock = {}    ##Key: Transacao, Value: Objetos
        self.transacoesEmWait = {}  ##Key Transacao, Value: Objeto


    def pedirBloqueioCompartilhado(self, operacao):
        try:
            objeto = self.objetosGerenciados[operacao.objetoDaOperacao]
            if(objeto.isExclusiveLocked()):
                comparacaoDasTransacoes = cmp(operacao.transacaoResponsavel, objeto.transacaoXLock)
                if(comparacaoDasTransacoes == -1):
                    objeto.transacaoXLock.transacaoResponsavel.abort()
                    objeto.transacaoXLock = None
                    objeto.listaDeBloqueioCompartilhado.append(operacao.transacaoResponsavel)
                elif(comparacaoDasTransacoes == 1):
                    objeto.listaDeEspera.append(operacao.transacaoResponsavel)
                    operacao.transacaoResponsavel.isWaiting = True
                else:
                    pass #Existe algo pra colocar aqui?

            #Caso ja exista um bloqueio compartilhado ou o objeto ta livre
            else:
                #Tenta achar a transacao na lista, caso ela nao exista ele adiciona
                try:
                    objeto.listaDeBloqueioCompartilhado.index(operacao.transacaoResponsavel)
                except ValueError:
                    objeto.listaDeBloqueioCompartilhado.append(operacao.transacaoResponsavel)

        except KeyError:
            objeto = Objeto()
            objeto.listaDeBloqueioCompartilhado.append(operacao.transacaoResponsavel)
            self.objetosGerenciados[operacao.objetoDaOperacao] = objeto



    def pedirBloqueioExclusivo(self, operacao):
        try:
            objeto =  self.objetosGerenciados[operacao.objetoDaOperacao]
            if(not(objeto.isSharedLocked() or objeto.isExclusiveLocked())): #Objeto livre, sem locks
                objeto.transacaoXLock = operacao.transacaoResponsavel

            elif(objeto.isExclusiveLocked()):
                comparacaoDasTransacoes = cmp(operacao.transacaoResponsavel, objeto.transacaoXLock)
                if(comparacaoDasTransacoes == -1):
                    objeto.transacaoXLock.transacaoResponsavel.abort()
                    objeto.transacaoXLock = operacao.transacaoResponsavel
                elif(comparacaoDasTransacoes == 1):
                    objeto.listaDeEspera.append(operacao.transacaoResponsavel)
                    operacao.transacaoResponsavel.isWaiting = True
                else:
                    pass # Precisa colocar algo aqui?
            else:
                objeto.listaDeBloqueioCompartilhado.sort()
                tamanhoDaListaDeBloqueioCompartilhado = len(objeto.listaDeBloqueioCompartilhado)
                i = 0
                comparacaoDasTransacoes = -1
                while(i<tamanhoDaListaDeBloqueioCompartilhado and comparacaoDasTransacoes!=-1):
                    comparacaoDasTransacoes = cmp(operacao.transacaoResponsavel, objeto.listaDeBloqueioCompartilhado[i])
                    if(comparacaoDasTransacoes == -1):
                        objeto.listaDeBloqueioCompartilhado[i].abort()

                    i=i+1

                tamanhoDaListaDeBloqueioCompartilhado = len(objeto.listaDeBloqueioCompartilhado)
                if(tamanhoDaListaDeBloqueioCompartilhado == 0):
                    objeto.transacaoXLock = operacao.transacaoResponsavel
                elif(tamanhoDaListaDeBloqueioCompartilhado == 1):
                    comparacaoDasTransacoes = cmp(operacao.transacaoResponsavel, objeto.listaDeBloqueioCompartilhado[0])
                    if(comparacaoDasTransacoes == 0):
                        del objeto.listaDeBloqueioCompartilhado[0]
                        objeto.transacaoXLock = operacao.transacaoResponsavel
                    else:
                        objeto.listaDeEspera.append(operacao.transacaoResponsavel)
                        operacao.transacaoResponsavel.isWaiting = True
                else:
                    objeto.listaDeEspera.append(operacao.transacaoResponsavel)
                    operacao.transacaoResponsavel.isWaiting = True

        except KeyError:
            objeto = Objeto()
            objeto.isXBlock = True
            objeto.transacaoXLock = operacao.transacaoResponsavel
            self.objetosGerenciados[operacao.objetoDaOperacao] = objeto





