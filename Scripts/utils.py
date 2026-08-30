import os, uvicorn
#
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

# FastAPI
fastAPI:FastAPI = FastAPI()
ise : HTTPException = HTTPException(status_code=500, detail="Internal Server Error")

# Slowapi rate limiter
limiter = Limiter(key_func=get_remote_address)
fastAPI.state.limiter = limiter
fastAPI.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

def startFastAPI(host:str = "0.0.0.0", port:int=8080, origins:list = []) -> None:
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
        host=host,
        port=port,
        log_level="error",
        proxy_headers=True,
        forwarded_allow_ips="127.0.0.1",
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