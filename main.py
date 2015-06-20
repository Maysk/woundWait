from Transacao import Transacao
from Operacao import Operacao
from Escalonador import Escalonador


t1 = Transacao("Transacao 1")
t2 = Transacao("Transacao 2")
t3 = Transacao("Transacao 3")

op1 = Operacao('write','X')
op2 = Operacao('read','X')
op3 = Operacao('write','Z')
op4 = Operacao('commit')
op5 = Operacao('abort')

t1.setListaDeOperacoes([op1, op2, op5])
t2.setListaDeOperacoes([op3])
t3.setListaDeOperacoes([op4])

e1 = Escalonador([t1,t2,t3]) #exemplo inutil, claro

print t1, "\n", t2, "\n", t3

listaDeTransacoes = [t2,t1,t3]
print listaDeTransacoes
listaDeTransacoes.sort()
print listaDeTransacoes

print "t1: ", t1.timeStampDaTransacao
print "t2: ", t2.timeStampDaTransacao
print "t3: ", t3.timeStampDaTransacao

print "Compara t1 e t2",cmp(t1,t2)
print "Compara t1 e t3",t1.__cmp__(t3)
print "Compara t2 e t3",cmp(t2,t3)

e1.showTable()

