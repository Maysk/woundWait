from Operacao import Operacao
from Transacao import Transacao
import os.path

class GerenciadorDeArquivos:
    def __init__(self):
        pass
    
    
    def lerEntrada(self, nomeArquivoEntrada = 'historiaEntrada.luke'):
        listaTransacoes = [] #retorno do metodo
        historiaCustomizada = [] #retorno do metodo
        if(os.path.isfile(nomeArquivoEntrada)):#se o arquivo existe            
            arquivoEntrada = open(nomeArquivoEntrada,'r')
        
            linhas = arquivoEntrada.readlines()
            l = 0
                           
            #Leitura:
            while(linhas[l] != '\n'):
                #ler transacao da linha atual:
                transacaoAtual = Transacao(linhas[l].split(':')[0])
                
                operacoesDaTransacaoAtual = linhas[l].split(':')[1].split(';')
                
                for element in operacoesDaTransacaoAtual:
                    
                    operacao = Operacao(element.split('(')[0], element.split('(')[1].split(')')[0])
                    transacaoAtual.adicionarOperacao(operacao)
                
                listaTransacoes.append(transacaoAtual)
                l = l + 1

            l = l + 1 #pular a linha '\n'
                        
            #Ler a flag de HistoriaAutomatica
            if (linhas[l].split('=')[1] == 'True\n'):
                #Se a historia for gerada automaticamente, ignora o resto do arquivo
                pass                
            else:                
                #Senao, ler o resto do arquivo 
                historiaEntrada = linhas[l+2].split(';') #o +2 no indice e de pular a linha HistoriaAutomatica=<Bool> e de pular a linha '\n'
                
                for operacao in historiaEntrada:
                    tipoDaOperacao = operacao[0]
                    objetoDaOperacao = operacao.split('(')[1].split(')')[0]
                    nomeDaTransacao = 'T'+operacao.split(tipoDaOperacao)[1].split('(')[0]
                
                    operacaoAInserir = Operacao(tipoDaOperacao, objetoDaOperacao)
                    for t in listaTransacoes:
                        if(t.nomeDaTransacao == nomeDaTransacao):
                            operacaoAInserir.transacaoResponsavel = t
                    
                    historiaCustomizada.append(operacaoAInserir)                    
                
            arquivoEntrada.close()
            
        else:
            print "Arquivo de entrada nao existe!"
        
        return [listaTransacoes,historiaCustomizada]
    
    
    def escreverSaida(self, listaTransacoes,historiaEntrada,historiaSaida, nomeArquivoSaida = 'historiaSaida.luke' ):
        arquivoSaida = open(nomeArquivoSaida,'w')    
        
        arquivoSaida.write('Historia de Entrada: ')
        for operacao in historiaEntrada:
            arquivoSaida.write(operacao.tipoDeOperacao + operacao.transacaoResponsavel.nomeDaTransacao.replace('T','')+'('+operacao.objetoDaOperacao+')')
        arquivoSaida.write('\nHistoria de Saida: ')
        for operacao in historiaSaida:
            if(operacao.tipoDeOperacao == 'abort'):
                arquivoSaida.write('rollback' + operacao.transacaoResponsavel.nomeDaTransacao.replace('T','')+'('+operacao.objetoDaOperacao+')')
            else:
                arquivoSaida.write(operacao.tipoDeOperacao + operacao.transacaoResponsavel.nomeDaTransacao.replace('T','')+'('+operacao.objetoDaOperacao+')')        
        arquivoSaida.write('\nDeadlock: Nao\n')
        arquivoSaida.write('Transacoes Abortadas:\n')
        arquivoSaida.write('Transacoes Efetivadas: ')
        for t in range(0,len(listaTransacoes)):
            arquivoSaida.write(listaTransacoes[t].nomeDaTransacao)
            if(t != (len(listaTransacoes)-1) ):
                arquivoSaida.write(',')
        
                pass
        
        arquivoSaida.close()