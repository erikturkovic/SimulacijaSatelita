from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import asyncio
import random

app = FastAPI()

app.mount("/", StaticFiles(directory="static", html=True), name="static")

satellite_data = {
    "position": {"x": 0, "y": 0, "z": 0},
    "speed": 0.0,
}

async def update_satellite_data():
    while True:
        satellite_data["position"]["x"] += random.uniform(-1, 1)
        satellite_data["position"]["y"] += random.uniform(-1, 1)
        satellite_data["position"]["z"] += random.uniform(-1, 1)
        satellite_data["speed"] = random.uniform(0, 10)
        await asyncio.sleep(1)

@app.on_event("startup")
async def start_simulation():
    asyncio.create_task(update_satellite_data())

@app.get("/satellite")
async def get_satellite_data():
    return satellite_data


#python -m uvicorn main:app --reload --port 8000