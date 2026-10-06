import numpy as np
from calibration.metrics import travel_time_metrics
def test_metrics():
    r=travel_time_metrics(np.array([100.,200.]),np.array([110.,180.])); assert r["n"]==2; assert r["mae_sec"]==15.; assert r["bias_sec"]==-5.
