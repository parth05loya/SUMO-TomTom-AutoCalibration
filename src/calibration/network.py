from __future__ import annotations
from pathlib import Path
import sumolib
class SumoNetwork:
    def __init__(self,net_file): self.net_file=Path(net_file); self.net=sumolib.net.readNet(str(self.net_file),withInternal=False)
    def summary(self): return {"nodes":len(self.net.getNodes()),"edges":len(self.net.getEdges())}
    def lonlat_to_edge(self,lon,lat,radius_m=500):
        x,y=self.net.convertLonLat2XY(lon,lat); c=self.net.getNeighboringEdges(x,y,radius_m)
        if not c: raise ValueError(f"No SUMO edge within {radius_m:g} m of ({lon}, {lat}).")
        c.sort(key=lambda z:z[1]); return c[0][0]
