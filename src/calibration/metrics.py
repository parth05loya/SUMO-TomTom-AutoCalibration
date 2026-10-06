from __future__ import annotations
import numpy as np
import pandas as pd

def travel_time_metrics(observed: pd.Series | np.ndarray, simulated: pd.Series | np.ndarray) -> dict[str, float | int]:
    o = np.asarray(observed, dtype=float); s = np.asarray(simulated, dtype=float)
    mask = np.isfinite(o) & np.isfinite(s) & (o > 0)
    if not np.any(mask): return {"n":0,"mae_sec":np.nan,"rmse_sec":np.nan,"mape_pct":np.nan,"bias_sec":np.nan}
    e=s[mask]-o[mask]
    return {"n":int(e.size),"mae_sec":float(np.mean(np.abs(e))),"rmse_sec":float(np.sqrt(np.mean(e**2))),"mape_pct":float(np.mean(np.abs(e/o[mask]))*100.0),"bias_sec":float(np.mean(e))}
