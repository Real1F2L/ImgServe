import os, time, threading, re
#
from pathlib import Path
from urllib.parse import unquote
from PIL import Image
from fastapi import Request, Response

# Scripts
from Scripts import utils
from Scripts.utils import Color
from Scripts.ServerData import ServerData

# Routes
from routes import Images



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
 
# Request resized image
# @utils.fastAPI.get("/image/resize")
# async def resizeImg(request:Request):
#     """ 
#     Resizes an image in the db and returns it 

#     Query Params:
#         f - The location of the file you want
#         s - The resolution you want the image to be returned (ex. "1280x720")
#         t - The file type of response (default webp)
#         ar - Keep aspect ratio
#     """
#     query = request.query_params
#     reqFile = query.get("f") # f

#     # Query param are required
#     if not query or not reqFile:
#         raise HTTPException(status_code=404, detail="You must supply a file in url query")
#     assert reqFile is not None
#     reqFile = unquote(reqFile)

#     img: Path = Path(str(ServerData["fileLocation"])) / reqFile

#     # \d+ matches one or more digits, groups for each digit
#     resMatch = re.match(r"(\d+)x(\d+)", unquote(query.get("s", "64x64")))

#     if not resMatch:
#         return HTTPException(status_code=400, detail="Size must be written in format ###x###")
#     width, height = map(int, resMatch.groups())

#     # Cap width and heigh to not hurt CPU too hard
#     if width > 3000: width = 3000
#     if height > 2000: height = 2000

#     requestedType = unquote(query.get("t", "webp"))
#     aspectRatio = unquote(query.get("ar", "y"))

#     basename = img.name
#     cacheSavePath: Path = Path(str(ServerData["cacheLocation"])) / f"{str(img).replace("\\", "_")}_{width}x{height}_{"y" if aspectRatio == "y" else "n"}.{requestedType}"

#     # Check if the location is good
#     if not img.exists():
#         raise HTTPException(status_code=404)
#     elif not img.is_file():
#         raise HTTPException(status_code=400, detail="File location is a directory")
    
#     else:
#         # Check if the image type is supported
#         if (img.suffix.replace(".", "") in utils.supported_image_extensions):
            
#             # Look for the image in cache
#             if (cacheSavePath.exists()):
#                 return FileResponse(
#                     path=cacheSavePath,
#                     filename=f"{img.stem}.{requestedType}",
#                     media_type=f"image/{requestedType}"
#                 )

#             # Resize image with Pillow
#             with Image.open(img) as image:
#                 if aspectRatio == "y":
#                     image.thumbnail((width, height), Image.Resampling.LANCZOS)
#                     image.save(cacheSavePath, format=requestedType)
#                 else:
#                     resizedImg = image.resize((width, height), Image.Resampling.LANCZOS)
#                     resizedImg.save(cacheSavePath, format=requestedType)

#                 # Return the new resized image
#                 return FileResponse(
#                     path=cacheSavePath,
#                     filename=f"{img.stem}.{requestedType}",
#                     media_type=f"image/{requestedType}"
#                 )

#         # Not a supported image, just return the full image
#         else:
#             return FileResponse(img, filename=f"{img.name}")
        

# @utils.fastAPI.get("/image/download")
# async def downloadImg(request:Request):
#     """ 
#     Returns a raw image 
    
#     Query Params:
#         f - The location of the file you want
#     """
#     query = request.query_params
#     reqFile = query.get("f") # f

#     # Query param are required
#     if not query or not reqFile:
#         raise HTTPException(status_code=404)
#     assert reqFile is not None
#     reqFile = unquote(reqFile)

#     img: Path = Path(str(ServerData["fileLocation"])) / reqFile

#     # Check if the location is good
#     if not img.exists():
#         raise HTTPException(status_code=404)
#     elif not img.is_file():
#         raise HTTPException(status_code=400, detail="File location is a directory")
    
#     else:
#         return FileResponse(path=img, filename=img.name)



# Main
if __name__ == "__main__":

    # Create Library folder
    ServerData.get_library_path().mkdir(exist_ok=True)

    # Create Cache folder
    ServerData.get_cache_path().mkdir(exist_ok=True)

    # Start FastAPI
    print(f"{Color.y}Starting FastAPI...\n{Color.re}")
    utils.startFastAPI(host=ServerData.getData("host"), port=ServerData.getData("port"), origins=ServerData.getData("CORS_origins"))
