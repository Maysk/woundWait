
class Objeto:
    def __init__(self):
        self.listaDeEspera = []
        self.listaDeBloqueioCompartilhado = []
        self.transacaoXLock = None

    def isSharedLocked(self):
        if( len(self.listaDeBloqueioCompartilhado) != 0):
            return True
        else:
            return False

    def isExclusiveLocked(self):
        if(self.transacaoXLock != None):
            return True
        else:
            return False


