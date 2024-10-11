import httpimport
import datetime
clase = httpimport.add_remote_repo("https://git.inegi.org.mx/EMMANUEL.RODRIGUEZ/sistema-colaborativo-de-generalizacion.git","lineas")
print(dir(clase))
print(clase.load_module("lineas").__loader__.ca_file)   
with httpimport.github_repo("EMMANUEL.RODRIGUEZ","sistema-colaborativo-de-generalizacion",ref="main"): 
    
    
    
	import lineas","","import json, numpy as np","import geopandas","import geodatasets","","","from unir import feature","_gdb = ["pruebas.gdb","costa"]","f = feature(_gdb)","costa = geopandas.read_file(geodatasets.get_path('costa'))","print(costa)","","res = f.leer({"d":_gdb,"f":"SHAPE@XY","t":"arreglo","e":[0,-1],"w":[0,2]})","for i in range(1,len(res)):","    angle = np.arctan2(res[i][0][0]-res[i-1][0][0],res[i][0][1]-res[i-1][0][1])","    dg = np.degrees(angle)","    print("  ----->  ",angle)","    print((dg-450)*-1 if angle>=0 else dg + 360 )","    #print((dg + 90 if angle < 1 else dg + 270) if angle >= 0 else (dg * -1) + 90)","","
# ['__call__', '__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', ","#  '__func__', '__ge__', '__get__',
# '__getattribute__', '__gt__', '__hash__', '__init__', ","#  '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', ","#  '__repr__', '__self__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']