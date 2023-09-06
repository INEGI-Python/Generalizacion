from .featureClass import FeatureClass
__version__ = "0.0.1"
__autor__= "INEGI"
__fecha__ = 2023

def LEER(d,t,f="*",p=0,e=[0,1]):
    return FeatureClass().LEER(d,t,f,p,e)


__all__ = ['LEER']

