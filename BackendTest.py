from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import threading

app = FastAPI()

class Satellite(BaseModel):
    pos: List[float]
    velocity: List[float]
    mass: float
    radius: float

satellites = []

@app.post("/add_satellite/")
def add_satellite(sat: Satellite):
    global satellitess
    pos = vector(*sat.pos)
    velocity = vector(*sat.velocity)
    satellite = create_satellite(pos, velocity, sat.mass, sat.radius)
    satellites.append(satellite)
    return {"status": "Satellite added"}

@app.post("/start_simulation/")
def start_simulation(duration: int, dt: float):
    def simulation_thread():
        run_simulation(satellites, duration, dt)

    thread = threading.Thread(target=simulation_thread)
    thread.start()
    return {"status": "Simulation started"}

@app.get("/satellite_positions/")
def get_positions():
    return [{"pos": [sat.pos.x, sat.pos.y, sat.pos.z]} for sat in satellites]

#uvicorn BackendTest:app --reload