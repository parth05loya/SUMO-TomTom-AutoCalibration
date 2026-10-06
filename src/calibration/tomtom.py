from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import os,requests
@dataclass
class TomTomObservation:
    travel_time_sec: float
    no_traffic_travel_time_sec: float
    distance_m: float
    raw: dict[str,Any]
class TomTomClient:
    BASE_URL="https://api.tomtom.com/routing/1/calculateRoute/{locations}/json"
    def __init__(self,api_key=None,timeout=30):
        self.api_key=api_key or os.getenv("TOMTOM_API_KEY"); self.timeout=timeout
        if not self.api_key: raise ValueError("TomTom API key is not configured.")
    def route(self,origin_lon,origin_lat,destination_lon,destination_lat,depart_at="now"):
        locations=f"{origin_lat},{origin_lon}:{destination_lat},{destination_lon}"
        params={"key":self.api_key,"traffic":"true","travelMode":"car","routeType":"fastest","departAt":depart_at}
        r=requests.get(self.BASE_URL.format(locations=locations),params=params,timeout=self.timeout); r.raise_for_status()
        p=r.json(); s=p["routes"][0]["summary"]
        return TomTomObservation(float(s["travelTimeInSeconds"]),float(s.get("noTrafficTravelTimeInSeconds",s["travelTimeInSeconds"])),float(s.get("lengthInMeters",float("nan"))),p)
