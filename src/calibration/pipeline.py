from __future__ import annotations
import pandas as pd
from .network import SumoNetwork

def attach_sumo_edges(df,net_file):
    n=SumoNetwork(net_file); out=df.copy()
    out["origin_edge"]=out.apply(lambda r:n.lonlat_to_edge(r.origin_lon,r.origin_lat).getID(),axis=1)
    out["destination_edge"]=out.apply(lambda r:n.lonlat_to_edge(r.destination_lon,r.destination_lat).getID(),axis=1)
    return out
