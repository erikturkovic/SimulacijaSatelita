from fastapi import FastAPI
from pydantic import BaseModel
import asyncio

app = FastAPI()

class SatelliteData(BaseModel):
    x: float
    y: float

@app.post("/satellite_position/")
async def get_satellite_position():

    return SatelliteData(x=0.0, y=100.0)

