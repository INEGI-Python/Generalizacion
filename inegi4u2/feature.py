import numpy as np
import pandas as pan
import datetime
from arcpy import env,da

class feature:
    def __init__(self):
        pass
    def leer(s,_dat):  
        lee = lambda _dat:list(da.SearchCursor(_dat["d"][1],_dat["f"]))
        env.workspace = _dat["d"][0]
        return (("Formato %s no valido" % _dat["t"] if _dat["t"]!="arreglo" else lee(_dat))   if _dat["t"] != "arreglo_np" else np.asarray(lee(_dat),dtype=np.matrix))  if _dat["t"]!="data_frame" else pan.DataFrame(lee(_dat) )  if _dat["t"] != "unico" else lee(_dat)[_dat["e"][0]:_dat["e"][1]]
    def actualizar(s,u):
        obj={"status":True,"data":[],"fecha":datetime.date.today(),"user":u}
        return obj
    def eliminar(s,e):
        return np.array([54,55,25,685,e])
