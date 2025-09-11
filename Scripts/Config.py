import json
#
from pathlib import Path
from typing import Any, TypeVar

# Do something when this file is __main__
if __name__ == "__main__":
    from Color import Color
    print(f"{Color.red}This file literally does nothing. Run main.py instead.{Color.reset}")
    exit(0)
from Scripts.Color import Color
from Scripts import utils


class Config:
    """ Class for storing ImgServe config data """
    _data: dict
    _ConfigPath: Path

    # A bunch of default values that are REQUIRED in the config file
    _requiredDict: dict[str, Any] = {
        "Server" : "ImgServe",
        "ServerURL" : "example.com",
        "ServerVersion" : "v1.1.0",

        # Locations
        "fileLocation" : "./Files",
        "cacheLocation" : "./Cache",
        "logLocation" : "./Logs",

        # Cache clearing
        "doClearCache" : True,
        "clearCacheEveryHours" : 24,

        "ignoreFiles" : [
            "Dockerfile",
            ".gitignore",
            ".venv",
            ".pyCache",
            "__pycache__",
            ".git"
        ]
    }

    # Constructor
    def __init__(self, path: Path):
        """ 
        An instance is made to load from the config file, the class itself is used for accessing data 
        
        Discard this instance after creation
        """
        Config._data = self._load_config(path)

    @staticmethod
    def _load_config(path: Path) -> dict:
        """ Private method for loading config data from disk """

        # Check if the file exists
        if not path.is_file():
            raise FileNotFoundError(f"{Color.red}Fatal error: config file does not exist at {path}{Color.reset}")
        
        print(f"\n{Color.yellow}Loading config...{Color.reset}")
        
        # Load json data from config
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            f.close()

        Config._validate(data)
        Config._ConfigPath = path
        print(f"{Color.green}Config loaded successfuly!{Color.reset}")
        return data
    
    @staticmethod
    def _validate(data: dict) -> None:
        """ Simple check that ensures all required keys are in the config """
        for key in Config._requiredDict.keys():
            if not key in data:
                raise ValueError(f"{Color.red}Fatal error: missing required key in config ({key}){Color.reset}")
    
    @classmethod
    def get(cls, key: str, default=None) -> Any:
        """ 
        Get data from the config file
        
        Args:
            key - The key of the value you are looking for
            default - What will be returned if the data is not found

        The key should always be found though
        """
        return cls._data.get(key, default)
    
    @classmethod
    def __class_getitem__(cls, key: str) -> str:
        """ 
        Grab data using this class as a dictionary

        Use .get() to avoid possible Nones, or cast to a type

        For example:
            Config["fileLocation"]
        """
        try:
            return str(cls._data[key])
        except KeyError as e:
            print(f"{Color.red}KeyError getting config key {key}")
            raise e

# Automagically create a Config instance to load config file
config: Config = Config(utils.configPath)
del config

