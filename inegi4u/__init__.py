from .codigo import LEER,TOPOLOGIA

__version__ = "1.0.0"

def leer(d,t,p=0,f="*",e=[0,1]):
    return LEER(d,t,p,f,e)
def topologia(d,t,p):
    return TOPOLOGIA(d,t,p,f,e)

__ALL__ = ["leer","topologia"]
