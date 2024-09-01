from fastapi import FastAPI, Query
from pydantic import BaseModel
import math
import time
from datetime import datetime, timedelta

app = FastAPI()


EARTH_RADIUS_KM = 6371  
EARTH_MASS_KG = 5.972e24  
EARTH_GRAVITY = 9.81  

SATELLITE_ORBIT_RADIUS_KM = EARTH_RADIUS_KM + 400  


TIME_SCALE = 1000  
START_TIME = datetime.utcnow()  
LAST_UPDATE_TIME = time.time() 
simulated_seconds = 0  
class EarthData(BaseModel):
    radius_km: float
    mass_kg: float
    gravity: float

class SatelliteData(BaseModel):
    x: float
    y: float

class TimeData(BaseModel):
    current_simulated_time: str

@app.get("/earth_data/")
def get_earth_data() -> EarthData:
    return EarthData(
        radius_km=EARTH_RADIUS_KM,
        mass_kg=EARTH_MASS_KG,
        gravity=EARTH_GRAVITY
    )

@app.get("/satellite_position/")
async def get_satellite_position() -> SatelliteData:
    global simulated_seconds, LAST_UPDATE_TIME
    
    current_real_time = time.time()
    delta_real_time = current_real_time - LAST_UPDATE_TIME

    simulated_seconds += delta_real_time * TIME_SCALE
    
    LAST_UPDATE_TIME = current_real_time

    orbital_period = 5400
    angle = (simulated_seconds % orbital_period) * 2 * math.pi / orbital_period
    x = SATELLITE_ORBIT_RADIUS_KM * math.cos(angle)
    y = SATELLITE_ORBIT_RADIUS_KM * math.sin(angle)
    return SatelliteData(x=x, y=y)

@app.get("/simulated_time/")
def get_simulated_time() -> TimeData:
    global simulated_seconds
    
    simulated_time = START_TIME + timedelta(seconds=simulated_seconds)
    return TimeData(current_simulated_time=simulated_time.strftime("%Y-%m-%d %H:%M:%S"))

@app.post("/set_time_scale/")
def set_time_scale(scale: float = Query(..., description="Multiplier for the time scale")):
    global TIME_SCALE, LAST_UPDATE_TIME, simulated_seconds
    
    current_real_time = time.time()
    delta_real_time = current_real_time - LAST_UPDATE_TIME
    simulated_seconds += delta_real_time * TIME_SCALE
    
    TIME_SCALE = scale
    
    LAST_UPDATE_TIME = current_real_time
    
    return {"message": f"Time scale set to {TIME_SCALE}"}
