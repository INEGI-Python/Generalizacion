from .featClass import LEER,AGRUPAR

__version__ = "1.0.0"

def LEER(d,t,p=0,f="*",e=[0,1]):
    return featClass().LEER(d,t,p,f,e)
def AGRUPAR(d,t,f="*",g="@OID"):
    return featClass().AGRUPAR(d,t,p)

__ALL__ = ["LEER","AGRUPAR"]
