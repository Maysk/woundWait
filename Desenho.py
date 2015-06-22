from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Transacao import Transacao

class Vertice(object):
    
    def __init__(self,raio,texto,x,y):
        self.raio = raio
        self.texto = QString(texto)
        self.x = x
        self.y = y
    
    def drawVertice(self,painter):
        painter.drawEllipse(self.x,self.y,self.raio,self.raio)
        painter.drawText((self.x+self.raio/2)-5,(self.y+self.raio/2)+5,self.texto)
        
class Aresta(object):
    def __init__(self,verticeOrigem,verticeDestino):
        self.verticeOrigem = verticeOrigem
        self.verticeDestino = verticeDestino
        
    def drawAresta(self,painter):
        
        x1=self.verticeOrigem.x+self.verticeOrigem.raio/2
        y1=self.verticeOrigem.y+self.verticeOrigem.raio/2
        x2=self.verticeDestino.x+self.verticeDestino.raio/2
        y2=self.verticeDestino.y+self.verticeDestino.raio/2
        raio = self.verticeDestino.raio
        p1 = QPoint(0,0)
        p2 = QPoint(0,0)
        p3 = QPoint(0,0)
        
        
        if(x1<x2 and y1<y2):
            x1 = x1 + raio/3
            y1 = y1 + raio/3
            x2 = x2 - raio/3
            y2 = y2 - raio/3
            p2.setX(x2)
            p2.setY(y2)
            p1.setX(x2)
            p1.setY(y2-12)
            p3.setX(x2-12)
            p3.setY(y2)
        elif(x1>x2 and y1<y2):
            x1 = x1 - raio/3
            y1 = y1 + raio/3
            x2 = x2 + raio/3
            y2 = y2 - raio/3
            p2.setX(x2)
            p2.setY(y2)
            p1.setX(x2+12)
            p1.setY(y2)
            p3.setX(x2)
            p3.setY(y2-12)
        elif(x1<x2 and y1>y2):
            x1 = x1 + raio/3
            y1 = y1 - raio/3
            x2 = x2 - raio/3
            y2 = y2 + raio/3
            p2.setX(x2)
            p2.setY(y2)
            p1.setX(x2-12)
            p1.setY(y2)
            p3.setX(x2)
            p3.setY(y2+12)
        elif(x1>x2 and y1>y2):
            x1 = x1 - raio/3
            y1 = y1 - raio/3
            x2 = x2 + raio/3
            y2 = y2 + raio/3
            p2.setX(x2)
            p2.setY(y2)
            p1.setX(x2)
            p1.setY(y2+12)
            p3.setX(x2+12)
            p3.setY(y2)
        elif(x1==x2 and y1<y2):
            y1 = y1 + raio/2.15
            y2 = y2 - raio/2.15
            p2.setX(x2)
            p2.setY(y2)
            p1.setX(x2-12)
            p1.setY(y2-12)
            p3.setX(x2+12)
            p3.setY(y2-12)
        elif(x1==x2 and y1>y2):
            y1 = y1 - raio/2.15
            y2 = y2 + raio/2.15
            p2.setX(x2)
            p2.setY(y2)
            p1.setX(x2+12)
            p1.setY(y2+12)
            p3.setX(x2-12)
            p3.setY(y2+12)
        elif(x1>x2 and y1==y2):
            x1 = x1 - raio/2.15
            x2 = x2 + raio/2.15
            p2.setX(x2)
            p2.setY(y2)
            p1.setX(x2+12)
            p1.setY(y2+12)
            p3.setX(x2+12)
            p3.setY(y2-12)
        elif(x1<x2 and y1==y2):
            x1 = x1 + raio/2.15
            x2 = x2 - raio/2.15
            p2.setX(x2)
            p2.setY(y2)
            p1.setX(x2-12)
            p1.setY(y2-12)
            p3.setX(x2-12)
            p3.setY(y2+12)
        
        #Desenhar aresta:
        painter.drawLine(x1,y1,x2,y2)
        
        #Desenhar orientacao (nao terminada para x1==x1 ou y1==y2
        painter.setBrush(Qt.black)
        painter.drawPolygon(p1,p2,p3)
        

class Desenho(QWidget):

    def __init__(self, listaTransacoes,parent=None):
        QWidget.__init__(self, parent)
        # setGeometry(x_pos, y_pos, width, height)    
        altura = 100 + len(listaTransacoes)/2*200
        if(len(listaTransacoes)%2 != 0):
            altura = altura + 200
        largura = 750    
        self.setGeometry(200, 200, largura, altura)
        self.setWindowTitle('Wait-Fot Graph')
        self.listaTransacoes = listaTransacoes
    
    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        
        paint.setRenderHint(QPainter.Antialiasing)
        #background branco:
        paint.setBrush(Qt.white)
        paint.drawRect(event.rect())
        
        paint.setPen(Qt.black)

        listaVertices = []
        listaArestas = []
        
        i=0
        tipoLinha = 0 #0 para linha par, 1 para linha impar
        altura=100
        while (i < len(self.listaTransacoes)):
            
            if(tipoLinha%2 == 0):
                V = Vertice(100,self.listaTransacoes[i].nomeDaTransacao,100,altura)
                listaVertices.append(V)
                i = i + 1
                if(i < len(self.listaTransacoes)):
                    V = Vertice(100,self.listaTransacoes[i].nomeDaTransacao,400,altura)
                    listaVertices.append(V)
                    i = i + 1
                    altura = altura + 200
            else:
                V = Vertice(100,self.listaTransacoes[i].nomeDaTransacao,250,altura)
                listaVertices.append(V)
                i = i + 1
                if(i < len(self.listaTransacoes)):                    
                    V = Vertice(100,self.listaTransacoes[i].nomeDaTransacao,550,altura)
                    listaVertices.append(V)
                    i = i + 1
                    altura = altura + 200
                    
            tipoLinha = tipoLinha + 1
            
        #Criacao das arestas:        
        Vertice1 = None
        Vertice2 = None
        
        for t in self.listaTransacoes:
            if(len(t.waitFor) != 0):
                for vertice in listaVertices:
                    if(t.nomeDaTransacao == vertice.texto):
                        Vertice1 = vertice
                for transacao in t.waitFor:
                    for vertice2 in listaVertices:
                        if(transacao.nomeDaTransacao == vertice2.texto):
                            Vertice2 = vertice2
                            listaArestas.append(Aresta(Vertice1, Vertice2))   
    
        #cor:
        paint.setBrush(QColor(99,184,255))
        #Desenho em si:
        for vertice in listaVertices:
            vertice.drawVertice(paint)            

        for aresta in listaArestas:
            aresta.drawAresta(paint)

        paint.end()
        
        
        