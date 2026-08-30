import asyncio, shutil
#
from pathlib import Path
from urllib.parse import unquote
from PIL import Image
from fastapi import Request, Response
from datetime import time

# Scripts
from Scripts import utils
from Scripts.utils import Color
from Scripts.ServerData import ServerData
from Scripts.Tasks import ClearCacheTask, PurgeCacheTask, ScheduledExecute

# Routes
from routes import Images
from routes import Files


# Middleware runs before every request is processed
@utils.fastAPI.middleware("http")
async def middleware(request: Request, call_next):
    # Gather request info
    xff: str = request.headers.get("x-forwarded-for").split(',')[0].strip() if request.headers.get("x-forwarded-for") else None
    ip = xff if xff else request.client.host
    path = request.url.path
    method = request.method
    query = request.query_params

    #* Allow request to be processed
    response: Response = await call_next(request)

    # 0 for success, 1 for redirect, 2 for failed
    good = 0 if response.status_code in [200, 201] else 1 if response.status_code in [307] else 2
    color = Color.g if good == 0 else Color.y if good == 1 else Color.r
    rjust: int = 80

    # Log request
    if request.url.path != "/favicon.ico":
        message: str = "".join(
            (
                color,
                f"[{method}] ",
                Color.re,
                f"{ip} - {path} ",
                color,
                f" {(" " + str(response.status_code)).rjust(rjust - (len(method) + 3 + len(ip) + 3 + len(path) + len(str(response.status_code))), "-")}",
                Color.re
            )
        )
        print(message)

    # Set response headers
    response.headers["Server"] = ServerData.getData("server_name")
    response.headers["Server-Version"] = ServerData.getData("server_version")
    response.headers["Server-URL"] = ServerData.getData("server_url")
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["Cache-Control"] = "no-store"

    # Return response
    return response

 
async def start_cache_tasks():
    """Starts the cache clearing and purging tasks"""
    cache_persists = bool(ServerData.getData("cache_persists"))

    if not cache_persists:
        print(f"{Color.y}Creating cache clearing tasks...\n{Color.re}")

        # Create clear cache task
        clear_cache_task = ClearCacheTask("Clear Cache Task", execute_every_hours=1)


        # Load purge time
        purge_cache_time = time.fromisoformat(ServerData.getData("purge_cache_time"))
        purge_cache_schedule = ScheduledExecute(purge_cache_time)

        # Create purge task
        purge_cache_task = PurgeCacheTask("Purge Cache Task", scheduled_executes=[purge_cache_schedule], execute_now=True)

        # Start both in the background
        asyncio.create_task(clear_cache_task.start_task())
        asyncio.create_task(purge_cache_task.start_task())


# Main
if __name__ == "__main__":

    # Create Library folder
    ServerData.get_library_path().mkdir(exist_ok=True)

    # Copy front-end assets into Library
    asset_folder = utils.WORKINGDIR / "www/src/assets"
    shutil.copytree(
        asset_folder,
        ServerData.get_library_path() / "ImgServe Web UI",
        dirs_exist_ok=True
    )

    # Create Cache folder
    ServerData.get_cache_path().mkdir(exist_ok=True)

    # Start cache tasks
    asyncio.run(start_cache_tasks())

    # Start FastAPI
    print(f"\n\n{Color.y}Starting FastAPI...\n{Color.re}")
    utils.startFastAPI(host=ServerData.getData("host"), port=ServerData.getData("port"), origins=ServerData.getData("CORS_origins"))
