import asyncio
import uvicorn

async def start_server(port: int):
    config = uvicorn.Config("backend:app", host="127.0.0.1", port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    ports = [8000, 8001, 8002]
    tasks = [start_server(port) for port in ports]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
