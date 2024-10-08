from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import math
import time
from datetime import datetime, timedelta
import sqlite3
import os
import signal
import sys

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

class CombinedData(BaseModel):
    earth_data: EarthData
    satellite_positions: list[SatelliteData]
    current_simulated_time: str

def get_all_satellites_from_db():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name, x, y, z, orbital_period, direction, orbit_type FROM satellites")
        satellites = cursor.fetchall()
        conn.close()
        return satellites
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

def update_simulation_time(new_time_seconds: float):
    global simulated_seconds, LAST_UPDATE_TIME
    simulated_seconds = new_time_seconds
    LAST_UPDATE_TIME = time.time()

@app.post("/update_simulation_time/")
async def update_simulation_time_endpoint(request: Request):
    data = await request.json()
    time_seconds = data.get("time_seconds")
    if time_seconds is not None:
        update_simulation_time(time_seconds)
        return {"message": "Simulation time updated", "time_seconds": time_seconds}
    else:
        raise HTTPException(status_code=400, detail="Invalid time_seconds value")

@app.get("/earth_data/")
def get_earth_data() -> EarthData:
    return EarthData(
        radius_km=EARTH_RADIUS_KM,
        mass_kg=5.972e24,
        gravity=9.81
    )

@app.get("/combined_data/")
async def get_combined_data() -> CombinedData:
    global simulated_seconds, LAST_UPDATE_TIME

    current_real_time = time.time()
    delta_real_time = current_real_time - LAST_UPDATE_TIME
    simulated_seconds += delta_real_time * TIME_SCALE
    LAST_UPDATE_TIME = current_real_time

    earth_data = EarthData(
        radius_km=EARTH_RADIUS_KM,
        mass_kg=5.972e24,
        gravity=9.81
    )

    satellites = get_all_satellites_from_db()
    satellite_positions = []

    for satellite in satellites:
        name, x_initial, y_initial, z_initial, orbital_period, direction, orbit_type = satellite

        angle = direction * (simulated_seconds % orbital_period) * 2 * math.pi / orbital_period

        if orbit_type == 'XY':
            x = x_initial * math.cos(angle) - y_initial * math.sin(angle)
            y = x_initial * math.sin(angle) + y_initial * math.cos(angle)
            z = z_initial
        elif orbit_type == 'XZ':
            x = x_initial * math.cos(angle) - z_initial * math.sin(angle)
            y = y_initial * math.cos(angle) - z_initial * math.sin(angle)
            z = z_initial
        elif orbit_type == 'YZ':
            x = x_initial * math.sin(angle) + y_initial * math.cos(angle)
            y = y_initial * math.cos(angle) - z_initial * math.sin(angle)
            z = z_initial
        else:
            x = x_initial * math.cos(angle) - y_initial * math.sin(angle)
            y = x_initial * math.sin(angle) + y_initial * math.cos(angle)
            z = z_initial

        satellite_positions.append(SatelliteData(name=name, x=x, y=y, z=z))

    simulated_time = START_TIME + timedelta(seconds=simulated_seconds)

    return CombinedData(
        earth_data=earth_data,
        satellite_positions=satellite_positions,
        current_simulated_time=simulated_time.strftime("%Y-%m-%d %H:%M:%S")
    )

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

@app.post("/shutdown/")
def shutdown():
    global simulated_seconds
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE simulation_time SET last_simulated_seconds = ? WHERE id = 1", (simulated_seconds,))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    import requests
    for port in range(8001, 8006):
        if port != int(os.getenv("PORT", 8001)):
            try:
                requests.post(f"http://127.0.0.1:{port}/update_simulation_time/", json={"time_seconds": simulated_seconds})
            except requests.RequestException:
                pass

    print("Shutting down the server...")

    pid = os.getpid() 
    os.kill(pid, signal.SIGTERM)  

    return {"message": "Shutting down..."}

def save_simulation_state():
    global simulated_seconds
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE simulation_time SET last_simulated_seconds = ? WHERE id = 1", (simulated_seconds,))
        conn.commit()
        conn.close()
        print(f"Simulation state saved with {simulated_seconds} seconds.")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

def shutdown_server():
    pid = os.getpid()  
    os.kill(pid, signal.SIGTERM)  

def handle_shutdown_signal(signum, frame):
    print("Received shutdown signal. Saving state and shutting down...")
    save_simulation_state()
    shutdown_server()


signal.signal(signal.SIGINT, handle_shutdown_signal)
signal.signal(signal.SIGTERM, handle_shutdown_signal)

@app.post("/shutdown/")
def shutdown():
    handle_shutdown_signal(None, None)
    return {"message": "Shutting down..."}

@app.get("/save_state/")
def save_state():
    save_simulation_state()
    return {"message": "State saved."}