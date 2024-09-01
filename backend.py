from fastapi import FastAPI, Query
from pydantic import BaseModel
import math
import time

app = FastAPI()

# Constants for Earth
EARTH_RADIUS_KM = 6371  # Earth's radius in kilometers
EARTH_MASS_KG = 5.972e24  # Earth's mass in kilograms
EARTH_GRAVITY = 9.81  # Acceleration due to gravity in m/s^2

# Constants for the Satellite
SATELLITE_ORBIT_RADIUS_KM = EARTH_RADIUS_KM + 400  # Typical Low Earth Orbit (LEO) altitude in kilometers

# Global time scale, modifiable via an endpoint
TIME_SCALE = 1000  # Default scale: 1 real second = ~17 simulated minutes

class EarthData(BaseModel):
    radius_km: float
    mass_kg: float
    gravity: float

class SatelliteData(BaseModel):
    x: float
    y: float

@app.get("/earth_data/")
def get_earth_data() -> EarthData:
    return EarthData(
        radius_km=EARTH_RADIUS_KM,
        mass_kg=EARTH_MASS_KG,
        gravity=EARTH_GRAVITY
    )

@app.get("/satellite_position/")
async def get_satellite_position() -> SatelliteData:
    current_time = time.time() * TIME_SCALE  # Use the global time scale
    orbital_period = 5400  # 1.5 hours for a full orbit, typical of LEO satellites
    angle = (current_time % orbital_period) * 2 * math.pi / orbital_period
    x = SATELLITE_ORBIT_RADIUS_KM * math.cos(angle)
    y = SATELLITE_ORBIT_RADIUS_KM * math.sin(angle)
    return SatelliteData(x=x, y=y)

@app.post("/set_time_scale/")
def set_time_scale(scale: float = Query(..., description="Multiplier for the time scale")):
    global TIME_SCALE
    TIME_SCALE = scale
    return {"message": f"Time scale set to {TIME_SCALE}"}