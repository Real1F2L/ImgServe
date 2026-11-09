import json, yaml
#
from typing import Any
from pathlib import Path
from Scripts import utils
from Scripts.utils import Color
from fastapi import HTTPException

# Default config values
_defaults: dict = {
    "server_url": "missing_server_url_value",

    "host": "0.0.0.0",
    "port": 8080,
    "CORS_origins": [
        "http://localhost",
        "http://127.0.0.1"
    ],

    "image_location": "./Library/",
    "cache_location": "./Cache/",

    "cache_persists": False,
    "keep_cache_for_hours": 24,
    "purge_cache_time": "00:00:00",

    "update_statistics_every_minutes": 10,
}

class ServerData:
    """ A class that grabs and stores data on the enitre server process"""
    _data: dict = {}
    _already_started = False

    @staticmethod
    def start():
        # Check if already started
        if ServerData._already_started:
            return
        ServerData._already_started = True

        # Read Options.yml
        ServerData._data = ServerData.readOptionsFile()

    @staticmethod
    def readOptionsFile() -> dict:
        """Checks for Options.yml, creates it if it doesnt exists, and returns the data inside."""
        print(f"[ServerData] Attempting to read Options.yml...")
        path = utils.WORKINGDIR / "Options.yml"

        try:
            # Check if the file exists
            if not path.is_file():

                # Make the file and fill with defaults
                print(f"{Color.r}Options.yml not Found, creating file with default values.{Color.re}")
                with open(utils.options_location, "w") as f:
                    yaml.dump(_defaults, f, default_flow_style=False)
                    f.close()

            # Open the config file
            #? By now it should exist
            with open(path, "r") as f:
                data:dict = yaml.load(f, Loader=yaml.FullLoader)

                # Check if any keys are missing, load defaulyt values
                _missingKeys:list = []
                for key in _defaults.keys():
                    if key not in data.keys():
                        _missingKeys.append(key)

                # Warn if any keys are missing
                if len(_missingKeys) > 0:
                    print(f"{Color.r}Warning: Atleast 1 value was missing from Options.yml{Color.re}\nMissing value(s): {', '.join(_missingKeys)}\nDefault Values Will Be Used!")
                else:
                    print(f"{Color.g}Options.yml read successfully, missing 0 values.{Color.re}")

                # Done
                f.close()
                return data

        except Exception as e:
            print(f"{Color.r}Error Reading Options.yml: {e}{Color.re}")
            return {}

    
    @classmethod
    def getData(cls, key : str) -> Any:
        try:
            # Return the data
            return cls._data[key]

        except KeyError:
            print(f"{Color.r}Attempted to access value from Options.yml that doesn't exist! Value: {key}{Color.re}")

            # Attempt to return default
            if key in _defaults.keys():
                print(f"{Color.y}Found a default value for {key}.{Color.re}")
                return _defaults[key]

    @classmethod
    def get_library_path(cls) -> Path:
        """Returns resolved path to library folder"""
        return Path(str(cls.getData("image_location"))).resolve()

    @classmethod
    def get_cache_path(cls) -> Path:
        """Returns resolved path to cache folder"""
        return Path(str(cls.getData("cache_location"))).resolve()

ServerData.start()

def resolve_library_path(requested_path: str) -> Path:
    root = ServerData.get_library_path()

    # Treat "/" as the root of the library folder
    try:
        library_path = (root / requested_path.lstrip("/")).resolve()
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail="Invalid path") from exc

    # Prevent directory traversal
    if not library_path.is_relative_to(root):
        raise HTTPException(status_code=403, detail="Invalid path")

    # Return the path inside the library folder
    return library_path