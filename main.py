# © 2025 1F2L - gegeha.com
# v1.1.1
# Thank you for checking out ImgServe!
#
# ImgServe is a free and open source image serving API.
# Built for minimizing website load times and bandwidth.
# Serve images at the correct size in a modern format!
#
# Contributions and modding are allowed, please do not sell ImgServe.
# Exact specifications in LICENSE
import os, time, threading, re
#
from pathlib import Path
from urllib.parse import unquote
from PIL import Image

# Scripts
from Scripts import utils
from Scripts.Config import Config
from Scripts.Logs import Logs
from Scripts.Color import Color

# FastAPI
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from fastapi import Request, Response

Image.MAX_IMAGE_PIXELS = None


@utils.fastAPI.middleware("http")
async def middleware(request: Request, call_next):
    # Gather request info
    
    # Get IP
    ip = request.headers.get("x-forwarded-for", "")
    if ip:
        ip = ip.split(',')[0].strip()
    else:
        ip = request.client.host if request.client else ""
    path = request.url.path
    method = request.method

    #? Process request through routes
    response: Response = await call_next(request)

    # 0 for success, 1 for maybe, 2 for BAD
    good: int = 0 if response.status_code in [200, 201] else 1 if response.status_code in [307] else 2
    rjust: int = 80

    # Log request
    if request.url.path != "/favicon.ico":
        message: str = "".join(
            (
                Color.green if good == 0 else Color.yellow if good == 1 else Color.red,
                f"[{method}] ",
                Color.reset,
                f"{ip} - {path} ",
                Color.green if good == 0 else Color.yellow if good == 1 else Color.red,
                #                                  rjust - (method + brackets and spaces + ip + spaces and dash + path + status code length)
                f" {f" {response.status_code}".rjust(rjust - (len(method) + 3 + len(ip) + 3 + len(path) + len(str(response.status_code))), "-")}",
                Color.reset
            )
        )

        print(message)

    Logs.requestLogger().info(f"[{method}] {ip} - {path} [{response.status_code}]")

    # Headers
    response.headers["Server"] = Config.get("Server", "")
    response.headers["Server-URL"] = Config.get("ServerURL", "")
    response.headers["Server-Version"] = Config.get("ServerVersion", "v1.1.1")
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["Cache-Control"] = "no-store"

    # Return response
    return response
 
# Request resized image
@utils.fastAPI.get("/image/resize")
async def resizeImg(request:Request):
    """ 
    Resizes an image in the db and returns it 

    Query Params:
        f - The location of the file you want
        s - The resolution you want the image to be returned (ex. "1280x720")
        t - The file type of response (default webp)
        ar - Keep aspect ratio
    """
    query = request.query_params
    reqFile = query.get("f") # f

    # Query param are required
    if not query or not reqFile:
        raise HTTPException(status_code=404)
    assert reqFile is not None
    reqFile = unquote(reqFile)

    img: Path = Path(str(Config.get("FileLocation"))) / reqFile

    # \d+ matches one or more digits, groups for each digit
    resMatch = re.match(r"(\d+)x(\d+)", unquote(query.get("s", "64x64")))

    if not resMatch:
        return HTTPException(status_code=400, detail="Size must be written in format ###x###")
    width, height = map(int, resMatch.groups())

    # Cap width and heigh to not hurt CPU too hard
    if width > 3000: width = 3000
    if height > 2000: height = 2000

    requestedType = unquote(query.get("t", "webp"))
    aspectRatio = unquote(query.get("ar", "y"))

    basename = img.name
    cacheSavePath: Path = Path(str(Config["cacheLocation"])) / f"{str(img).replace("\\", "_")}_{width}x{height}_{"y" if aspectRatio == "y" else "n"}.{requestedType}"

    # Check if the location is good
    if not img.exists():
        raise HTTPException(status_code=404)
    elif not img.is_file():
        raise HTTPException(status_code=400, detail="File location is a directory")
    
    else:
        # Check if the image type is supported
        if (img.suffix.replace(".", "") in utils.imageExtentions):
            
            # Look for the image in cache
            if (cacheSavePath.exists()):
                return FileResponse(
                    path=cacheSavePath,
                    filename=f"{img.stem}.{requestedType}",
                    media_type=f"image/{requestedType}"
                )

            # Resize image with Pillow
            with Image.open(img) as image:
                if aspectRatio == "y":
                    image.thumbnail((width, height), Image.Resampling.LANCZOS)
                    image.save(cacheSavePath, format=requestedType)
                else:
                    resizedImg = image.resize((width, height), Image.Resampling.LANCZOS)
                    resizedImg.save(cacheSavePath, format=requestedType)

                # Return the new resized image
                return FileResponse(
                    path=cacheSavePath,
                    filename=f"{img.stem}.{requestedType}",
                    media_type=f"image/{requestedType}"
                )

        # Not a supported image, just return the full image
        else:
            return FileResponse(img, filename=f"{img.name}")
        

@utils.fastAPI.get("/image/download")
async def downloadImg(request:Request):
    """ 
    Returns a raw image 
    
    Query Params:
        f - The location of the file you want
    """
    query = request.query_params
    reqFile = query.get("f") # f

    # Query param are required
    if not query or not reqFile:
        raise HTTPException(status_code=404)
    assert reqFile is not None
    reqFile = unquote(reqFile)

    img: Path = Path(str(Config["fileLocation"])) / reqFile

    # Check if the location is good
    if not img.exists():
        raise HTTPException(status_code=404)
    elif not img.is_file():
        raise HTTPException(status_code=400, detail="File location is a directory")
    
    else:
        return FileResponse(path=img, filename=img.name)


def deleteCacheThread():
    print("Clear cache thread started!")
    cacheLocation: Path = Path(str(Config["cacheLocation"]))

    # infinite loop
    while True:
        
        # Make the cache folder
        cacheLocation.mkdir(parents=True, exist_ok=True)
        
        # Each file in cache folder
        for file in os.listdir(cacheLocation):
            filePath: Path = cacheLocation / file

            # Delete file
            filePath.unlink()

        print(f"\n{Color.green}Cache successfully cleared at {utils.getCurrentTime()}{Color.reset}")
        Logs.getLogger("CacheLogger").info(f"Cache cleared successfully")
        
        # Wait for next cache clear
        time.sleep(Config.get("clearCacheEveryHours", 4) * 3600)

# Main
if __name__ == "__main__":
    print(f"\n{Color.yellow}Running Main:{Color.reset}\nFound working directory: {utils.WORKINGDIR}")
    print(f"Config test: fileLocation={Config["fileLocation"]}, cacheLocation={Config["cacheLocation"]}, logLocation={Config["logLocation"]}")
    Logs.getLogger("TestLogger").info("This is a test to confirm Logs are working!")

    # Create file location folder
    Path(str(Config["fileLocation"])).mkdir(parents=True, exist_ok=True)

    # Start clear cache thread
    if Config["doClearCache"] == True:
        threading.Thread(target=deleteCacheThread).start()

    # Start FastAPI
    utils.startFastAPI()
