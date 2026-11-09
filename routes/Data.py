from Scripts import utils
from fastapi import Query, Request
from Scripts.LibraryStats import LibraryStats

@utils.fastAPI.get("/api/v1/data/library-file-counts")
@utils.limiter.limit("120/minute")
def get_file_counts(request: Request):
    """Returns the total number of files, dirs, and images in the entire library"""
    return {
        "success": True,
        "stats": {
            "dirs": LibraryStats.getDirCount(),
            "files": LibraryStats.getFileCount(),
            "images": LibraryStats.getImgCount(),
            "svgs": LibraryStats.getSvgCount(),
        },
        "last_updated": LibraryStats.last_updated.isoformat(),
    }