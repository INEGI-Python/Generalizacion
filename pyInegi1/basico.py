import numpy as np
import shapely as  shpy

class Basico:
	def dist2pnts(self, x1, y1, x2, y2):
		return ((x2-x1)**2+(y2-y1)**2)**0.5
	def importarSHP(self, shp):
		import fiona
		with fiona.open(shp) as shapefile:
			for record in shapefile:
				print(record)
	def importFeat(self, gdb, feat, campos=None):
		import geopandas as gpd
		return gpd.read_file(gdb,layer=feat,columns=campos)

	def tabla2Excel(self,gdb,feat,nom):
		import geopandas as gpd
		tabla = gpd.read_file(gdb,layer=feat)
		return tabla.to_excel(f"{nom}.xlsx")



#Basico().dist2pnts(x1=-102.325,y1=24.35,x2=-102.8745,y2=25.365)  Visibles_10k_GenerateNearTab', 'visibles_15k', 'visibles_15k_GenerateNearTab
		 

