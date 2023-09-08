from .codigo import LEER as _leer,TOPOLOGIA as _topo

__version__ = "1.0.0"

def LEER(d,t,p=0,f="*",e=[0,1]):
    return _leer(d,t,p,f,e)
def TOPOLOGIA(d,t,p):
    return _topo(d,t,p)

__ALL__ = ["LEER","TOPOLOGIA"]
