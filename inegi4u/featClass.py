import numpy as np
import pandas as pan
from arcpy import da,env

valid = lambda d: {"status":False, "error": "Falta ruta de GDB o de FeatureClass. Array d = %d pos, deben ser 2" % len(d)} if len(d) != 2 else False

def LEER(d,t,f="*",p=0,e=[0,1]):
    if not valid(d) return valid(d)
    env.workspace = d[0] 
    lee = lambda x:list(da.SearchCursor(d[1],f))
    return ((("Formato %s no valido" % t if t!="arreglo" else lee()) if t!= "arreglo_np" else np.asarray(lee(),dtype=np.matrix)) if t!= "data_frame" else pan.DataFrame(lee())) if t!="unico" else lee()[e[0]:e[1]]

def AGRUPAR(d,f="*",g="@OID"):
    if not valid(d) return valid(d)
    env.workspace = d[0] 
    gpo = lambda x:list(da.SearchCursor(d[1],f,sql_clause=(None,"GROUP BY %s" % g)))
    return gpo()
