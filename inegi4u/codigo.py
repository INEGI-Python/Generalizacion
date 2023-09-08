import numpy
import pandas

def LEER(d,t,p=0,f="*",e=[0,1]):
    lee = lambda x:x*x
    return numpy.array(map(lee,e))

def TOPOLOGIA(d,t,p):
    topo = lambda x:"Topologia elegida: %s" % x
    return pandas.DataFrame(map(topo,[f for f in dir(pandas)]))
