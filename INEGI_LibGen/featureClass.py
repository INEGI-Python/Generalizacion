import numpy as np
import pandas as pan
from arcpy import da,env

class FeatureClass:
    def __init__(self,d):
        self._gdb = d[0]
        self._fet = d[1]
    def LEER(s,t,f="*",p=0,e=[0,1]):
        def lee():
            return list(da.SearchCursor(s._fet,f))
        env.workspace = s._gdb
        return ((("Formato %s no valido" % t if t!="arreglo" else lee()) if t!= "arreglo_np" else np.asarray(lee(),dtype=np.matrix)) if t!= "data_frame" else pan.DataFrame(lee())) if t!="unico" else lee()[e[0]:e[1]]
