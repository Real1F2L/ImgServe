# v1.0.0
# Thank you for downloading ImgServe!
#
# ImgServe is a free and open source image serving API.
# Built for maximizing website load times and bandwidth.
# Serve images at the correct size in a modern format!
#
# Contributions and modding is allowed, under no circumstances should you sell ImgServe, modded or not.
#
import os, threading, time, subprocess
#
from utils import utils
from fastapi import Request, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse, StreamingResponse
from urllib.parse import unquote
from PIL import Image

# Middleware for logging
@utils.fastAPI.middleware("http")
async def middleware(request: Request, call_next):
    #* Print the request for debugging (format: "method :- IP -: /location ?query")
    _ip = (utils.getIP(request) + "-:").ljust(20)
    _method = (request.method.capitalize() + "]").ljust(10)
    print(f"{utils.color.g}[{_method}{utils.color.re} :-{_ip}    {utils.color.bold}{request.url.path}{utils.color.re}" + (unquote(" ?" + str(request.query_params)) if str(request.query_params) else ""))

    #* Log the request
    utils._RequestLogger.info(f"New {request.method} request from {utils.getIP(request)} - {request.url.path}" + (unquote(" ?" + str(request.query_params)) if str(request.query_params) else ""))

    #* return original request
    return await call_next(request)

# Search files, search the specified location for files/folders
@utils.fastAPI.get("/searchFiles")
async def searchFiles(request:Request):
    """
    Searches a folder for files/folders between a range
    Returns:
        JSON formatted response
    """
    try:
        requestQuery = request.query_params
        if (not requestQuery): raise HTTPException(status_code=400, detail="Missing query")

        _folder = os.path.join(utils._root, unquote(requestQuery.get("folder", ""))) #? The location of the folder to search
        end = int(unquote(requestQuery.get("end", "6"))) #? The ending index
        start = int(unquote(requestQuery.get("start", "0"))) #? The starting index

        # checks
        _exists = os.path.exists(_folder)
        _isFile = os.path.isfile(_folder)

        #! reject access to other folders
        if not _folder.startswith(utils._root):
            raise HTTPException(status_code=400, detail="Access to this folder is denied.")

        if _exists and not _isFile:
            _result = [] #? the JSON to be returned
            _folderDescription = None

            # slice the files in the folder
            _files_to_return = os.listdir(_folder)[start:end]

            # loop through each file inside the index
            for filename in _files_to_return:
                _fileDict = {} #? the JSON that will be added to the _result

                # get the file path and extension
                filePath = os.path.join(_folder, filename).replace("\\\\", "\\")
                fileExtension = os.path.splitext(filePath)[-1]

                accessDenied = False

                if any(name.lower() in filePath.lower() for name in utils._dontShareNames):
                    continue

                # check if the file exists
                if not os.path.exists(filePath):
                    continue

                # ignore the .ShareGegeha description file
                if filename == ".ShareGegeha":
                    continue
                
                # record name, path, type, extension, and size
                _fileDict["Name"] = filename
                _fileDict["Path"] = filePath.replace(utils._root, "")
                
                # check if the file is a folder
                if os.path.isdir(filePath):
                    _fileDict["Type"] = "Folder" 
                    _fileDict["Extension"] = "Folder"
                    _fileDict["SizeMB"] = "This feature is disabled for folders due to long calculation times" # round(utils.getDirSize(filePath) / (1024 ** 2), 2)

                # check if the file is a file
                elif os.path.isfile(filePath):
                    _fileDict["Type"] = "File"
                    _fileDict["Extension"] = fileExtension
                    _fileDict["SizeKB"] = round(os.path.getsize(filePath) / (1024), 2) #? bytes / 1024 = KB, rounded to 2 decimals
                
                _result.append(_fileDict) #? add JSON to the _result
            
            # Look for the .ShareGegeha description file
            shareGegehaLoc = _folder + ".ShareGegeha"
            if os.path.exists(shareGegehaLoc):
                with open(shareGegehaLoc, 'r') as r:
                    _folderDescription = r.read()
                    r.close()

            # return the JSON
            return {"files" : _result, "dirInfo" : _folderDescription}
        
        #! requested folder does not exist
        else:
            raise HTTPException(status_code=400, detail="Folder does not exist or is a file")
    except Exception as e:
        print(f"{utils.color.r}[searchFiles] Unexpected exception: {e}.{utils.color.re}")
        utils._RequestLogger.error(f"Unexpected exception: {e}. Traceback will be logged in ErrorLogs.log")
        utils._ErrorLogger.error(f"Unexpected exception: {e}. Traceback will be logged in ErrorLogs.log")
        raise HTTPException(status_code=500, detail="Internal server error")
    
