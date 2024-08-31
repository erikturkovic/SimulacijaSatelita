from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import math
import time

app = FastAPI()

class SatelliteData(BaseModel):
    x: float
    y: float

EARTH_RADIUS = 200  
ORBIT_RADIUS = 300 
ORBIT_SPEED = 0.05  

@app.get("/satellite_position/")
async def get_satellite_position():
    current_time = time.time()
    angle = current_time * ORBIT_SPEED
    x = EARTH_RADIUS + ORBIT_RADIUS * math.cos(angle)
    y = EARTH_RADIUS + ORBIT_RADIUS * math.sin(angle)
    return SatelliteData(x=x, y=y)

