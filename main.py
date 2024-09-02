import sqlite3
import subprocess
import os

DATABASE_PATH = "database.db"

def get_all_satellite_ids():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM satellites")
        satellites = cursor.fetchall()
        conn.close()
        return [sat[0] for sat in satellites]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

def start_uvicorn_instance(satellite_id, port):
    env = os.environ.copy()
    env['SATELLITE_ID'] = str(satellite_id)
    subprocess.Popen([
        "python", "-m", "uvicorn", "backend:app", 
        "--host", "127.0.0.1", "--port", str(port), 
        "--reload", "--log-level", "info", "--workers", "1"
    ], env=env)

def main():
    satellite_ids = get_all_satellite_ids()
    base_port = 8000

    for i, satellite_id in enumerate(satellite_ids):
        port = base_port + i + 1
        start_uvicorn_instance(satellite_id, port)
        print(f"Started Uvicorn instance for satellite {satellite_id} on port {port}")

if __name__ == "__main__":
    main()