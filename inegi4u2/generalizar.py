import warnings
from clases import reduceLineas,linea,nodo,operaciones
import os,sys
from time import time as t
import pandas as pd
from arcpy import MakeFeatureLayer_management as mF
from arcpy import da
from arcpy import FeatureVerticesToPoints_management as fV
from arcpy import CopyFeatures_management as cFm
from arcpy import ListFeatureClasses as Lfc
from arcpy import Delete_management as dm
from arcpy import ListFields as lF
from arcpy import AddField_management as addF
from arcpy import AddIndex_management as addI
from arcpy import management as m
from datetime import datetime
from operator import itemgetter
from pandas.core.common import SettingWithCopyWarning

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

class generalizar:
    def __init__(self):
        pass
    

    def start(s,db,fet,vuelta,td,opc): 
        _c_ = "capa%d" %vuelta
        _res_ = "resul%d" % vuelta
        mF(db+fet,_c_)
        op = operaciones()
        #op.EliminarCasiTodo([m,Lfc,dm],["resul"],5)
        op.crearIndice(_c_,[da,lF,addF,addI])
        rL = reduceLineas(_c_,int(_arg[3]))
        cFm(_c_,"lineas%d" %vuelta)
        mF(db+"lineas%d" %vuelta,_res_)
        nd = "nodos%d" %vuelta
        rL.setOid2(_res_)
        print("[info] Creando nodos en cada inicio y fin de linea")
        fV(_c_,nd,"BOTH_ENDS")
        _geoms_tmp = []  
        with da.SearchCursor(nd,["SHAPE@XY","ID_TMP","LARGO"],spatial_reference=rL.getSR()) as _rws:
            _noArr = _rws._as_narray()
            for i in range(len(_noArr)):
                try:
                    _idx = _geoms_tmp.index(op.trunCoord(list(_noArr[i][0])))
                    rL.updNodo(_idx,_noArr[i][1],_noArr[i][2])
                except ValueError:      
                    rL._nodos.append(nodo(rL.getIdNodos(),op.trunCoord(list(_noArr[i][0])),_noArr[i][1],_noArr[i][2]))
                    _geoms_tmp.append(op.trunCoord(list(_noArr[i][0])))   
        dataNodos = pd.DataFrame(rL.getNodos())
        _nodos = dataNodos.drop([i for i in range(rL.getIdNodos()-1) if len(dataNodos.iloc[i]["ln"])!=2])
        print("[info] Obteniendo lineas de longitud menor a %s m. " % rL._cond)
        _fil = {"oid":[],"geometry":[],"tam":[]}
        with da.SearchCursor(rL._capa,["ID_TMP","SHAPE@JSON","SHAPE@LENGTH"],where_clause="Shape_Length < %f" % float(rL._cond) ,spatial_reference=rL.getSR()) as rows:
            for row in rows:
                _fil["oid"].append(row[0])
                _fil["geometry"].append(row[1])
                _fil["tam"].append(row[2])
            df = pd.DataFrame(_fil) 
            _idLn = [df.iloc[i]["oid"]  for i in df.index]
            print("[info] Eliminando nodos que no tocan lineas de longitud menor a %s m. " % rL._cond)
            _tmp = [_n[0] for _n in _nodos.iterrows() if  op.sublista(dict(_n[1])["ln"],_idLn)]
            _tmp_   = _nodos.loc[_tmp]
            _obj = [_tmp_.iloc[i] for i in range(len(_tmp_)) if len(_tmp_.iloc[i]["geom"]) > 0] 
            if len(_obj) == 0:
                op.FIN(ini,[m,Lfc,dm],vuelta,td,t,db,opc,cFm,mF)
        print("[info] Uniendo lineas")
        _muere=0
        for i in range(len(_obj)):
            _obj[i].loc["mini"] = min(_obj[i].loc["ta"])
            _obj[i].loc["maxi"] = max(_obj[i].loc["ta"])
        sortedlist = sorted(sorted(_obj,key=itemgetter('maxi'),reverse=True),key=itemgetter('mini'))  
        for y in sortedlist:
            op.optimo=0
            _t = [op.inter(_y,opc["op2"]) for _y in y["ln"]]
            if op.optimo == 0:
                w_c = rL._oid_new+" IN "+ str(tuple(_t))
                g =  [r for r in da.SearchCursor(_res_,["SHAPE@","SHAPE@LENGTH"],where_clause=w_c,spatial_reference=rL.getSR(),sql_clause=(None,"ORDER BY Shape_Length ASC"))]    
                if len(g)>1:
                    g3 = rL.unir2(g)
                    if g3:
                        with da.UpdateCursor(_res_,["SHAPE@","ID_TMP"],where_clause=w_c,spatial_reference=rL.getSR(),sql_clause=(None,"ORDER BY Shape_Length ASC")) as rows:
                            row = rows.next()
                            _idx = _t.index(row[1])
                            row[0] = g3
                            rows.updateRow(row)
                            row = rows.next()
                            rows.deleteRow()
                            op.interC[_t[_idx-1]]=_t[_idx]
                        _muere += 1

        print("Lineas a Unirse en la vuelta %d: %d" % (vuelta , _muere))  
        if _muere==0 or len(_obj) == _muere:
            op.FIN(ini,[m,Lfc,dm],vuelta,td,t,db,opc,cFm,mF)
        return 1









    def lineas(s,_arg):
        if len(_arg)<5:
            print("[error] ERROR DE ARGUMENTOS. Numero de argumentos invalido. Se esperan 4 argumentos al menos")
            exit(1)

        pt = str(datetime.now())
        td = pt.replace("-","").replace(":","").replace(".","").replace(" ","_")
        ini = t()
        db = _arg[1]+"\\" if _arg[1][1] == ":" else os.getcwd()+"\\"+_arg[1]+"\\"
        from arcpy import env as e
        e.workspace = db
        e.overwriteOutput=True
        o = operaciones()
        o.EliminarCasiTodo([m,Lfc,dm],["linea","nodos"],5)
        vuelta,capa = 1, _arg[2] 
        opc = {"op1":_arg[4],"op2":_arg[2]}
        def validParam(v):
            if not v.isdigit():
                print("[error] ERROR DE ARGUMENTOS. Se esperaba un numero")
                exit(1)
            if int(v) not in [0,1]:   
                print("[error] ERROR DE ARGUMENTOS. Solo se permiten 0 y 1 para este parametro")
                exit(1)
            return int(v)
        try:
            opc["op2"] = validParam(_arg[5])  
        except Exception as e: 
            opc["op2"] = 0
        try:
            opc["op3"] = validParam(_arg[6])  
        except Exception as e: 
            opc["op3"] =  0
        while True:
            vuelta += s.start(db,capa,vuelta,td,opc)
            capa = "lineas%d" % (vuelta-1)
            print("   *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* ")