# Get file contents, return the inside of a text file
@utils.fastAPI.get("/get-file-contents")
async def getFileContents(request:Request):
    """
    Reads the contents of a file and returns it
    Returns:
        Raw text response
    """
    try:
        requestQuery = request.query_params
        if (not requestQuery): raise HTTPException(status_code=400, detail="Missing query")

        _file = os.path.join(utils._root, requestQuery.get("file", "")) #? The location of the file to read
        
        for name in utils._dontShareNames:
            if name in _file:
                raise HTTPException(status_code=400, detail="Access to this file is denied.")

        # checks
        _exists = os.path.exists(_file)
        _isFile = os.path.isfile(_file)

        #! reject access to other folders
        if not _file.startswith(utils._root):
            raise HTTPException(status_code=400, detail="Access to this folder is denied.")


        if _exists and _isFile:
            # open the file
            with open(_file, 'r') as f:
                try:
                    return PlainTextResponse(content=f.read())
                except Exception as e:
                    print(f"{utils.color.r}[get-file-contents] Failed to read file {_file}: {e}{utils.color.re}")
                    utils._RequestLogger.error(f"Failed to read file {_file}: {e}. Traceback will be logged in ErrorLogs.log")
                    utils._ErrorLogger.exception(f"Unexpected exception while reading file: {e}.")
                    return HTTPException(status_code=500, detail="Internal server error")
                
        else:
            raise HTTPException(status_code=400, detail="File does not exist or is a folder")
    except Exception as e:
        print(f"{utils.color.r}[get-file-contents] Unexpected exception: {e}.{utils.color.re}")
        utils._RequestLogger.error(f"Unexpected exception: {e}. Traceback will be logged in ErrorLogs.log")
        utils._ErrorLogger.exception(f"Unexpected exception: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Download, return a file response for downloading
@utils.fastAPI.get("/download")
async def downloadFile(request:Request):
    """
    Returns an entire file, and supports resizing for images
    Returns:
        File response
    """
    try:

        requestQuery = request.query_params
        if (not requestQuery): raise HTTPException(status_code=400, detail="Missing query")

        _file = os.path.join(utils._root, unquote(requestQuery.get("file", ""))) #? The location of the file to return
        _imgSize = int(unquote(requestQuery.get("size", 64))) #? the image size, default 64
        _extensionWithoutDot = os.path.splitext(_file)[1].split(".")[1].lower() #? the file extension
        _basename = os.path.basename(_file) #? the entire name of the file (including extension)
        _CacheSavePath = os.path.join(utils._CacheLocation, _basename + "_resized" + unquote(requestQuery.get("size", "64")) + ".webp") #? where the image will be stored in the cache

        for name in utils._dontShareNames:
            if name in _file:
                raise HTTPException(status_code=400, detail="Access to this file is denied.")

        # checks
        _exists = os.path.exists(_file)
        _isFile = os.path.isfile(_file)

        #! reject access to other folders
        if not _file.startswith(utils._root):
            raise HTTPException(status_code=400, detail="Access to this folder is denied.")

        if not _exists:
            raise HTTPException(status_code=404, detail="File does not exist or is a folder")
        elif not _isFile:
            raise HTTPException(status_code=400, detail="Path is a folder")
        
        else:
            img_files = ["png", "jpg", "jpeg", "webp", "svg", "heic", "pdn"]

            # check if the file is an image
            if (_extensionWithoutDot in img_files):
                # check if the image is already in cache
                if (os.path.exists(_CacheSavePath)):
                    return FileResponse(_CacheSavePath, filename=_basename, media_type="image/webp", status_code=200)

                # open the image with PIL
                with Image.open(_file) as img:
                    # resize the image to the size specified
                    img.thumbnail((_imgSize, _imgSize), Image.Resampling.LANCZOS)
                    img.save(_CacheSavePath, "webp") #? save image to cache

                    # return the new resized image
                    return FileResponse(_CacheSavePath, filename=os.path.basename(_CacheSavePath), media_type="image/webp", status_code=200)

            # not an image, just return the file
            else:
                return FileResponse(_file, filename=_basename, status_code=200)
            
    except Exception as e:
        print(f"{utils.color.r}[download] Unexpected exception: {e}.{utils.color.re}")
        utils._RequestLogger.error(f"Unexpected exception: {e}. Traceback will be logged in ErrorLogs.log")
        utils._ErrorLogger.exception(f"Unexpected exception: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Display video, return a video in a lower resoluton and bitrate
@utils.fastAPI.get("/display-video")
async def display_video(request: Request):
    """
    Resizes and lowers bitrate of a video
    Returns:
        Streaming response
    """
    try:
        requestQuery = request.query_params
        if (not requestQuery): raise HTTPException(status_code=400, detail="Missing query")

        _file = os.path.join(utils._root, requestQuery.get("file", ""))

        for name in utils._dontShareNames:
            if name in _file:
                raise HTTPException(status_code=400, detail="Access to this file is denied.")

        _basename = os.path.basename(_file) #? the entire name of the file (including extension)
        _CacheSavePath = os.path.join(utils._CacheLocation, _basename + f"_resized{utils._vidScaleX}X{utils._vidScaleY}_bitrate{utils._vidBitrate}" + ".mp4") #? where the image will be stored in the cache

        # checks
        _exists = os.path.exists(_file)
        _isFile = os.path.isfile(_file)

        #! reject access to other folders
        if not _file.startswith(utils._root):
            raise HTTPException(status_code=400, detail="Access to this folder is denied.")

        if _exists and _isFile:
            # check if the video is already in cache
            if (os.path.exists(_CacheSavePath)):
                return StreamingResponse(
                    utils.video_streamer(_CacheSavePath), 
                    media_type="video/mp4"
                )
            
            #* video is not in cache
            else:
                # if resizing is enabled
                if utils._doVideoResizing:
                    # resize using ffmpeg command
                    subprocess.run(f'ffmpeg -i "{_file}" -vf "scale={utils._vidScaleX}:{utils._vidScaleY}" "{_CacheSavePath}"', check=True)
                    return StreamingResponse(
                        utils.video_streamer(_CacheSavePath), 
                        media_type="video/mp4"
                    )
                
                # video resizing is disabled
                else:
                    # return the original video
                    return StreamingResponse(
                        utils.video_streamer(_file), 
                        media_type="video/mp4"
                    )
        elif not _isFile or not _exists:
            raise HTTPException(status_code=400, detail="File does not exist or is a folder")
        
    except Exception as e:
        utils._RequestLogger.error(f"Unexpected exception displaying video: {e}. Traceback will be logged in ErrorLogs.log")
        utils._ErrorLogger.exception(f"Unexpected exception: {e}")
        print(f"{utils.color.r}[display-video] Unexpected exception: {e}{utils.color.re}")
        raise HTTPException(status_code=500, detail="Internal server error")

def deleteCacheThread():
    vidCount:int = 0
    while True:

        for file in os.listdir(utils._CacheLocation):
            _file = os.path.join(utils._CacheLocation, file) #? the path to the file
            _extension = os.path.splitext(file)[1] #? the extension of the file (not including the dot)
            print(_extension)
            
            if _extension in utils._videoTypes:
                if utils._clearVideoCache:
                    os.remove(_file)
                else:
                    vidCount += 1
                    continue
            else:
                os.remove(_file)

        print(f"\n{utils.color.g}[deleteCacheThread]{utils.color.re} Cache successfully cleared at {utils.getCurrentTime()} with {vidCount} video{"s" if vidCount > 1 or vidCount == 0 else ""} kept in cache.\n")
        time.sleep(utils._clearCacheHrs * 3600) #? once every hour
        vidCount = 0

if __name__ == "__main__":

    #* Start API

    utils.loadConfig()

    # utils._Platform = "Linux"
    if utils._Platform == "Darwin":
        print(f"\n{utils.color.r}[__main__] ImgServe is not supported on macOS.{utils.color.re}\nWhile not reccomended you can remove this retriction by editing the file __init__.py, and uncomment line 315.")

    # start delete cache thread
    if utils._DoClearCache:
        cacheThread = threading.Thread(target=deleteCacheThread)
        cacheThread.start()
    else:
        print(f"\n[__main__] DoClearCache is set to False. Image and video cache will be stored forever.\n")

    print(f"\n\n[__main__]{utils.color.g} Starting API...{utils.color.re}\n\n")
    utils.startFastapi()