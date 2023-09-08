from .codigo import LEER,TOPOLOGIA

__version__ = "1.0.0"

def LEER(d,t,p=0,f="*",e=[0,1]):
    return codigo().LEER(d,t,p,f,e)
def TOPOLOGIA(d,t,p):
    return codigo().TOPOLOGIA(d,t,p)

__ALL__ = ["LEER","TOPOLOGIA"]
