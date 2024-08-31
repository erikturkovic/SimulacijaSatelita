from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import math
import time

app = FastAPI()

class SatelliteData(BaseModel):
    x: float
    y: float

class EarthData(BaseModel):
    radius_km: float
    mass_kg: float
    gravity: float


EARTH_RADIUS_KM = 12742  
EARTH_MASS_KG = 5.972e24  
EARTH_GRAVITY = 9.81     

@app.get("/earth_data/")
def get_earth_data() -> EarthData:
    return EarthData(
        radius_km=EARTH_RADIUS_KM,
        mass_kg=EARTH_MASS_KG,
        gravity=EARTH_GRAVITY
    )

@app.get("/satellite_position/")
async def get_satellite_position() -> SatelliteData:
    current_time = time.time()
    angle = current_time * 0.05
    orbit_radius = EARTH_RADIUS_KM + 0.1  
    x = orbit_radius * math.cos(angle)
    y = orbit_radius * math.sin(angle)
    return SatelliteData(x=x, y=y)
