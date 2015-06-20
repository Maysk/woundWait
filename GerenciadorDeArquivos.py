import Operacao
import Transacao
import os.path

class GerenciadorDeArquivos:
    def __init__(self):
        pass
    
    
    def lerEntrada(self, nomeArquivoEntrada = 'historiaEntrada.luke'):
        listaTransacoes = [] #retorno do metodo
        if(os.path.isfile(nomeArquivoEntrada)):#se o arquivo existe
            
            
            arquivoEntrada = open(nomeArquivoEntrada,'r')
        
            print '\n',arquivoEntrada.read()
        
        
        
            arquivoEntrada.close()
            
        else:
            print "Arquivo nao existe!"
        
        return listaTransacoes
    
    
    def escreverSaida(self, historiaSaida, nomeArquivoSaida = 'historiaSaida.luke' ):
        arquivoSaida = open(nomeArquivoSaida,'w')
        
        arquivoSaida.write('huehuehuehue')
        
        arquivoSaida.close()