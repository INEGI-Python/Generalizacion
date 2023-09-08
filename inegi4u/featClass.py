import numpy as np
import pandas as pan
from arcpy import da,env

def valid(d): 
    if len(d) != 2:    
        print("Falta ruta de GDB o de FeatureClass. Array d = %d pos, deben ser 2" % len(d))
        exit(1)
    env.workspace = d[0]
def LEER(d,t,f="*",p=0,e=[0,1]):
    valid(d)
    lee = lambda x:list(da.SearchCursor(d[1],f))
    return ((("Formato %s no valido" % t if t!="arreglo" else lee()) if t!= "arreglo_np" else np.asarray(lee(),dtype=np.matrix)) if t!= "data_frame" else pan.DataFrame(lee())) if t!="unico" else lee()[e[0]:e[1]]

def AGRUPAR(d,f="*",g="@OID"):
    valid(d)
    gpo = lambda x:list(da.SearchCursor(d[1],f,sql_clause=(None,"GROUP BY %s" % g)))
    return gpo()
