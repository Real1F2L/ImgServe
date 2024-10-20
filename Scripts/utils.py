import json, os, uvicorn, sys, logging, platform
#
from datetime import datetime
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from typing import Generator
from datetime import datetime

class utils:
    _currentWorkingDirectory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    #* Vars loaded from config.json
    _root = "./files/" # the folder to share files from
    _CacheLocation = "./cache/" # the path to save the cache
    _Platform = platform.system()

    _DoClearCache = True #? should we clear the cache
    _clearVideoCache = False #? should we clear video cache (this can be very CPU intensive if enabled)
    _clearCacheHrs = 1 #? Hours between each cache clear
    _doVideoResizing = True #? should we resize videos?

    _videoTypes = ["mp4", "m4a", "mov", "flv", "mkv", "ts", "gif"]
    _imageTypes = ["png", "jpg", "jpeg", "webp", "svg", "heic"] #? supported image types, make sure PIL supports these
    _dontShareNames = ["Dockerfile", ".gitignore", ".venv", ".pyCache", "__pycache__", ".git"] #? file/folders to not share

    _vidBitrate = "500K" #? video bitrate, K = kilobits, M = megabits, G = gigabits
    _vidScaleX = 854 #? video scale width
    _vidScaleY = 480 #? video scale height

    # only change these if you know how to use ffmpeg
    _vidAcodec = "aac"
    _vidVcodec = "libaom-av1"

    #* Loggers
    # make new loggers
    _RequestLogger = logging.getLogger("RequestLogger")
    _ErrorLogger = logging.getLogger("ErrorLogger")

    # make handlers
    os.makedirs(os.path.join(_currentWorkingDirectory, "Logs"), exist_ok=True)
    _requestLoggerHandler = logging.FileHandler(os.path.join(_currentWorkingDirectory, "Logs", "RequestLogs.log"))
    _errorLoggerHandler = logging.FileHandler(os.path.join(_currentWorkingDirectory, "Logs", "ErrorLogs.log"))

    # formatters
    _logFormatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')

    # set handlers
    _requestLoggerHandler.setFormatter(_logFormatter)
    _errorLoggerHandler.setFormatter(_logFormatter)

    # add handlers
    _RequestLogger.addHandler(_requestLoggerHandler)
    _ErrorLogger.addHandler(_errorLoggerHandler)

    # set level
    _RequestLogger.setLevel(logging.INFO)
    _ErrorLogger.setLevel(logging.ERROR)

    @staticmethod
    def loadConfig() -> None:
        # make config file if it doesnt exist
        if not os.path.exists(os.path.join(utils._currentWorkingDirectory, "config.json")):
            with open(os.path.join(utils._currentWorkingDirectory, "config.json"), "w") as conf:
                json.dump({"RootLocation" : "./Files/", "CacheLocation" : "./Cache/", "DoClearCache" : True, "DoClearVideoCache" : False, "ClearCacheHrs" : 24, "DoVideoResizing" : True, "VideoScaleX" : 854, "VideoScaleY" : 480, "VideoBitrate" : "500K", "DontShareNames" : ["Dockerfile", ".gitignore", ".venv", ".pyCache", "__pycache__", ".git"]}, conf, indent=4)
                conf.close()

        # load from config file
        with open(os.path.join(utils._currentWorkingDirectory, "config.json"), "r") as conf:
            try:
                # load json data
                _json:dict = json.load(conf)
                utils._root = _json.get("RootLocation", "./Files/")
                utils._CacheLocation = _json.get("CacheLocation", "./Cache/")
                utils._DoClearCache = _json.get("DoClearCache", True)
                utils._clearVideoCache = _json.get("DoClearVideoCache", False)
                utils._clearCacheHrs = _json.get("ClearCacheHrs", 1)
                utils._doVideoResizing = _json.get("DoVideoResizing", True)

                utils._vidBitrate = _json.get("VideoBitrate", "500K")
                utils._vidScaleX = _json.get("VideoScaleX", 854)
                utils._vidScaleY = _json.get("VideoScaleY", 480)

                utils._dontShareNames = _json.get("DontShareNames", ["Dockerfile", ".gitignore", ".venv", ".pyCache", "__pycache__", ".git"])
                
                # make folders
                os.makedirs(utils._CacheLocation, exist_ok=True)
                os.makedirs(utils._root, exist_ok=True)

                if utils._doVideoResizing and utils._DoClearCache and utils._clearVideoCache:
                    print(f"\n{utils.color.y}[loadConfig] _clearVideoCache is set to True. {utils.color.re} Video cache will be cleared every {utils._clearCacheHrs} hrs. Video resizing can be EXTREMELY CPU intensive and may take long periods of time!")

            except Exception as e:
                print(f"{utils.color.r}[loadConfig] CIRITCAL ERROR LOADING CONFIG: {e}{utils.color.re}")
                utils._ErrorLogger.exception(f"CRITICAL ERROR LOADING CONFIG: {e} SYSTEM WILL EXIT IMMEDIATELY")
                sys.exit(1)

    fastAPI:FastAPI = FastAPI()
    fastAPI.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @staticmethod
    def startFastapi() -> None:
        uvicorn.run(utils.fastAPI, host="0.0.0.0", port=80, log_level="error", proxy_headers=True) #? 20033 - project API

    @staticmethod
    class color:
        # Foreground
        r = '\033[91m'
        g = '\033[92m'
        y = '\033[93m'
        b = '\033[94m'
        m = '\033[95m'
        c = '\033[96m'
        w = '\033[97m'
        re = '\033[0m'
        bold = '\033[1m'
        underline = '\033[4m'

        # Background
        rbg = '\033[41m'
        gbg = '\033[42m'
        ybg = '\033[43m'
        bbg = '\033[44m'
        mbg = '\033[45m'
        cbg = '\033[46m'
        wbg = '\033[47m'
        rebg = '\033[0m'

    #! DEPRECATED
    @staticmethod  
    def getDirSize(directory_path) -> int:
        total_size:int = 0
        for rootPath, _, fileList in os.walk(directory_path):
            for file in fileList:
                path = os.path.join(rootPath, file)
                total_size += os.path.getsize(path)
        return total_size

    @staticmethod
    def getIP(request:Request) -> str:
        """Returns an IP address of the client"""
        return request.headers.get("X-Forwarded-For", "Unknown IP").split(",")[0].strip()
    
    @staticmethod
    def video_streamer(file_path: str) -> Generator[bytes, None, None]:
        with open(file_path, mode="rb") as video_file:
            while chunk := video_file.read(1024 * 1024):
                yield chunk

    def getCurrentTime() -> str:
        # time in hour:minute:second AM/PM, month/day/year
        return datetime.now().strftime("%I:%M:%S %p, %m/%d/%Y")

if __name__ == "__main__":
    print("[utils.py] Oops... you can the wrong file :(\nTry opening __init__.py next time!\n")
    input("Press Enter to exit...")
    sys.exit(0)