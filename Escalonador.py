from Transacao import Transacao
from Operacao import Operacao
from GerenciadorDeBloqueio import GerenciadorDeBloqueio
from PyQt4.QtGui import * 
from PyQt4.QtCore import * 
import sys

class Escalonador(object):
    def __init__(self, listaDeTransacoes, historiaEntrada = []):
        self.listaDeTransacoes = listaDeTransacoes
        self.grafoDeEspera = '' # String marcando o Wait For Graph
        self.lockMan = GerenciadorDeBloqueio()
        self.nOperacoes = 0 ##
                            ##
                            ##
        if(not historiaEntrada):    # esta vazia
            self.historiaEntrada = []
            # Criar historia de forma ciclica
            for t in self.listaDeTransacoes:
                self.nOperacoes += len(t.listaDeOperacoes)

            while(len(self.historiaEntrada) != self.nOperacoes):
                for t in self.listaDeTransacoes:
                    if(t.indiceProximaOperacao < len(t.listaDeOperacoes) and not t.isWaiting and not t.isOver):
                        proximaOperacao = t.listaDeOperacoes[t.indiceProximaOperacao]
                        if(proximaOperacao.tipoDeOperacao == 'c'):
                            t.isOver = True
                            self.nOperacoes = self.nOperacoes + 1
                            self.historiaEntrada.append(proximaOperacao)
                            self.liberarBloqueios(proximaOperacao)

                        elif(proximaOperacao.tipoDeOperacao=='r'):
                            self.lockMan.pedirBloqueioCompartilhado(proximaOperacao)
                        elif(proximaOperacao.tipoDeOperacao=='w'):
                            self.lockMan.pedirBloqueioExclusivo(proximaOperacao)

                        if(self.lockMan.transacoesCanceladas):  #Se tiver alguma transacao em transacoes canceladas ele vai fazer o seguinte
                            for t in self.lockMan.transacoesCanceladas:
                                self.nOperacoes = self.nOperacoes - t.indiceProximaOperacao
                                self.rollbackTransacao(t)

                        if(not t.isWaiting):
                            self.nOperacoes = self.nOperacoes + 1
                            self.historiaEntrada.append(proximaOperacao)
                            t.indiceProximaOperacao = t.indiceProximaOperacao + 1


            for t in self.listaDeTransacoes:
                t.indiceProximaOperacao = 0
        else: 		
            self.historiaEntrada = historiaEntrada #Lista de Operacoes
        
        self.historiaSaida = self.historiaEntrada #inicializacao de teste, a historiaSaida devera ser uma lista de operacoes, onde commit e abort tambem sao operacoes
        self.gerenciadorDeBloqueio = None #Criar classe    
    

    def rollbackTransacao(self, transacao):
        self.liberarBloqueios(transacao)
        transacao.indiceProximaOperacao = 0
        transacao.isWaiting = False
        self.historiaEntrada.append("a"+transacao.nomeDaTransacao.split("T")[1]+"()")

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
                proximaOperacao = t.listaDeOperacoes[t.indiceProximaOperacao]
                objeto.transacaoXLock = t
                self.lockMan.addInTrasacoesComExclusiveLock(proximaOperacao)
                t.isWaiting = False
                self.nOperacoes = self.nOperacoes + 1
                self.historiaEntrada.append(proximaOperacao)
                t.indiceProximaOperacao = t.indiceProximaOperacao + 1


    #Funcao para liberar os XLocks feitos por uma transacao e
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
                    objeto.transacaoXLock = t
                    self.lockMan.addInTrasacoesComExclusiveLock(proximaOperacaoDaTransacaoMaisVelha)
                    t.isWaiting = False
                    self.nOperacoes = self.nOperacoes + 1
                    self.historiaEntrada.append(proximaOperacaoDaTransacaoMaisVelha)
                    t.indiceProximaOperacao = t.indiceProximaOperacao + 1
                    del objeto.listaDeEspera[0]
                    del self.lockMan.transacoesEmWait[t]

                elif(proximaOperacaoDaTransacaoMaisVelha.tipoDeOperacao == 'r'):
                    tamanhoDaLista = len(objeto.listaDeEspera)
                    indice = 0
                    while(proximaOperacaoDaTransacaoMaisVelha != 'w' and indice < tamanhoDaLista):
                        t = objeto.listaDeEspera[0]
                        objeto.listaDeBloqueioCompartilhado.append(t)
                        self.lockMan.addInTransacoesComSharedLock(proximaOperacaoDaTransacaoMaisVelha)
                        t.isWaiting = False
                        self.nOperacoes = self.nOperacoes + 1
                        self.historiaEntrada.append(proximaOperacaoDaTransacaoMaisVelha)
                        t.indiceProximaOperacao = t.indiceProximaOperacao + 1
                        indice = indice + 1
                        del objeto.listaDeEspera[0]
                        del self.lockMan.transacoesEmWait[t]

    def liberarWaits(self,transacao):
        if(transacao in self.lockMan.transacoesEmWait):
            objetoEsperado = self.lockMan.transacoesEmWait[transacao]
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
            
            itemInserido = QTableWidgetItem(operacao.tipoDeOperacao + '(' + operacao.objetoDaOperacao + ')')
            
            #Parte das cores das operacoes:
            if(operacao.tipoDeOperacao == 'commit'):
                itemInserido.setTextColor(QColor(0,128,0))
            if(operacao.tipoDeOperacao == 'abort'):
                itemInserido.setTextColor(QColor(220,20,60))
                
            #Identificar a transacao de cada operacao:
            indiceTransacao = 0
            for indiceIterativo in range(0,len(self.listaDeTransacoes)):
                if(operacao in self.listaDeTransacoes[indiceIterativo].listaDeOperacoes):
                    indiceTransacao = indiceIterativo
            
            table.setItem(linha,indiceTransacao,itemInserido)
                
            linha = linha + 1
        
        table.show()        
        return app.exec_()
        
        
