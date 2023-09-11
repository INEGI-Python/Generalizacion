from .feature import feature, leer, actualizar, eliminar

__version__="1.0"

def leer():
    return feature().leer()
                   


__ALL__ = ["leer","actualizar","eliminar"]
