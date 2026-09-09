# File structure requesting routes

import os
#
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from Scripts.ServerData import ServerData
from Scripts import utils
from fastapi import Query
from PIL import Image


@utils.fastAPI.get("/api/v1/folder-search")
def file_search(
    f: str = Query("/", title="The location of the directory you want"),
):
    """Returns the files and dirs inside a Library folder"""
    path = ServerData.get_library_path() / f

    # Prevent directory traversal
    if not path.is_relative_to(ServerData.get_library_path()):
        raise HTTPException(status_code=403, detail="Invalid path")

    # Reject non-dir paths
    if not path.is_dir():
        raise HTTPException(status_code=400, detail="Path does not exist or is not a directory")

    dirs = []
    files = []

    for entry in os.scandir(path):

        # Dirs
        if entry.is_dir():
            dirs.append({
                "path": f,
                "name": entry.name,
                "size_bytes": entry.stat().st_size,
                "items_inside": len(list(os.scandir(entry.path))),
            })

        # Files
        elif entry.is_file():
            extension = entry.name.split(".")[-1]
            name = entry.name.replace("." + extension, "")
            is_resizable_image = extension in utils.supported_resize_image_extensions
            is_image = extension in utils.supported_download_image_extensions
            is_video = extension in utils.supported_video_extentions

            files.append({
                "path": f,
                "name": name,
                "extension": extension,
                "is_image": is_image,
                "is_image": is_image,
                "is_resizable_image": is_resizable_image,
                "is_video": is_video,
                "last_modified": entry.stat().st_mtime,
                "size_bytes": entry.stat().st_size,
            })

    return JSONResponse({
        "dirs": dirs,
        "files": files,
    })

@utils.fastAPI.get("/api/v1/file-search")
def file_search(
    f: str = Query(..., title="The location of the file you want"),
):
    """Returns data on a file in the library"""
    path = ServerData.get_library_path() / f
    
    # Prevent directory traversal
    if not path.is_relative_to(ServerData.get_library_path()):
        raise HTTPException(status_code=403, detail="Invalid path")

    # Reject non-dir paths
    if not path.is_file():
        raise HTTPException(status_code=400, detail="Path does not exist or is not a file")

    extension = path.name.split(".")[-1]
    name = path.name.replace("." + extension, "")
    is_resizable_image = extension in utils.supported_resize_image_extensions
    is_image = extension in utils.supported_download_image_extensions
    is_video = extension in utils.supported_video_extentions

    # Get image size data
    if is_resizable_image:
        try:
            with Image.open(path) as img:
                width, height = img.size
        except Exception as e:
            width, height = None, None
    else:
        width, height = None, None

    return JSONResponse({
        "path": f,
        "name": name,
        "extension": extension,
        "is_image": is_image,
        "is_resizable_image": is_resizable_image,
        "width": width,
        "height": height,
        "is_video": is_video,
        "last_modified": path.stat().st_mtime,
        "size_bytes": path.stat().st_size,
    })