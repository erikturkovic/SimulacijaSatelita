from fastapi import FastAPI, Query, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
import math
import time
from datetime import datetime, timedelta
from pathlib import Path
from database import engine, SessionLocal, Satellite, database

app = FastAPI()

EARTH_RADIUS_KM = 6371
EARTH_MASS_KG = 5.972e24
EARTH_GRAVITY = 9.81
SATELLITE_ORBIT_RADIUS_KM = EARTH_RADIUS_KM + 400

TIME_SCALE = 1000
START_TIME = datetime.utcnow()
LAST_UPDATE_TIME = time.time()
simulated_seconds = 0

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/earth_data/")
def get_earth_data() -> EarthData:
    return EarthData(
        radius_km=EARTH_RADIUS_KM,
        mass_kg=EARTH_MASS_KG,
        gravity=EARTH_GRAVITY
    )

@app.get("/satellite_position/")
async def get_satellite_position(db: Session = Depends(get_db)) -> SatelliteData:
    global simulated_seconds, LAST_UPDATE_TIME
    
    current_real_time = time.time()
    delta_real_time = current_real_time - LAST_UPDATE_TIME

    simulated_seconds += delta_real_time * TIME_SCALE
    
    LAST_UPDATE_TIME = current_real_time

    orbital_period = 5400
    angle = (simulated_seconds % orbital_period) * 2 * math.pi / orbital_period
    x = SATELLITE_ORBIT_RADIUS_KM * math.cos(angle)
    y = SATELLITE_ORBIT_RADIUS_KM * math.sin(angle)
    z = 0

    new_satellite = Satellite(x=x, y=y, z=z, created_at=datetime.utcnow())
    db.add(new_satellite)
    db.commit()
    
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

@app.get("/satellites/")
async def get_all_satellites():
    query = Satellite.__table__.select()
    results = await database.fetch_all(query)
    return results
