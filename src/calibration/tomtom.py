from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import os, requests

@dataclass
class TomTomObservation:
    travel_time_sec: float
    no_traffic_travel_time_sec: float
    distance_m: float
    raw: dict[str,Any]

class TomTomClient:
    BASE_URL="https://api.tomtom.com/routing/1/calculateRoute/{locations}/json"
    def __init__(self, api_key: str|None=None, timeout:int=30):
        self.api_key=api_key or os.getenv("TOMTOM_API_KEY"); self.timeout=timeout
        if not self.api_key: raise ValueError("TomTom API key is not configured.")
    def route(self, origin_lon:float, origin_lat:float, destination_lon:float, destination_lat:float, depart_at:str="now")->TomTomObservation:
        locations=f"{origin_lat},{origin_lon}:{destination_lat},{destination_lon}"
        params={"key":self.api_key,"traffic":"true","travelMode":"car","routeType":"fastest","departAt":depart_at}
        r=requests.get(self.BASE_URL.format(locations=locations),params=params,timeout=self.timeout); r.raise_for_status()
        payload=r.json(); summary=payload["routes"][0]["summary"]
        return TomTomObservation(float(summary["travelTimeInSeconds"]),float(summary.get("noTrafficTravelTimeInSeconds",summary["travelTimeInSeconds"])),float(summary.get("lengthInMeters",float("nan"))),payload)
