import argparse as ag
import geopandas as gpd
import folium as fol
from time import time as t
import shapely as sh
from .atajos import imp,fechaHora


def crearGpos(_dataF,CRS,distancia):
	imp("Buscando Localidades Cercanas para agruparlas")
	bu = _dataF.buffer(distancia/2)
	buDF = gpd.GeoDataFrame(geometry=bu,crs=CRS)
	uni =bu.union_all()
	uniDF = gpd.GeoDataFrame(data=[{"id":1}],geometry=[uni],crs=CRS)
	gpos = uniDF.explode(index_parts=True)
	#gpos.to_file("datos/grupos_pruebas.shp")
	imp("Generando grupos")
	gpos["id"]=[i[1]+1 for  i in  gpos.index.sort_values().to_list()]
	gpos.set_index("id")
	cont = gpos.count(numeric_only=True)['id']
	agrupados = _dataF.sjoin(gpos,how="inner",predicate='intersects')
	agrupados["gpo"]=agrupados['id']
	agrupados = agrupados.drop(columns=['index_right0','index_right1','id'])
	imp("Total de Grupos generados: %d" % cont)
	porGPO = agrupados.groupby(by="gpo").groups
	return gpos,agrupados,porGPO

def Generar_Plot(agrupados, distancia, CRS):
	visibles = agrupados.loc[agrupados['isvisible']==True,]
	ocultar = agrupados.loc[agrupados['isvisible']==False,]
	geometria=visibles.loc[visibles.index,].buffer(distancia)
	geomDF = gpd.GeoDataFrame(geometry=geometria,crs=CRS)
	#locas=agrupados.intersection(geomDF.union_all(),align=True)
	#segus = agrupados.loc[locas[locas.is_empty].index,]
	DF_visi = gpd.GeoDataFrame(data=visibles.loc[:,['nombre','gpo','num_hab']].to_dict(),geometry=[sh.Point(*list(g['geometry']['coordinates'])) for g in visibles.__geo_interface__['features']],crs=CRS)
	DF_ocul = gpd.GeoDataFrame(data=ocultar.loc[:,['nombre','gpo','num_hab']].to_dict(),geometry=[sh.Point(*list(g['geometry']['coordinates'])) for g in ocultar.__geo_interface__['features']],crs=CRS)
	return DF_visi,DF_ocul,geomDF	

def crearMapa(**capas):
	_cap=capas['a']
	CRS=capas['b']
	geomDF=capas['c']
	imp("Creando Mapa...")
	m1=_cap["Visible"][0].explore(tooltip=['nombre'],marker_type="circle",style_kwds=dict(color=_cap['Visible'][1],weight=5,opacity=1),marker_kwds=dict(radius=4, fill=True,draggable=True),legend=False,name="Visibles",popup=['nombre','num_hab','gpo'])
	m2=_cap["Ocultas"][0].explore(m=m1,tooltip=['nombre'],marker_type="circle",style_kwds=dict(color=_cap['Ocultas'][1],weight=3,opacity=0.6),marker_kwds=dict(radius=2, fill=True),legend=False,name="Ocultas",popup=['nombre','num_hab','gpo'])
	geomDF.explore(m=m2,color="#AAF", tooltip=False,name="Poligono prueba",legend=False)
	fol.TileLayer("OpenStreetMap",show=True).add_to(m2)
	fol.LayerControl().add_to(m2)
	m2.show_in_browser()


def main(**params):
	imp(params)
	gdb = params['gdb']
	feat = params['feat']
	camp = params["camp"]
	nom_camp = [n.split(":")[0] for n in camp]
	orden = [int(n.split(":")[1])==1  for n in camp]
	distancia = params['dist']
	ver = params['ver']

	t1 = t()
	_dataF = gpd.read_file(gdb,layer=feat) if gdb[-3:]=="gdb" else   gpd.read_file(gdb)
	_dataF["gpo"]=0
	_dataF["isvisible"]=True
	CRS = _dataF.crs.to_string() #"EPSG:6372" 
	gpos,agrupados,porGPO = crearGpos(_dataF,CRS,distancia)


##*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*---*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*--*-
	for i in gpos.id:   
		_cantG=len(porGPO[i])
		imp("Grupo %d »» No. elementos: %d " % (i,_cantG))
		if _cantG>1:
			gpoX = agrupados.iloc[porGPO[i]]
			gpoX = gpoX.sort_values(by=nom_camp, ascending=orden)
			for _g in gpoX.index:
				buf = gpoX.loc[_g,'geometry'].buffer(distancia)
				res = gpoX[gpoX.loc[:,'geometry'].intersects(buf)]
				if res.loc[_g,"isvisible"]:
					if data:=[dict(idx=i,pob=n,jer=j) for i,n,v,j in zip(res.index,res['num_hab'],res['isvisible'],res[nom_camp[0]]) if v and i!=_g]:
						looser = [a['idx'] for a in data if a['jer']>0]
						agrupados.loc[looser,'isvisible'] = False
						gpoX.loc[looser,'isvisible'] = False
	imp("Tiempo del algoritmo: %.3f " % float(t()-t1))
##*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*---*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*--*-


	imp("Guardando resultado...")
	import os 
	nom=gdb.split('/').pop() if feat =="_" else feat
	miDir = os.getcwd()
	for _d in ["RESULTADOS",nom.split(".")[0],str(distancia)]:
		if _d not in os.listdir(): 
			os.mkdir(_d)
		os.chdir(_d)
	archivo=f"{fechaHora()}.shp"
	agrupados.to_file(archivo,encoding="UTF-8")
	imp(f"{os.getcwd().replace("\\","/")}/{archivo}")
	os.chdir(miDir)
	if ver==1:
		DF_visi,DF_ocul,geomDF = Generar_Plot(agrupados, distancia, CRS) 
		crearMapa(a={"Visible":[DF_visi,"#F00"],"Ocultas":[DF_ocul,"gray"]},b=CRS,c=geomDF)  



if __name__ == "__main__":
	parser = ag.ArgumentParser(description="Esta aplicación generaliza una capa  de   tipo punto, reduciendo la cantidad de elementos basados en una distancia dada")
	parser.add_argument('GDB',type=str, help="Ruta absoluta o relativa  de  una Geodatabase o un Shapefile")
	parser.add_argument('FEAT',type=str,  nargs='?', default="fiona.listlayers(args.GDB)", help="Nombre del Featureclass o coloques un guion bajo (_) si no aplica. Si lo omite, el sistema le mostrara un listado de los featuresClass que contiene su geodatabase")
	parser.add_argument("CAMP",type=str, nargs='?', default="Jerarquia:1", help="Campos y su ordenamiento separados por coma que se utilizaran como criterios de importancia. Ejemplo: - jerarquia:1 -  0 = Descendente  1 = Ascendente  ")
	parser.add_argument("DIST",type=int, nargs='?', default=20000, help="Distancia en metros que deberan de existir entre dos puntos del resultado. Default: 20000")
	parser.add_argument("VER",type=int, nargs='?', default=1, help="Genera y muestra un Mapa Web con el resultado. Default: 1")	
	
	args = parser.parse_args()
	if args.FEAT=="fiona.listlayers(args.GDB)":
		import fiona
		print(eval(args.FEAT))
	else:
		main(gdb=args.GDB,feat=args.FEAT,camp=args.CAMP.split(","),dist=args.DIST,ver=args.VER)
#else:
 #   main(gdb='datos/prueba2.shp', feat='_', camp="Jerarquia:1,geografico:1,num_hab:0".split(","),dist=1500,ver=1) 
