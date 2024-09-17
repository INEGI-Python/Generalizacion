import numpy as np
import shapely as  shpy

class Basico:
    def dist2pnts(s,x1,y1,x2,y2):
        return (x2-x1)/(y2-y1)
    def importarSHP(s,shp):
        import fiona
        with fiona.open(shp) as shapefile:
            for record in shapefile:
                print(record)



#Basico().dist2pnts(x1=-102.325,y1=24.35,x2=-102.8745,y2=25.365)
         

