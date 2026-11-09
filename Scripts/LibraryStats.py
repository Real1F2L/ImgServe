import os
#
from datetime import datetime, timedelta
from Scripts.ServerData import ServerData
from Scripts import utils

class LibraryStats:
    _dirs = 0
    _files = 0
    _svgs = 0 # SVG files
    _images = 0 # All images that can be resized (not SVG)

    last_updated = datetime.now() - timedelta(days=365) # Set to a year ago so it updates on first run
    update_every_mins = ServerData.getData("update_statistics_every_minutes")

    @classmethod
    def update(cls):
        """ Updates the library stats """
        # Check if its time to update
        if cls.update_every_mins == -1:
            return

        if cls.is_time_to_update():

            #? Avoid race conditions
            new_dirs = 0
            new_files = 0
            new_images = 0
            new_svgs = 0

            # Get new values
            for root, dirs, files in os.walk(ServerData.get_library_path()):
                new_dirs += len(dirs)
                new_images += len([f for f in files if f.split(".")[-1].lower() in utils.supported_resize_image_extensions])
                new_svgs += len([f for f in files if f.split(".")[-1].lower() == "svg"])
                new_files += len(files)

            # Swap values
            LibraryStats._dirs = new_dirs
            LibraryStats._files = new_files - new_svgs - new_images
            LibraryStats._images = new_images
            LibraryStats._svgs = new_svgs

            LibraryStats.last_updated = datetime.now()
            print(f"[LibraryStats] Updated library stats: {LibraryStats._dirs} dirs, {LibraryStats._files} files, {LibraryStats._images} images.")

    @classmethod
    def is_time_to_update(cls) -> bool:
        """ Returns True if it is time to update the library stats """
        return (datetime.now() - cls.last_updated).total_seconds() > cls.update_every_mins * 60


    #* Getters

    @classmethod
    def getDirCount(cls) -> int:
        """ Returns the total number of directories in the entire library"""
        if cls.is_time_to_update():
            cls.update()
        return cls._dirs

    @classmethod
    def getFileCount(cls) -> int:
        """ Returns the total number of files in the entire library"""
        if cls.is_time_to_update():
            cls.update()
        return cls._files

    @classmethod
    def getImgCount(cls) -> int:
        """ Returns the total number of images in the entire library"""
        if cls.is_time_to_update():
            cls.update()
        return cls._images

    @classmethod
    def getSvgCount(cls) -> int:
        """ Returns the total number of SVGs in the entire library"""
        if cls.is_time_to_update():
            cls.update()
        return cls._svgs

LibraryStats.update()