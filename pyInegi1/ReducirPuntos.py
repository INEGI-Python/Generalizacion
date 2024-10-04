import argparse as ag
import geopandas as gpd 
import folium as fol
from atajos import imp,sepa,colores
from time import time as t
import shapely as sh


class datos(object):
	def __init__(self,**arg):
		print(arg)
		self.gdb=arg['gdb']
		self.feat=arg['feat']
		self.camp=arg['camp']
		self.dist=arg['dist']
		self.ver=arg['ver']
		self._dataF= gpd.GeoDataFrame()
		self.crs=None
		self.gpos=None
		self.agrupados=gpd.GeoDataFrame()
		self.porGPO = gpd.GeoDataFrame()


		self.inicio()	
		self.crearGpos()
		self.algoritmo()
		if self.ver:
			self.crearMapa()

	def setDatos(self):
		self._dataF = gpd.read_file(self.gdb,layer=self.feat,columns=["cve_edo","cve_mun","cve_loc","nombre"]+self.camp) 
	def crearMapa(self):
		visibles = self.agrupados.loc[self.agrupados['isvisible']==True,]
		ocultar = self.agrupados.loc[self.agrupados['isvisible']==False,]
		geometria=visibles.loc[visibles.index,].buffer(self.dist)
		geomDF = gpd.GeoDataFrame(geometry=geometria,crs=self.crs)
		DF_visi = gpd.GeoDataFrame(data=visibles.loc[:,['nombre','gpo','num_hab']].to_dict(),geometry=[sh.Point(*list(g['geometry']['coordinates'][0])) for g in visibles.__geo_interface__['features']],crs=self.crs)
		DF_ocul = gpd.GeoDataFrame(data=ocultar.loc[:,['nombre','gpo','num_hab']].to_dict(),geometry=[sh.Point(*list(g['geometry']['coordinates'][0])) for g in ocultar.__geo_interface__['features']],crs=self.crs)
		imp("Creando Mapa...")
		m1= DF_visi.explore(color="red",tooltip=['nombre'],marker_type="circle",style_kwds=dict(color="darkblue",weight=5,opacity=1),marker_kwds=dict(radius=4, fill=True,draggable=True),legend=False,name="Visibles",popup=['nombre','num_hab','gpo'])
		m2= DF_ocul.explore(m=m1,tooltip=['nombre'],marker_type="circle",style_kwds=dict(color="gray",weight=3,opacity=0.6),marker_kwds=dict(radius=2, fill=True),legend=False,name="Ocultas",popup=['nombre','num_hab','gpo'])
		geomDF.explore(m=m2,color="#AAF", tooltip=False,name="Poligono prueba",legend=False)
		fol.TileLayer("OpenStreetMap",show=True).add_to(m2)
		fol.LayerControl().add_to(m2)
		m2.show_in_browser()

	def inicio(self):
		self.setDatos()
		self._dataF["gpo"] = 0
		self._dataF["isvisible"] = True
		self._dataF["distancia"] = 0
		self.crs = self._dataF.crs.to_string() 	

	def crearGpos(self):
		imp("Buscando Localidades Cercanas para agruparlas")
		bu = self._dataF.buffer((self.dist/2)+1)
		buDF = gpd.GeoDataFrame(geometry=bu, crs=self.crs)
		uni =bu.union_all()
		uniDF = gpd.GeoDataFrame(data=[{"id":1}], geometry=[uni], crs=self.crs)
		self.gpos = uniDF.explode(index_parts=True)
		imp("Generando grupos")
		self.gpos["id"] = [i[1]+1 for  i in  self.gpos.index.sort_values().to_list()]
		self.gpos.set_index("id")
		cont = self.gpos.count(numeric_only=True)['id']
		self.agrupados = self._dataF.sjoin(self.gpos, how="inner", predicate='intersects')
		self.agrupados["gpo"] = self.agrupados['id']
		self.agrupados = self.agrupados.drop(columns=['index_right0', 'index_right1', 'id'])
		imp("Total de Grupos generados: %d" % cont)
		self.porGPO = self.agrupados.groupby(by="gpo").groups
	def algoritmo(self):
		t1 = t()
		for i in self.gpos.id:   ##  GRUPOS
			_cantG=len(self.porGPO[i])
			imp("Grupo %d »» No. elementos: %d " % (i,_cantG))
			if _cantG>1:
				gpoX = self.agrupados.iloc[self.porGPO[i]]
				gpoX = gpoX.sort_values(by=self.camp,ascending=[True,True,False])
				for _g in gpoX.index:
					buf = gpoX.loc[_g,'geometry'].buffer(self.dist)
					res = gpoX[gpoX.loc[:,'geometry'].intersects(buf)]
					if res.loc[_g,"isvisible"]:
						if data := [dict(idx=i, pob=n, jer=j) for i, n, v, j in zip(res.index, res['num_hab'], res['isvisible'], res[self.camp[0]]) if v and i != _g]:
							looser = [a['idx'] for a in data if a['jer']>0]
							self.agrupados.loc[looser,'isvisible'] = False
							gpoX.loc[looser,'isvisible'] = False
		imp("Tiempo del algoritmo: %.3f " % float(t()-t1))
		imp("Guardando resultado...")
		self.agrupados.to_file(f"RESULT-{self.feat}.shp")

if False:  #__name__ == "__main__":
	parser = ag.ArgumentParser(description="Esta aplicacion generaliza una capa  de   tipo punto, reduciendo la cantidad de elementos basados en una distancia dada")
	parser.add_argument('GDB',type=str, help="Ruta absoluta o relativa  de  la geodatabase")
	parser.add_argument('FEAT',type=str,  nargs='?', default="fiona.listlayers(args.GDB)", help="Nombre del featureclass a generalizar. Si lo omite, el sistema le mostrara un listado de los featuresClass que contiene su geodatabase")
	parser.add_argument("CAMP",type=str, nargs='?', default="jera,clase,num_hab", help="Campos separados por coma que se utilizaran como criterios de importancia")
	parser.add_argument("DIST",type=int, nargs='?', default=20000, help="Distancia en metros que deberan de existir entre dos puntos del resultado. Default: 20000")
	parser.add_argument("VER",type=int, nargs='?', default=1, help="Genera y muestra un Mapa Web con el resultado. Default: 1")	
	args = parser.parse_args()
	imp(dict(gdb=args.GDB,feat=args.FEAT,camp=args.CAMP.split(","),dist=args.DIST,ver=args.VER))
	if args.FEAT=="fiona.listlayers(args.GDB)":
		import fiona
		print(eval(args.FEAT))
	else:
		d = datos(gdb=args.GDB,feat=args.FEAT,camp=args.CAMP.split(","),dist=args.DIST,ver=args.VER)
else:
    d = datos(gdb='datos/Generalizacion_1.gdb', feat='BCs', camp="jera,clase,num_hab".split(","),dist=20000,ver=1) 
