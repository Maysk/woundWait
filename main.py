from Transacao import Transacao
from Operacao import Operacao
from Escalonador import Escalonador

t1 = Transacao("t1")
t2 = Transacao("t2")
t3 = Transacao("t3")

e1 = Escalonador([])

op1 = Operacao('w','t1','x')
op2 = Operacao('r','t1','x')
op3 = Operacao('w','t2','x')
op4 = Operacao('r','t3','y')

print "t1: ", t1.timeStampDaTransacao
print "t2: ", t2.timeStampDaTransacao
print "t3: ", t3.timeStampDaTransacao

print "Compara t1 e t2",cmp(t1,t2)
print "Compara t1 e t3",t1.__cmp__(t3)
print "Compara t2 e t3",cmp(t2,t3)

