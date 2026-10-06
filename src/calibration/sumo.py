from __future__ import annotations
from pathlib import Path
import os

def find_route_time(net_file,origin_edge,destination_edge,use_libsumo=True,sumo_binary=None):
    try: import libsumo as sim
    except ImportError: sim=None
    if not use_libsumo: sim=None
    cfg=Path(net_file).with_name("autocalibration.sumocfg")
    cfg.write_text(f'<configuration><input><net-file value="{Path(net_file).name}"/></input><time><begin value="0"/><end value="1"/></time></configuration>\n',encoding="utf-8")
    binary=sumo_binary or os.getenv("SUMO_BINARY","sumo")
    if sim is not None:
        sim.start([binary,"-c",str(cfg),"--no-step-log","true"])
        try: return float(sim.simulation.findRoute(origin_edge,destination_edge,depart=0).travelTime)
        finally: sim.close()
    import traci
    traci.start([binary,"-c",str(cfg),"--no-step-log","true"])
    try: return float(traci.simulation.findRoute(origin_edge,destination_edge,depart=0).travelTime)
    finally: traci.close()
