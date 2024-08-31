from fastapi import FastAPI
import uvicorn
import asyncio
from vpython import vector, sphere, textures, rate, norm, mag

# Constants
G = 6.67e-11
RE = 6.378e6
ME = 5.972e24

# Global Variables
simulation_task = None
satellites = []

# FastAPI app
app = FastAPI()

# Define Earth
Earth = sphere(pos=vector(-RE, 0, 0), radius=RE, texture=textures.earth)
Earth.m = ME

def create_satellite(pos, velocity, mass, radius):
    sat = sphere(pos=pos, radius=radius, make_trail=True)
    sat.m = mass
    sat.p = sat.m * velocity
    return sat

def update_position(sat, dt):
    r = sat.pos - Earth.pos
    F = -G * Earth.m * sat.m * norm(r) / mag(r)**2
    sat.p = sat.p + F * dt
    sat.pos = sat.pos + sat.p * dt / sat.m

async def run_simulation(dt):
    while True:
        rate(400)
        for sat in satellites:
            update_position(sat, dt)
        await asyncio.sleep(0)  # Yield control to the event loop

@app.post("/start")
async def start_simulation():
    global simulation_task, satellites
    if simulation_task and not simulation_task.done():
        return {"status": "Simulation already running"}
    
    # Create satellites
    satellites = [
        create_satellite(vector(2 * RE, 0, 0), vector(0, 5000, 0), 100, 0.03 * RE),
        create_satellite(vector(2 * RE, 10, 15), vector(1000, 5000, 2000), 100, 0.03 * RE)
    ]
    
    simulation_task = asyncio.create_task(run_simulation(1))
    return {"status": "Simulation started"}

@app.post("/stop")
async def stop_simulation():
    global simulation_task
    if simulation_task:
        simulation_task.cancel()
        try:
            await simulation_task
        except asyncio.CancelledError:
            pass
        return {"status": "Simulation stopped"}
    else:
        return {"status": "No simulation running"}

@app.get("/status")
async def simulation_status():
    global simulation_task
    if simulation_task and not simulation_task.done():
        return {"status": "Simulation running"}
    else:
        return {"status": "Simulation not running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)