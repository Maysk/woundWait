from Transacao import Transacao
from Operacao import Operacao
from Escalonador import Escalonador
from GerenciadorDeArquivos import GerenciadorDeArquivos



ioHandler = GerenciadorDeArquivos()

[listaDeTransacoes, historiaEntrada] = ioHandler.lerEntrada()

e1 = Escalonador(listaDeTransacoes,historiaEntrada)
    
ioHandler.escreverSaida(e1.historiaSaida)
