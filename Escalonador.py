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
        
        if(not historiaEntrada):    # esta vazia
            self.historiaEntrada = []
            # Criar historia de forma ciclica
            nOperacoes = 0
            for t in self.listaDeTransacoes:
                nOperacoes += len(t.listaDeOperacoes)

            while(len(self.historiaEntrada) != nOperacoes):
                for t in self.listaDeTransacoes:
                    if(t.indiceProximaOperacao < len(t.listaDeOperacoes) and not t.isWaiting):
                        proximaOperacao = t.listaDeOperacoes[t.indiceProximaOperacao]
                        if(proximaOperacao.tipoDeOperacao == 'c'):
                            self.historiaEntrada.append(proximaOperacao)
                            self.liberarBloqueios(proximaOperacao)

                        if(proximaOperacao.tipoDeOperacao=='r'):
                            self.lockMan.pedirBloqueioCompartilhado(proximaOperacao)
                        elif(proximaOperacao.tipoDeOperacao=='w'):
                            self.lockMan.pedirBloqueioExclusivo(proximaOperacao)
                        elif(proximaOperacao.tipoDeOperacao=='c'):
                            pass


                        self.historiaEntrada.append(proximaOperacao)
                        t.indiceProximaOperacao = t.indiceProximaOperacao + 1

            for t in self.listaDeTransacoes:
                t.indiceProximaOperacao = 0
        else: 		
            self.historiaEntrada = historiaEntrada #Lista de Operacoes
        
        self.historiaSaida = self.historiaEntrada #inicializacao de teste, a historiaSaida devera ser uma lista de operacoes, onde commit e abort tambem sao operacoes
        self.gerenciadorDeBloqueio = None #Criar classe    
    
    
    def liberarBloqueios(self,transacao):
        if(transacao in self.lockMan.transacoesComSharedLock):
            SLockList = self.lockMan.transacoesComSharedLock[transacao]

        if(transacao in self.lockMan.transacoesComExclusiveLock):
            XLockList = self.lockMan.transacoesComExclusiveLock[transacao]


        for obj in SLockList:
            objeto = self.lockMan.objetosGerenciados[obj]
            objeto.listaDeBloqueioCompartilhado.remove(transacao)
            objeto.listaDeEspera.sort()

        for obj in XLockList:
            objeto = self.lockMan.objetosGerenciados[obj]
            objeto.transacaoXLock = None
            objeto.listaDeEspera.sort()


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
        
        
