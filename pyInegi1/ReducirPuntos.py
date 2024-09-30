import argparse as ag
import geopandas as gpd
import folium as fol
from atajos import imp,distancia,datos,geometria,gdb
from time import time as t
import shapely as sh


def polyDist(buf,_i):
	geometria.append(buf)
	datos.append({'id':_i})
 
 
def crearGpos(_dataF,CRS):
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
	return gpos, porGPO,agrupados



def crearMapa(**capas):
	agrupados=capas['a']
	CRS=capas['b']
	geomDF=capas['c']
	imp("Creando Mapa...")
	pVisibles = gpd.GeoDataFrame(data=agrupados.loc[:,['isvisible','distancia','gpo','num_hab']].to_dict(),geometry=[sh.Point(*list(g['geometry']['coordinates'][0])) for g in agrupados.__geo_interface__['features']],crs=CRS)
	m=pVisibles.explore(column='isvisible',cmap=["gray","red"],marker_kwds=dict(radius=4, fill=True),legend=False,name="Localidades",popup=['isvisible','num_hab','gpo'])
	geomDF.explore(m=m,color="#FFF",name="Poligono prueba",legend=False)
	fol.TileLayer("OpenStreetMap",show=True).add_to(m)
	fol.LayerControl().add_to(m)
	m.show_in_browser()
 
 

def main(**params):
	imp(params)
	gdb = params['gdb']
	capa = params['feat']
	distancia = params['dist']
 
	t1 = t()
	_dataF = gpd.read_file(gdb,layer=capa,columns=["cve_edo","cve_mun","cve_loc","nombre","num_hab"])
#	data = [dict(vecinos=[dict(idx=i,pob=h)]) for i,h in zip(_dataF.index,_dataF['num_hab'])]
	_dataF["gpo"]=0
	_dataF["isvisible"]=True
	_dataF["distancia"]=object()  #pd.DataFrame(data={'data':data})
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

	for i in gpos.id:   ##  GRUPOS
		_cantG=len(porGPO[i])
		imp("Anlizando grupo %d. Localidades del grupo: %d " % (i,_cantG))
		if _cantG==1:
			agrupados.loc[porGPO[i][0],'isvisible'] = True
		else:
			gpoX = agrupados.iloc[porGPO[i]]
			gpoX = gpoX.sort_values(by="num_hab",ascending=False)
			for _g in gpoX.index:
				buf = gpoX.loc[_g,'geometry'].buffer(distancia)			
				res = gpoX[gpoX.loc[:,'geometry'].intersects(buf)]
				data = [dict(idx=i,pob=n) for i,n,v in zip(res.index,res['num_hab'],res['isvisible']) if v and i!=_g]			
				pob=gpoX.loc[_g]['num_hab']
				agrupados.loc[_g,'distancia']={'vecinos':data}.values().mapping
				
				looser = [a['idx'] for a in data if pob>=a['pob']]
				agrupados.loc[looser,'isvisible'] = False  
	agrupados.to_file("datos/%s-Parte1.shp" % capa)
	geometria=agrupados.loc[agrupados['isvisible']==True,].buffer(distancia)
	geomDF = gpd.GeoDataFrame(geometry=geometria,crs=CRS)
	locas=agrupados.intersection(geomDF.union_all(),align=True)
	segus = agrupados.loc[locas[locas.is_empty].index,]
	crearMapa(a=agrupados,b=CRS,c=geomDF)  
	segus.to_file("datos/%s-Restantes.shp" % capa)
 
 
	# from zipfile import ZipFile
	# with ZipFile("datos/%s.zip","w") as sip:
	# 	for z in ["shp","shx","dbf","prj"]:
	# 		sip.write("datos/%s.%s" % (name,z))
	# 	sip.close()

	print("Tiempo: %.3f " % float(t()-t1))




if __name__ == "__main__":
	parser = ag.ArgumentParser(description="Esta aplicacion generaliza una capa  de   tipo punto, reduciendo la cantidad de elementos basados en una distancia dada")
	parser.add_argument('GDB',type=str, nargs='?', default="datos/Generalizacion.gdb", help="Ruta absoluta o relativa  de  la geodatabase")
	parser.add_argument('FEAT',type=str, nargs='?', default="Localidad_2021", help="Rutal relativa a la geodatabase donde se encuentra el featureclass a generalizar")
	parser.add_argument("DIST",type=int,nargs='?',default=20000,help="Distancia en metros que deberan de existir entre dos puntos del resultado")
	args = parser.parse_args()
	main(gdb=args.GDB,feat=args.FEAT,dist=args.DIST)
#m.show_in_browser()


## ['Chis_min_2', 'localidad250', 'Localidad_2021', 'Cercanos_geo', 'BCs']