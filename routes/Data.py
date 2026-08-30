# Image data requesting routes
#
from Scripts import utils
from fastapi import Query

@utils.fastAPI.get("/api/v1/data/metadata")
def get_cache_data(
    f: str = Query(..., title="The location of the file you want"),
):
    """Gets info on a file inside the library"""
    ...

@utils.fastAPI.get("/api/v1/data/caches")
def get_cache_data(
    f: str = Query(..., title="The location of the file you want"),
):
    """Get cache info about an image in the library such as number of caches, sizes, etc."""
    ...