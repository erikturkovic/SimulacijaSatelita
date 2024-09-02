from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import math
import time
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3

app = FastAPI()

# Constants
EARTH_RADIUS_KM = 6371
EARTH_MASS_KG = 5.972e24
EARTH_GRAVITY = 9.81

TIME_SCALE = 1000
START_TIME = datetime.utcnow()
LAST_UPDATE_TIME = time.time()
simulated_seconds = 0

DATABASE_PATH = "database.db"

class EarthData(BaseModel):
    radius_km: float
    mass_kg: float
    gravity: float

class SatelliteData(BaseModel):
    x: float
    y: float
    z: float

class TimeData(BaseModel):
    current_simulated_time: str

def get_satellite_from_db():
    """Fetch the satellite's initial position from the database."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT x, y, z FROM satellites WHERE id = 1")
        satellite = cursor.fetchone()
        conn.close()
        if satellite:
            return satellite
        else:
            raise HTTPException(status_code=404, detail="Satellite not found in the database.")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

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
    
    satellite = get_satellite_from_db()
    if satellite is None:
        raise HTTPException(status_code=404, detail="Satellite not found.")
    
    x_initial, y_initial, z_initial = satellite

    current_real_time = time.time()
    delta_real_time = current_real_time - LAST_UPDATE_TIME
    simulated_seconds += delta_real_time * TIME_SCALE
    LAST_UPDATE_TIME = current_real_time


    orbital_period = 5400  
    angle = (simulated_seconds % orbital_period) * 2 * math.pi / orbital_period

    x = (EARTH_RADIUS_KM + 400) * math.cos(angle)
    y = (EARTH_RADIUS_KM + 400) * math.sin(angle)
    z = z_initial

    return SatelliteData(x=x, y=y, z=z)


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

@app.get("/earth_image/")
async def get_earth_image():
    return FileResponse(Path("pngs/earth.png"))
