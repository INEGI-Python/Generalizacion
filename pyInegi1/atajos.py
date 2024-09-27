def sepa(c="*-*-"):
    print("%s" * 20  % tuple([c for i in range(20)]))

def imp(text):
    print("[info]  %s" % str(text))
    
GDB="datos/Generalizacion_1.gdb"
distancia = 0
data,geometry=[],[]
