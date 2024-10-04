import datetime as dt
def sepa(c="*-*-"):
    print("%s" * 20  % tuple([c for i in range(20)]))

def fechaHora():
    t = dt.datetime.today()
    return str(t)[1:-8].replace(" ","-").replace(":","")

def imp(text):
    t = dt.datetime.today()
    print("|%s|  %s" % (str(t)[5:-5],str(text)))

def colores(v):
    return "red" if v==True else "gray"

gdb="datos/Generalizacion.gdb"
distancia = 0
datos,geometria=[],[]
