from .feature import feature, leer, actualizar, eliminar

__version__="1.0"

def leer():
    return feature().leer()
def actualizar(_u):
    return feature().actualizar(_u)
def eliminar(_u):
    return feature().eliminar(_u)
                   


__ALL__ = ["leer","actualizar","eliminar"]
