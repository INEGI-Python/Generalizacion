import datetime as dt
def sepa(c="*-*-"):
    print("%s" * 20  % tuple([c for i in range(20)]))

def imp(text):
    t = dt.datetime.today()
    print("[%s]  %s" % (t,str(text)))

def colores(v):
    return "red" if v==True else "gray"

GDB="datos/Generalizacion.gdb"
distancia = 0
datos,geometria=[],[]
