from arcpy import SelectLayerByAttribute_management as sA
from arcpy import Describe as desc
from arcpy import management as m
from arcpy import SpatialReference as sR
from arcpy import AddFeatureClassToTopology_management as Topo
from arcpy import AddRuleToTopology_management as Rule, ValidateTopology_management as valTop, ExportTopologyErrors_management as exTop
from arcpy import CreateFeatureDataset_management as cDs, CreateTopology_management as cTm
from arcpy import AddIncrementingIDField_management as Inc
from arcpy import ListDatasets as LstF
class reduceLineas:
    def __init__(self,c,_param):
        self._capa = c
        self._oid = desc(c).OIDFieldName
        self._oid_new = None
        self._sRf = desc(c).spatialReference
        self._nodos =  []
        self._cond = _param
    
    
    def __del__(self):
        pass

    def getSR(s,c=6362):
        return sR(c)

    def lim(self):
        self._nodos.clear()
        
    def setOid2(s,oi):
        s._oid_new = desc(oi).OIDFieldName 
        
    def getCapa(s):
        return s._capa
    
    def getNodos(s):
        return [n.getNodo() for n in s._nodos]
    
    def getIdNodos(self):
        return len(self._nodos)+1
    
    def updNodo(self,p,_iN,_tN):
        self._nodos[p]._lns.append(_iN)
        self._nodos[p]._tam.append(_tN)
    
    def unir2(self,_g):
        if _g[0][1]>= self._cond and _g[1][1]>=self._cond:
            return False
        return _g[0][0].union(_g[1][0])

class linea:
    def __init__(self,_dat):
        self.__id = _dat[0]   
        self.__largo = _dat[1]
        self.__geom = _dat[2]
    
    def __del__(self):
        pass
        
    @property
    def Id(self):
        return self.__id
    def Id(self,_i):
        self.__id = _i
          
    @property
    def Largo(self):
        return self.__largo
    def Largo(self,l):
        self.__largo = l

    @property
    def Geom(self):
        return self.__geom
    def Geom(self,g):
        self.__geom = g


    def getLinea(_s):
        return {"oid":_s.Id,"geom":_s.Geom,"largo":_s.Largo}

class nodo:
    def __init__(self,i,g,l,t):
        self._id = i
        self._geom=g
        self._lns = [l]
        self._tam = [t]
    
    def __del__(self):
        pass
       
    def getGeom(self):
        return self._geom
    
    
    def getNodo(self):
        return {"oid":self._id,"geom":self._geom,"ln":self._lns,"ta":self._tam}
  
class operaciones:
    def __init__(self):
        self.interC = {}
        self._geoms_tmp = []
        self._muere = 0
        self.optimo = 0
    def trunCoord(_s,_c):
        return [round(c,6) for c in _c]
    def inter(_s,_p,op):
        if (True if _p in _s.interC.keys() else False):
            if op:
                return _s.interC[_p]
            else:
                _s.optimo += 1
                return _p
        else:
            return _p
                    
    def sublista(_s,sb,tl):
        for i in sb:
            if i in tl:
                return True
        return False
    def crearIndice(_s,_lyr,_arc):
        _fs = _arc[1](_lyr)
        if  len([_fs[i].name for i in range(len(_fs)) if _fs[i].name in ["ID_TMP","LARGO"]])==0:
            #Inc(_lyr,"INCREMENTAL")
            _arc[2](_lyr,"LARGO","DOUBLE", 16, "", "", "LARGO", "NULLABLE")
            _arc[2](_lyr,"ID_TMP","LONG", 9, "", "", "ID_TMP", "NULLABLE")
            _arc[3](_lyr,"ID_TMP","idx_id","UNIQUE","ASCENDING")
        _oid_= 1
        with _arc[0].UpdateCursor(_lyr,["ID_TMP","LARGO","SHAPE@LENGTH"]) as uC:
            for u in uC:
                u[0]= _oid_
                u[1]= u[2]
                _oid_+=1
                uC.updateRow(u)
   
    def Topologias(_s, db,_ds,_topo,_ly,_capa,cFm,_arc):
        cDs(db,_ds,spatial_reference=desc(_capa).spatialReference)
        cFm(_capa,_ds+"/"+_ly)
        cTm(_ds,_topo)
        Topo(_ds+"/"+_topo,_ds+"/"+_ly,"")
        Rule(_ds+"/"+_topo,"Must Not Overlap (Line)",_ds+"/"+_ly)
        print("[info] Ejecutando regla topologica. Must Not Overlap...")
        valTop(_ds+"/"+_topo,"Full_Extent")
        exTop(_ds+"/"+_topo,_ds,"overlaps_tipo")
        cFm(_ds+"/overlaps_tipo_line","Topologia_overlaps_lineas")

    def FIN(_s,ti,_arc,v,_t,t,db,_o,cFm,mF): 
        print("[info] Renombrando archivo final.")
        ban,_n=["lineas","nodos"],""
        m.Rename("nodos1","Nodos_originales"+str(_t[10:-3]),"FeatureClass")   #% (str(_o["op2"]),str(_t[10:-3]))
        for _fet in _arc[1]():
            if _fet==_o["op1"]+"_lineas":
                _n = _o["op1"]+"_lineas"
                m.Rename("lineas%d" % v,_n+_t,"FeatureClass")
                ban[0]=False
            if _fet==_o["op1"]+"_nodos":
                m.Rename("nodos%d" % v,_o["op1"]+"_nodos"+_t,"FeatureClass")
                ban[1]=False
        [m.Rename("%s%d" % (b,v),_o["op1"]+"_%s"%b,"FeatureClass") for b in ban if b]
        if _o["op3"]:
            print("[info] Creando DataSet de Topologias.")
            nom = _o["op1"]+"_lineas" if len(_n)==0 else _n+_t
            capa = mF(db+nom,"lineas")
            _s.Topologias(db,"topo_tmp","Topologias","miCapa",capa,cFm,_arc)
        print("[info] Eliminando Archivos Temporales")
        print("[info] Se eliminaron %d archivos" % _s.EliminarCasiTodo(_arc,["linea","nodos","topo_"],5) )
        print("[info] EL PROCESO TERMINO SATISFACTORIAMENTE. Tiempo utilizado %.3f seg" % (t() - ti))
        exit(1)

    def EliminarCasiTodo(_s,_arc,_eli,_car):
        cont=0
        for f in _arc[1]():
            if f[:_car] in _eli:
                try:                        
                    _arc[2](f)
                    cont+=1
                except Exception as e:
                    print("ERROR DE BLOQUEOS. Cierre su arcMap para solucionar el problema")
        return cont
