import os, uvicorn, asyncio
#
from PIL import Image
from io import BytesIO
from contextlib import asynccontextmanager
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

# Home
WORKINGDIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Location of the server options file
options_location: Path = WORKINGDIR / "Options.yml"

supported_video_extentions = ["mp4", "m4a", "mov", "flv", "mkv", "ts", "gif"]
supported_resize_image_extensions = ["png", "jpeg", "jpg", "webp", "bmp"]
supported_download_image_extensions = ["png", "jpeg", "jpg", "webp", "gif", "ico", "svg"]

ise : HTTPException = HTTPException(status_code=500, detail="Internal Server Error")

# Slowapi rate limiter
limiter = Limiter(key_func=get_remote_address)

def startFastAPI(origins:list = []) -> None:
    # Add middleware
    fastAPI.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Run
    uvicorn.run(
        fastAPI,
        host="0.0.0.0",
        port=8081, # Backend runs on 8081, nginx is on 8080
        log_level="error",
        proxy_headers=True,
        forwarded_allow_ips="127.0.0.1",
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    """A 'lifespan context manager' that runs when FastAPI starts and stops. Used to start and stop scheduled tasks"""
    # Deferred imports avoid the module-level import cycle.
    from datetime import time
    from Scripts.ServerData import ServerData
    from Scripts.Tasks import ClearCacheTask, PurgeCacheTask, ScheduledExecute

    # Store asyncio tasks
    tasks = []

    # If cache should be delete periodically
    if not ServerData.getData("cache_persists"):

        # Create cache clearing tasks
        clear = ClearCacheTask(
            "Clear Cache Task",
            execute_every_hours=ServerData.getData("keep_cache_for_hours"),
        )
        purge = PurgeCacheTask(
            "Purge Cache Task",
            scheduled_executes=[
                ScheduledExecute(
                    time.fromisoformat(ServerData.getData("purge_cache_time"))
                )
            ],
            execute_now=True,
        )

        # Run the tasks
        tasks = [
            asyncio.create_task(clear.start_task()),
            asyncio.create_task(purge.start_task()),
        ]

    try:
        # Start fastAPI and wait for it to finish
        yield

    #? This will run when FastAPI is shutting down
    finally:
        # Cancel all tasks gracefully
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

# Create fastAPI instance
fastAPI:FastAPI = FastAPI(lifespan=lifespan)
fastAPI.state.limiter = limiter
fastAPI.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

class Color:
    # Font colors
    r = '\033[91m'
    g = '\033[92m'
    y = '\033[93m'
    b = '\033[94m'
    m = '\033[95m'
    c = '\033[96m'
    w = '\033[97m'

    # Text changes
    bold = '\033[1m'
    underline = '\033[4m'

    # Background colors
    redBg = '\033[41m'
    greenBg = '\033[42m'
    yellowBg = '\033[43m'
    blueBg = '\033[44m'
    magentaBg = '\033[45m'
    cyanBg = '\033[46m'
    whiteBg = '\033[47m'

    # reset
    re = '\033[0m'


def getIP(request:Request) -> str:
    """ Returns an IPv4 address attached in request headers """
    return request.headers.get("X-Forwarded-For", "Unknown IP").split(",")[0].strip()


def getCurrentTime() -> str:
    """ Returns: current time in format 'h:min:sec AM/PM, month/day/year'"""
    return datetime.now().strftime("%I:%M:%S %p, %m/%d/%Y")

def strip_image_metadata(path: Path) -> bytes:
    """
    Strip metadata from an image and return the image as bytes
    """
    if path.suffix.lower() == ".svg":
        return path.read_bytes()

    extension = path.suffix.lstrip(".").lower()
    if extension not in supported_download_image_extensions:
        raise ValueError(f"Unsupported downloadable image format: {extension}")

    with Image.open(path) as image:
        clean_image = Image.new(image.mode, image.size)
        clean_image.putdata(list(image.getdata()))

        image_format = image.format

        if image_format == "JPEG" and clean_image.mode not in ("RGB", "L"):
            clean_image = clean_image.convert("RGB")

        output = BytesIO()
        clean_image.save(output, format=image_format)

        return output.getvalue()