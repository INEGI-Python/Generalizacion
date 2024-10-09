
import matplotlib.pyplot as plt 
import time,os,gc
import numpy as np
import geopandas as geo
import shapely as sy
base=np.asarray([[-1,1],[0,1],[1,1],[-1,0],[1,0],[-1,-1],[0,-1],[1,-1]]).reshape(8,2)
r,c=400,140
class myMatrix:
    def __init__(self,w,h):
        self.data={}
        self.copia={}
        self.crearMatrix(w,h)
    def crearMatrix(s,w,h):
        for x in range(h+1):
            s.data[x]={}
            s.copia[x]={}
            for y in range(w+1):
                s.data[x][y]=cell(x,y)
                s.copia[x][y]={}
    def act(s,vivas):
        for v in vivas:
            s.data[v[1]][v[0]].setStatus(1)
    def ver(s):
        os.system("clear")
        for x in list(s.data.keys()):
            for y in list(s.data[x].keys()):
                print("▓" if s.data[x][y].getStatus()==1 else "░", sep="", end="")
            print("")
    def jugar(s):
        for c in list(s.data.keys()):
            for r in list(s.data[c].keys()):
                s.copia[c][r] = {"estatus":s.data[c][r].getStatus(),"cantVeci":sum([v.getStatus() for v in s.data[c][r].vecinos])}
        for c in list(s.copia.keys()):
            for r in list(s.copia[c].keys()):
                newSta=reglas(s.copia[c][r]["estatus"],s.copia[c][r]["cantVeci"])
                s.data[c][r].setStatus(newSta)

class cell:
    def __init__(self,x,y):
        self.id=(x,y)
        self.status=0
        self.x = x
        self.y = y
        self.vecinos=[] 
    def leer(s):
        return dict(id=s.id,estatus=s.status,vecinos=s.vecinos)
    def setStatus(s,v):
        s.status=v
    def getStatus(s):
        return s.status        
    def crearVecinos(self,_vid):
            for i in range(8):
                tmp = base[i]+self.id
                if ren:=_vid.data.get(tmp[0]):
                    if _cel:=ren.get(tmp[1]):
                        self.vecinos.append(_cel)
                    #else:
                        #self.vecinos.append(cell(*list(tmp)))
                
def linea(pos,i,r1,r2,ex=[]):
    
    return [[i,v] if pos=="v" else [v,i] for v in range(r1,r2+1) if v not in [e+r1 for e in ex]]
def cuadro(c,r,l,ex=[]):
    for x in range(c,c+l):
        for y in range(r,r+l):
            if [x,y] not in ex:
                yield [x,y]
def reglas(val,suma):
    if val==0:
        return 1 if suma==3 else 0
    else:
        return 1 if 1<suma<4 else 0    


vid = myMatrix(r,c)
myData = vid.data
myCells = []
#patron = linea("h",75,50,88,[8,14,15,16,20,21,22,23,24,25,33])
print(linea("h",60,100,105))
print("-*-*-***-*-*-*-***--*-*-**-*-*-*-*-*-*-*-*-*-*--*-*-*-*-")

c1 = [c for c in cuadro(100,10,100)]
patron = c1+linea("h",100,20,49)
vid.act(list(patron))

for _r in range(r):
    for _c in range(c):
        myCells.append(vid.data[_c][_r].leer())
        vid.data[_c][_r].crearVecinos(vid)

  

#gDF = geo.GeoDataFrame(geometry=[sy.Point(*p) for p in patron],crs="EPSG:4326")
#gDF.plot()
vid.ver()
time.sleep(10)
os.system("clear")

turno=0
while True:
    vid.jugar()
    vid.ver()
    
    #gDF = geo.GeoDataFrame(geometry=[v for v in vivas],crs="EPSG:4326")
    #gDF.plot(color="red",marker="*",markersize=2)
    time.sleep(1)
    turno+=1
    
  