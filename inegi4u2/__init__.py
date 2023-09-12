from .feature import feature 
import json
___vers__ = "1.0.0"
o = feature()
def leer(obj):              
    return o.leer(obj)
def actualizar(_u):
    return o.actualizar(_u)
def eliminar(_u):
    return o.eliminar(_u)             

__ALL__= ["leer","actualizar","eliminar"]
