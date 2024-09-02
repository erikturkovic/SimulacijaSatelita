from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import math
import time
from datetime import datetime, timedelta
import sqlite3

app = FastAPI()

EARTH_RADIUS_KM = 6371
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
    name: str
    x: float
    y: float
    z: float

class TimeData(BaseModel):
    current_simulated_time: str

def get_all_satellites_from_db():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name, x, y, z, orbital_period, direction FROM satellites")
        satellites = cursor.fetchall()
        conn.close()
        return satellites
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@app.get("/earth_data/")
def get_earth_data() -> EarthData:
    return EarthData(
        radius_km=EARTH_RADIUS_KM,
        mass_kg=5.972e24,
        gravity=9.81
    )

@app.get("/satellite_positions/")
async def get_satellite_positions() -> list[SatelliteData]:
    global simulated_seconds, LAST_UPDATE_TIME
    
    satellites = get_all_satellites_from_db()
    
    satellite_positions = []

    current_real_time = time.time()
    delta_real_time = current_real_time - LAST_UPDATE_TIME
    simulated_seconds += delta_real_time * TIME_SCALE
    LAST_UPDATE_TIME = current_real_time

    for satellite in satellites:
        name, x_initial, y_initial, z_initial, orbital_period, direction = satellite

        angle = direction * (simulated_seconds % orbital_period) * 2 * math.pi / orbital_period

        x = (EARTH_RADIUS_KM + 400) * math.cos(angle)
        y = (EARTH_RADIUS_KM + 400) * math.sin(angle)
        z = z_initial

        satellite_positions.append(SatelliteData(name=name, x=x, y=y, z=z))

    return satellite_positions

@app.get("/simulated_time/")
def get_simulated_time() -> TimeData:
    global simulated_seconds
    
    simulated_time = START_TIME + timedelta(seconds=simulated_seconds)
    return TimeData(current_simulated_time=simulated_time.strftime("%Y-%m-%d %H:%M:%S"))

@app.post("/set_time_scale/")
def set_time_scale(scale: float):
    global TIME_SCALE, LAST_UPDATE_TIME, simulated_seconds
    
    current_real_time = time.time()
    delta_real_time = current_real_time - LAST_UPDATE_TIME
    simulated_seconds += delta_real_time * TIME_SCALE
    
    TIME_SCALE = scale
    LAST_UPDATE_TIME = current_real_time
    
    return {"message": f"Time scale set to {TIME_SCALE}"}

@app.get("/earth_image/")
async def get_earth_image():
    return FileResponse("pngs/earth.png")
