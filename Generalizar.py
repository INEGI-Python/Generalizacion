

import httpimport 
GIT = httpimport.github_repo("Emmanuel-INEGI-2023","Generalizacion","main")
f = GIT.__
print(f,end="\n")
print(dir(f))


#       _recreate_cm                    args                       func              gen             kwds
# import pyInegi1 as inegi
# print(dir(inegi))





# print(inegi.basico.dist2pnts(21,35,58,65))
# inegi.basico.capa2Excel("lineasPuertos/poli.shp","Puertos")
# datos = inegi.shp2DF("lineasPuertos/poli.shp")
# poly = datos.polygonize()
# voronoi = datos.voronoi_polygons()
# clip = voronoi.clip(datos)
# clip.plot()
# datos.plot()
# voronoi.plot() 
# lns=[]
# for g in clip.geometry:
# 	lns += inegi.pol2Linea(g)


