from Transacao import Transacao
from Operacao import Operacao
from GerenciadorDeBloqueio import GerenciadorDeBloqueio
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Desenho import *
import sys

class Escalonador(object):
    def __init__(self, listaDeTransacoes, historiaEntrada = []):
        self.listaDeTransacoes = listaDeTransacoes
        self.grafoDeEspera = '' # String marcando o Wait For Graph
        self.lockMan = GerenciadorDeBloqueio()
        self.nOperacoesRealizadas = 0
        self.nOperacoesTotais= 0
        self.indiceHistoriaEntrada = 0

        if(not historiaEntrada):#esta vazia
            self.historiaEntrada = []
            #Criar historia de forma ciclica
            for t in self.listaDeTransacoes:
                self.nOperacoesTotais += len(t.listaDeOperacoes)
            while(len(self.historiaEntrada) != self.nOperacoesTotais):
                for t in self.listaDeTransacoes:
                    if(t.indiceProximaOperacao < len(t.listaDeOperacoes)):
                        self.historiaEntrada.append(t.listaDeOperacoes[t.indiceProximaOperacao])
                        t.indiceProximaOperacao = t.indiceProximaOperacao + 1
            for t in self.listaDeTransacoes:
                t.indiceProximaOperacao = 0
        else:
            self.nOperacoesTotais = len(historiaEntrada)
            self.historiaEntrada = historiaEntrada #Lista de Operacoes


        self.historiaSaida = []





    def escalona(self):
        while(self.indiceHistoriaEntrada < self.nOperacoesTotais):
            proximaOperacao = self.historiaEntrada[self.indiceHistoriaEntrada]
            self.realizarOperacao(proximaOperacao)
            proximaOperacao.transacaoResponsavel.indiceDaUltimaOperacaoNaHistoria = proximaOperacao.transacaoResponsavel.indiceDaUltimaOperacaoNaHistoria + 1
            self.indiceHistoriaEntrada = self.indiceHistoriaEntrada + 1



    def realizarOperacao(self, operacao):
        t = operacao.transacaoResponsavel
        if(not t.isWaiting):
            if(operacao.tipoDeOperacao == 'c'):
                t.isOver = True
                self.nOperacoesRealizadas = self.nOperacoesRealizadas + 1
                t.indiceProximaOperacao = t.indiceProximaOperacao + 1
                self.historiaSaida.append(operacao)
                self.liberarBloqueios(t)
            elif(operacao.tipoDeOperacao=='r'):
                self.lockMan.pedirBloqueioCompartilhado(operacao)
            elif(operacao.tipoDeOperacao=='w'):
                self.lockMan.pedirBloqueioExclusivo(operacao)

            if(self.lockMan.transacoesCanceladas):
                tamanhoDaListaDeCanceladas = len(self.lockMan.transacoesCanceladas)
                for index in range(tamanhoDaListaDeCanceladas):
                    transacaoCancelada = self.lockMan.transacoesCanceladas[0]
                    del self.lockMan.transacoesCanceladas[0]
                    self.rollbackTransacao(transacaoCancelada)
                    self.reiniciarTransacao(transacaoCancelada)

            if(not t.isWaiting and not t.isOver):
                self.nOperacoesRealizadas = self.nOperacoesRealizadas + 1
                t.indiceProximaOperacao = t.indiceProximaOperacao + 1
                self.historiaSaida.append(operacao)


    def reiniciarTransacao(self, transacao):
        while(transacao.indiceProximaOperacao<= transacao.indiceDaUltimaOperacaoNaHistoria and not transacao.isWaiting):
            self.realizarOperacao(transacao.listaDeOperacoes[transacao.indiceProximaOperacao])





    def rollbackTransacao(self, transacao):
        self.liberarBloqueios(transacao)
        self.nOperacoesRealizadas = self.nOperacoesRealizadas - transacao.indiceProximaOperacao
        transacao.indiceProximaOperacao = 0
        transacao.isWaiting = False
        op = Operacao('abort',"")
        op.transacaoResponsavel = transacao
        self.historiaSaida.append(op)

    def liberarBloqueios(self, transacao):
        self.liberarSLocksDaTransacao(transacao)
        self.liberarXLocksDaTransacao(transacao)
        self.liberarWaits(transacao)


    def liberarSLocksDaTransacao(self,transacao):
        if(transacao in self.lockMan.transacoesComSharedLock):
            SLockList = self.lockMan.transacoesComSharedLock[transacao]
            del self.lockMan.transacoesComSharedLock[transacao]
            for obj in SLockList:
                objeto = self.lockMan.objetosGerenciados[obj]
                objeto.listaDeBloqueioCompartilhado.remove(transacao)
                objeto.listaDeEspera.sort()
                if(objeto.listaDeEspera):
                    t = objeto.listaDeEspera[0]
                    del objeto.listaDeEspera[0]
                    del self.lockMan.transacoesEmWait[t]
                    t.isWaiting = False
                    objeto.transacaoXLock = None
                    while(t.indiceProximaOperacao<t.indiceDaUltimaOperacaoNaHistoria and not t.isWaiting):
                        self.realizarOperacao(t.listaDeOperacoes[t.indiceProximaOperacao])


    def liberarXLocksDaTransacao(self,transacao):
        if(transacao in self.lockMan.transacoesComExclusiveLock):
            XLockList = self.lockMan.transacoesComExclusiveLock[transacao]
            del self.lockMan.transacoesComExclusiveLock[transacao]
            for obj in XLockList:
                objeto = self.lockMan.objetosGerenciados[obj]
                objeto.transacaoXLock = None
                objeto.listaDeEspera.sort()
                if(objeto.listaDeEspera):
                    t = objeto.listaDeEspera[0]
                    proximaOperacaoDaTransacaoMaisVelha = t.listaDeOperacoes[t.indiceProximaOperacao]
                    if(proximaOperacaoDaTransacaoMaisVelha.tipoDeOperacao == 'w'):
                        t.isWaiting = False
                        del objeto.listaDeEspera[0]
                        del self.lockMan.transacoesEmWait[t]
                        while(t.indiceProximaOperacao<t.indiceDaUltimaOperacaoNaHistoria and not t.isWaiting):
                            self.realizarOperacao(t.listaDeOperacoes[t.indiceProximaOperacao])

                    elif(proximaOperacaoDaTransacaoMaisVelha.tipoDeOperacao == 'r'):
                        tamanhoDaLista = len(objeto.listaDeEspera)
                        indice = 0
                        while(proximaOperacaoDaTransacaoMaisVelha != 'w' and indice < tamanhoDaLista):
                            t = objeto.listaDeEspera[0]
                            t.isWaiting = False
                            indice = indice + 1
                            del objeto.listaDeEspera[0]
                            del self.lockMan.transacoesEmWait[t]
                            while(t.indiceProximaOperacao < t.indiceDaUltimaOperacaoNaHistoria and not t.isWaiting):
                                self.realizarOperacao(t.listaDeOperacoes[t.indiceProximaOperacao])

    def liberarWaits(self,transacao):
        if(transacao in self.lockMan.transacoesEmWait):
            KeyObjetoEsperado = self.lockMan.transacoesEmWait[transacao]
            objetoEsperado = self.lockMan.objetosGerenciados[KeyObjetoEsperado]
            del self.lockMan.transacoesEmWait[transacao]
            objetoEsperado.listaDeEspera.remove(transacao)
            transacao.isWaiting = False


    def showTable(self):
        app = QApplication(sys.argv)
        table = QTableWidget()
        tableItem = QTableWidgetItem()

        table.setWindowTitle("Trabalho 2 - Escalonador")

        largura = len(self.listaDeTransacoes)*100+30
        altura = len(self.historiaSaida)*30+30
        if(altura > 900):
            altura = 900

        table.resize(largura,altura)
        table.setRowCount(len(self.historiaSaida))
        table.setColumnCount(len(self.listaDeTransacoes))

        #Criacao das labels da tabela:
        labelsTransacoes = ''
        for t in self.listaDeTransacoes:
            labelsTransacoes = labelsTransacoes + t.nomeDaTransacao + ';'

        table.setHorizontalHeaderLabels(QString(labelsTransacoes).split(";"))

        #Loop do preenchimento da tabela:
        linha = 0
        for operacao in self.historiaSaida:
            nomeOperacao = operacao.tipoDeOperacao
            if(operacao.tipoDeOperacao == 'w'):
                nomeOperacao ='write'                
                
            if(operacao.tipoDeOperacao == 'r'):                
                nomeOperacao = 'read'
            if(operacao.tipoDeOperacao == 'c'):                
                nomeOperacao = 'commit'
                
            itemInserido = QTableWidgetItem(nomeOperacao + '(' + operacao.objetoDaOperacao + ')')    
                
            #Parte das cores das operacoes:
            if(nomeOperacao == 'commit'):
                itemInserido.setTextColor(QColor(0,128,0))
            if(nomeOperacao == 'abort'):
                itemInserido.setTextColor(QColor(220,20,60))

            indiceTransacao = self.listaDeTransacoes.index(operacao.transacaoResponsavel)
            
            
            table.setItem(linha,indiceTransacao,itemInserido)

            linha = linha + 1
    
        grafo = Desenho(self.listaDeTransacoes, waitForGraph =[])
        grafo.show()
        table.show()
        return app.exec_()