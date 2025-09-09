import os, uvicorn, platform
#
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

# Do something when this file is __main__
if __name__ == "__main__":
    from Color import Color
    print(f"{Color.red}You ran the wrong file! Run main.py instead.{Color.reset}")
    exit(0)
from Scripts.Color import Color

WORKINGDIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
configPath: Path = WORKINGDIR / "config.json"
OS = platform.system()
fastAPI:FastAPI = FastAPI()

videoExtentions = ["mp4", "m4a", "mov", "flv", "mkv", "ts", "gif"]
imageExtentions = ["png", "jpeg", "webp", "svg", "heic"] # Make sure pillow supports these types

def startFastAPI(host:str="0.0.0.0", port:int=80, log_level:str="error", proxy_headers:bool=True):
    print(f"\n{Color.yellow}Starting FastAPI...{Color.reset}")
    fastAPI.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    uvicorn.run(fastAPI, host=host, port=port, log_level=log_level, proxy_headers=proxy_headers)

def getIP(request:Request) -> str:
    """ Returns an IPv4 address attached in request headers """
    return request.headers.get("X-Forwarded-For", "Unknown IP").split(",")[0].strip()

def getCurrentTime() -> str:
    """ Returns: current time in format 'h:min:sec AM/PM, month/day/year'"""
    return datetime.now().strftime("%I:%M:%S %p, %m/%d/%Y")