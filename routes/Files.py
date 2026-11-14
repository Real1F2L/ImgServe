# File structure requesting routes

import os
#
from pathlib import Path
from fastapi import HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from Scripts.ServerData import ServerData, resolve_library_path
from Scripts import utils
from fastapi import Query
from PIL import Image


def get_file_name_and_extension(path: Path) -> tuple[str, str]:
    extension = path.suffix.lstrip(".")
    name = path.stem if extension else path.name
    return name, extension


@utils.fastAPI.get("/api/v1/file-download")
@utils.limiter.limit("1200/minute")
def download_file(
    request: Request,
    f: str = Query(..., title="The location of the file you want"),
):
    """Download a regular file from the library

    This is strictly for files, not images!
    """

    path = resolve_library_path(f)
    if not path.is_file():
        raise HTTPException(status_code=404, detail="File could not be found")
    if path.suffix.lstrip(".").lower() in utils.supported_download_image_extensions:
        raise HTTPException(
            status_code=400,
            detail="Image files must be downloaded through the image download endpoint",
        )

    return FileResponse(path, filename=path.name)


@utils.fastAPI.get("/api/v1/folder-search")
@utils.limiter.limit("60/minute")
def file_search(
    request: Request,
    f: str = Query("/", title="The location of the directory you want"),
):
    """Returns the files and dirs inside a Library folder"""

    dir = resolve_library_path(f)

    # Exists and is a directory
    if not dir.is_dir():
        raise HTTPException(status_code=400, detail="Path does not exist or is not a directory")

    dirs = []
    files = []

    for entry in os.scandir(dir):

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
            name, extension = get_file_name_and_extension(Path(entry.name))
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
@utils.limiter.limit("60/minute")
def file_search(
    request: Request,
    f: str = Query(..., title="The location of the file you want"),
):
    """Returns data on a file in the library"""

    path = resolve_library_path(f)

    # Exists
    if not path.is_file():
        raise HTTPException(status_code=400, detail="Path does not exist or is not a file")

    name, extension = get_file_name_and_extension(path)
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