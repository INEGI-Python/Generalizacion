import fiona as fio
import geopandas as gpd
import folium as fol
from atajos import imp,distancia,datos,geometria,GDB,colores
from time import time as t
import shapely as sh

distancia=20000

def polyDist(buf,_i):
	geometria.append(buf)
	datos.append({'id':_i})

def algoritmo(dfs,_c):
	pass
		
import pandas as pd
t1 = t()
lys= fio.listlayers(GDB)
print(lys)
_dataF = gpd.read_file(GDB,layer="BCs",columns=["cve_edo","cve_mun","cve_loc","nombre","num_hab"])
data = [dict(vecinos=[dict(idx=i,pob=h,visi=True)]) for i,h in zip(_dataF.index,_dataF['num_hab'])]
#_dataF["idx"]=_dataF.index
_dataF["gpo"]=0
_dataF["isvisible"]=True
_dataF["distancia"]=pd.DataFrame(data={'data':data})
CRS = _dataF.crs.to_string() #"EPSG:6372" 
imp("Buscando Localidades Cercanas para agruparlas")
bu = _dataF.buffer((distancia/2)+1)
buDF = gpd.GeoDataFrame(geometry=bu,crs=CRS)
uni =bu.union_all()
uniDF = gpd.GeoDataFrame(data=[{"id":1}],geometry=[uni],crs=CRS)
gpos = uniDF.explode(index_parts=True)
imp("Generando grupos")
gpos["id"]=[i[1]+1 for  i in  gpos.index.sort_values().to_list()]
gpos.set_index("id")
cont = gpos.count(numeric_only=True)['id']
agrupados = _dataF.sjoin(gpos,how="inner",predicate='intersects')
agrupados["gpo"]=agrupados['id']
agrupados = agrupados.drop(columns=['index_right0','index_right1','id'])
imp("Total de Grupos generados: %d" % cont)
porGPO = agrupados.groupby(by="gpo").groups


for i in gpos.id:
	_cantG=len(porGPO[i])
	imp("Anlizando grupo %d. Localidades del grupo: %d " % (i,_cantG))
	if _cantG==1:
		agrupados.loc[porGPO[i][0],'isvisible'] = True
	else:
		gpoX = agrupados.iloc[porGPO[i]]
		for _g in gpoX.index:
			buf = gpoX.loc[_g,'geometry'].buffer(distancia)			
			res = gpoX[gpoX.loc[:,'geometry'].intersects(buf)]
			data = [dict(idx=i,pob=n,visi=v) for i,n,v in zip(res.index,res['num_hab'],res['isvisible']) if v and i!=_g]			
			pob=gpoX.loc[_g]['num_hab']
			vis=gpoX.loc[_g]['isvisible']
			agrupados.loc[_g,'distancia']={'vecinos':data}.values().mapping
			
			looser = [a['idx'] for a in data if pob>=a['pob']]
			agrupados.loc[looser,'isvisible'] = False  

geometria=agrupados.loc[agrupados['isvisible']==True,].buffer(distancia)
locas=agrupados.loc[:,'geometry'].intersects(geometria)

pol = gpd.GeoDataFrame(geometry=geometria,crs=CRS)
pVisibles = gpd.GeoDataFrame(data=agrupados.loc[:,['isvisible','distancia','gpo','num_hab']].to_dict(),geometry=[sh.Point(*list(g['geometry']['coordinates'][0])) for g in agrupados.__geo_interface__['features']],crs=CRS)
print("Tiempo: %.3f " % float(t()-t1))
imp("Creando Mapa...")

m=pVisibles.explore(column='isvisible',cmap=["gray","red"],marker_kwds=dict(radius=4, fill=True),legend=False,name="Localidades",popup=['isvisible','num_hab','gpo'])
pol.explore(m=m,color="#FFF",name="Poligono prueba",legend=False)
fol.TileLayer("OpenStreetMap",show=True).add_to(m)
fol.LayerControl().add_to(m)
m

#m.show_in_browser()

#p1,p2 = [31.740804466331763, -115.06898870453817],[31.958902441793633, -114.74387815347139]
#dista = (p2[0]-p1[0])/(p2[1]-p1[1])
