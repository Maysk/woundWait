from Transacao import Transacao
from Operacao import Operacao
from Escalonador import Escalonador
from GerenciadorDeArquivos import GerenciadorDeArquivos



ioHandler = GerenciadorDeArquivos()

[listaDeTransacoes, historiaEntrada] = ioHandler.lerEntrada()

e1 = Escalonador(listaDeTransacoes,historiaEntrada)
e1.escalona()
ioHandler.escreverSaida(e1.listaDeTransacoes,e1.historiaEntrada,e1.historiaSaida)
e1.showTable()


