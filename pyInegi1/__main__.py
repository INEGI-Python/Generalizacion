from basico import Basico

__version__ = "1.0.0"

def DIST2PNT(**pnt):
    print(pnt)
    return Basico.dist2pnts(pnt)

__ALL__=["DIST2PNT"]

