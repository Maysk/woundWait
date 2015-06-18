from Transacao import Transacao

t1 = Transacao("t1")
t2 = Transacao("t2")
t3 = Transacao("t3")

print "t1: ", t1.timeStampDaTransacao
print "t2: ", t2.timeStampDaTransacao
print "t3: ", t3.timeStampDaTransacao

print "Compara t1 e t2",cmp(t1,t2)
print "Compara t1 e t3",cmp(t1,t3)
print "Compara t2 e t3",cmp(t2,t3)

print "Teste"