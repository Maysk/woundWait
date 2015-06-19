from Transacao import Transacao
from Operacao import Operacao
from Escalonador import Escalonador

t1 = Transacao("t1")
t2 = Transacao("t2")
t3 = Transacao("t3")

op1 = Operacao('write','t1','X')
op2 = Operacao('read','t1','X')
op3 = Operacao('write','t2','Z')
op4 = Operacao('commit','t3','')
op5 = Operacao('abort','t1','')

e1 = Escalonador([t1,t2,t3], [op1,op2,op3,op4,op5]) #exemplo inutil, claro

print "t1: ", t1.timeStampDaTransacao
print "t2: ", t2.timeStampDaTransacao
print "t3: ", t3.timeStampDaTransacao

print "Compara t1 e t2",cmp(t1,t2)
print "Compara t1 e t3",t1.__cmp__(t3)
print "Compara t2 e t3",cmp(t2,t3)

e1.showTable()