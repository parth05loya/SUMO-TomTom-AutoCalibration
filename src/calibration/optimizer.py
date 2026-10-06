from __future__ import annotations
from dataclasses import dataclass
import numpy as np
@dataclass
class OptimizationResult:
    parameter:float
    objective:float
    history:list

def grid_search_1d(objective_fn,lower,upper,coarse_steps=9,refine_steps=5):
    if lower>=upper: raise ValueError("lower must be less than upper")
    lo,hi=lower,upper; history=[]
    for level,steps in enumerate((coarse_steps,refine_steps),1):
        grid=np.linspace(lo,hi,steps); scores=[float(objective_fn(float(p))) for p in grid]
        history += [{"level":level,"parameter":float(p),"objective":s} for p,s in zip(grid,scores)]
        i=int(np.nanargmin(scores)); lo,hi=(grid[0],grid[1]) if i==0 else ((grid[-2],grid[-1]) if i==len(grid)-1 else (grid[i-1],grid[i+1]))
    best=min((x for x in history if np.isfinite(x["objective"])),key=lambda x:x["objective"])
    return OptimizationResult(best["parameter"],best["objective"],history)
