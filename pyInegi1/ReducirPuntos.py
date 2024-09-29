#import numpy as np
import fiona as fio
import geopandas as gpd
import folium as fol
#import matplotlib.pyplot as  plt
import atajos as ata
from time import time as t
import shapely as sh

ata.distancia=20000

def visible(df,v):
	df['properties']['isvisible']=v
	if v==1 and  df not in ata.data:
		ata.data.append(df['properties'])
		ata.geometry.append(sh.Point(*list(df["geometry"]['coordinates'][0])))

def algoritmo(dfs,_c):
	def  datTmp(_idx):
		isV = dfs[_idx]['properties']['isvisible']
		return  {"id":dfs[_idx]['properties']["OBJECTID"],"xy":dfs[_idx]['geometry']["coordinates"][0],"hab":dfs[_idx]['properties']["num_hab"],"vis":isV,"dist":dfs[_idx]['properties']['distancia']} if  isV != 0 else False
	for i in range(_c-1):
		p1 = datTmp(i)
		if p1:
			for j in range(i+1,_c):
				p2 = datTmp(j)				
				if p2:
					#print(p2)
					dist = ((p2['xy'][0]-p1['xy'][0])**2+(p2['xy'][1]-p1['xy'][1])**2)**0.5
					if dist<=ata.distancia:
						dfs[i]['properties']['distancia']['vecinos'].append(dfs[j]['properties']["OBJECTID"])
						#print(dfs)
						if p1["hab"]>=p2["hab"]:
							visible(dfs[j],0)
							visible(dfs[i],1)
						else:
							visible(dfs[j],1)
							visible(dfs[i],0)
							break
					
				else: 
					break
			
		
			
		
import pandas as pd
t1 = t()
lys= fio.listlayers(ata.GDB)
_dataF = gpd.read_file(ata.GDB,layer="BCs",columns=["OBJECTID","cve_edo","cve_mun","cve_loc","nombre","num_hab"])
#cant = _dataF.count(numeric_only=True)['OBJECTID']
data = [{'vecinos':[i]} for i in _dataF['OBJECTID']]
_dataF.set_index("OBJECTID")
_dataF["gpo"]=0
_dataF["isvisible"]=-1
_dataF["distancia"]=pd.DataFrame(data={'data':data})
CRS = _dataF.crs.to_string() #"EPSG:6372" 
bu = _dataF.buffer((ata.distancia/2)+1)
uni =bu.union_all()
uniDF = gpd.GeoDataFrame(data=[{"id":1}],geometry=[uni],crs=CRS)
#uniDF.to_file("Buffer.shp")
gpos = uniDF.explode(index_parts=True)
gpos["id"]=[i[1]+1 for  i in  gpos.index.sort_values().to_list()]
gpos.set_index("id")
cont = gpos.count(numeric_only=True)['id']
agrupados = _dataF.sjoin(gpos,how="inner",predicate='intersects')
agrupados["gpo"]=agrupados['index_right1']
#agrupados = agrupados.drop(columns=['index_right0','index_right1'])
print("GRUPOS: %d" % cont)
porGPO = agrupados.groupby(by="id").groups
oid = agrupados["OBJECTID"]

tmp=[agrupados.iloc[porGPO[_o]].__geo_interface__['features'] for _o in porGPO.keys()]

for i in range(cont):
	_cant=len(tmp[i])
	if _cant==1:
		visible(tmp[i][0],1)
	else:	
		algoritmo(tmp[i],_cant)
pVisibles = gpd.GeoDataFrame(data=ata.data,geometry=ata.geometry,crs=CRS)


print("Tiempo: %.3f " % float(t()-t1))

m = gpos.explore(column="id",cmap="Set1",name="Grupos",legend=False,  popup=["id"])
pVisibles.explore(m=m,column='isvisible',marker_kwds=dict(radius=2, fill=True),legend=False,name="Localidades",popup=["nombre"])
fol.TileLayer("OpenStreetMap",show=True).add_to(m)
fol.LayerControl().add_to(m)
m
#m.show_in_browser()

#p1,p2 = [31.740804466331763, -115.06898870453817],[31.958902441793633, -114.74387815347139]
#dista = (p2[0]-p1[0])/(p2[1]-p1[1])
