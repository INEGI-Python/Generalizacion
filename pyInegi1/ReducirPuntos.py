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
	ata.data.append(df['properties'])
	ata.geometry.append(sh.Point(*list(df["geometry"]['coordinates'][0])))

def algoritmo(dfs,_c):
	def  datTmp(_obj):
		df = gpd.GeoDataFrame(data=[_obj['properties']],geometry=[sh.Point(*list(_obj['geometry']['coordinates'][0]))],crs=CRS)
		print(df)
		isV = df['isvisible']
		buf = df.buffer(ata.distancia)
		vecinos = dfs.sjoin(buf,how="inner",predicate='intersects')
		print(vecinos)
		return False
  		#return  {"id":df['properties']["OBJECTID"],"xy":df['geometry']["coordinates"][0],"hab":df['properties']["num_hab"],"vis":isV,"dist":df['properties']['distancia']} if  isV != 0 else False
	for i in range(_c-1):
		p1 = datTmp(dfs[i])
		if p1:
			for j in range(i+1,_c):
				p2 = datTmp(j)				
				if p2:
					#print(p2)
					dist = int(((p2['xy'][0]-p1['xy'][0])**2+(p2['xy'][1]-p1['xy'][1])**2)**0.5)
					if dist<=ata.distancia:
						dfs[i]['properties']['distancia']['vecinos'].append({dfs[j]['properties']["OBJECTID"]:dist})
		visible(dfs[i],0)
     
     
     		# 		
			# 			#print(dfs)
			# 			if p1["hab"]>=p2["hab"]:
			# 				visible(dfs[j],0)							
			# 			else:
			# 				visible(dfs[j],1)
			# 				visible(dfs[i],0)
			# 				break
			# visible(dfs[i],1)
			
		
			
		
import pandas as pd
t1 = t()
lys= fio.listlayers(ata.GDB)
print(lys)
_dataF = gpd.read_file(ata.GDB,layer="BCs_",columns=["OBJECTID","cve_edo","cve_mun","cve_loc","nombre","num_hab"])
#cant = _dataF.count(numeric_only=True)['OBJECTID']
data = [{'vecinos':[{i:0}]} for i in _dataF['OBJECTID']]
_dataF.set_index("OBJECTID")
_dataF["gpo"]=0
_dataF["isvisible"]=-1
_dataF["distancia"]=pd.DataFrame(data={'data':data})
CRS = _dataF.crs.to_string() #"EPSG:6372" 
print(CRS)
bu = _dataF.buffer((ata.distancia/2)+1)
buDF = gpd.GeoDataFrame(geometry=bu,crs=CRS)
uni =bu.union_all()
uniDF = gpd.GeoDataFrame(data=[{"id":1}],geometry=[uni],crs=CRS)
#uniDF.to_file("Buffer.shp")
gpos = uniDF.explode(index_parts=True)
gpos["id"]=[i[1]+1 for  i in  gpos.index.sort_values().to_list()]
gpos.set_index("id")
cont = gpos.count(numeric_only=True)['id']
agrupados = _dataF.sjoin(gpos,how="inner",predicate='intersects')
agrupados["gpo"]=agrupados['id']
agrupados = agrupados.drop(columns=['index_right0','index_right1','id'])
print("GRUPOS: %d" % cont)
porGPO = agrupados.groupby(by="gpo").groups
oid = agrupados.OBJECTID

#tmp=[agrupados.iloc[porGPO[_o]].__geo_interface__['features'] for _o in porGPO.keys()]

for i in gpos.id:
	print("GRUPO %d " %i)
	_cantG=len(porGPO[i])
	if _cantG==1:
		agrupados.loc[porGPO[i][0],'isvisible'] = 1
	else:
		_gpo = agrupados.iloc[porGPO[i]]
		for _g in _gpo.index:
			_buf=_gpo.loc[_g,'geometry'].buffer(ata.distancia)
			res = _gpo[_gpo.loc[:,'geometry'].intersects(_buf)]
			data = [{o:n} for o,n in zip(res['OBJECTID'],res['num_hab'])]
			pob=_gpo.loc[_g]['num_hab']
			_d_ = [_dat for _dat in data]
			for _d in _d_:
				k=list(_d)[0]
				_i_V = agrupados.iloc[_d[k]]['isvisible']
				print(_i_V)
				if _i_V==-1:				
					if pob>=_d[k]:
						agrupados.loc[agrupados['OBJECTID']==k,'isvisible']=1			
					else:
						agrupados.loc[agrupados['OBJECTID']==_g,'isvisible']=1
						agrupados.loc[agrupados['OBJECTID']==k,'isvisible']=0
						break
     
			agrupados.loc[agrupados['OBJECTID']==_g,'isvisible']=0
   
   
			vec = {'vecinos':data}
			agrupados.loc[_g,'distancia']=vec.values().mapping
			
			#print(res.count(numeric_only=True)['OBJECTID'])
			ata.geometry.append(_buf)
			ata.data.append({'id':_g})
  		#print(_gpo.loc[:,'isvisible'])
		if False:
			for loc in _gpo.iterrows():
				_loc = gpd.GeoDataFrame(geometry=[loc[1].loc['geometry']],crs=CRS)
				_loc["buffer"] =_loc.buffer(ata.distancia)
				_loc["within"] =_loc["buffer"].within(_gpo)
				print(_loc)
		
  

	#else:	
	#	algoritmo(tmp[i],_cant)
#pVisibles = gpd.GeoDataFrame(data=ata.data,geometry=ata.geometry,crs=CRS)
f = agrupados.__geo_interface__['features']
_geoo=[sh.Point(*list(_f['geometry']['coordinates'][0])) for _f in f]
data = [{'id':o,'dist':d,'isV':v} for o,d,v in zip(agrupados['OBJECTID'],agrupados['distancia'],agrupados['isvisible'])]
pVisibles = gpd.GeoDataFrame(data=data,geometry=_geoo,crs=CRS)


print("Tiempo: %.3f " % float(t()-t1))

m = gpos.explore(column="id",cmap="Set1",name="Grupos",legend=False,popup=["id"])
pVisibles.explore(m=m,column='isV',cmap="Set1",marker_kwds=dict(radius=4, fill=True),legend=False,name="Localidades",popup=["isV"])
fol.TileLayer("OpenStreetMap",show=True).add_to(m)
fol.LayerControl().add_to(m)

m.show_in_browser()

#p1,p2 = [31.740804466331763, -115.06898870453817],[31.958902441793633, -114.74387815347139]
#dista = (p2[0]-p1[0])/(p2[1]-p1[1])
