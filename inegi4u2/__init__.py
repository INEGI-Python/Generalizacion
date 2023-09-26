from .feature import feature 
from .generalizar import generalizar
import json
___vers__ = "1.0.1"


o,g = feature(),generalizar()
def leer(obj):              
    return o.leer(obj)
def actualizar(_u):
    return o.actualizar(_u)
def eliminar(_u):
    return o.eliminar(_u)
def lineas(_arg):
    return g.lineas(_arg)         

__ALL__= ["leer","actualizar","eliminar","lineas"]
