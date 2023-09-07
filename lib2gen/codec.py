import numpy as np
import pandas as pan
from arcpy import da,env

def LEER(s,d,t,f="*",p=0,e=[0,1]):
    def lee():
        return list(da.SearchCursor(d[1],f))
    env.workspace = d[0]
    return ((("Formato %s no valido" % t if t!="arreglo" else lee()) if t!= "arreglo_np" else np.asarray(lee(),dtype=np.matrix)) if t!= "data_frame" else pan.DataFrame(lee())) if t!="unico" else lee()[e[0]:e[1]]
