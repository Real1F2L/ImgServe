import logging
#
from pathlib import Path
from typing import Any

# Do something when this file is __main__
if __name__ == "__main__":
    from Color import Color
    print(f"{Color.red}This file literally does nothing. Run main.py instead.{Color.reset}")
    exit(0)
from Scripts.Color import Color
from Scripts.Config import Config

class Logs:
    _logFormatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    _loggers: dict[str, logging.Logger] = {}
    _logLocation: Path
    _initalized:bool = False # Prevent multiple instances

    # Constructor
    def __init__(self, loggers: dict[str, str]):
        """ 
        An instance is made to create the loggers, the class itself is used for accessing data

        Discard this instance after creation 

        Takes a Dict of logger names and log levels
        (Ex. {"ErrorLogger" : "ERROR", "FileLogger : INFO"})
        """

        if self._initalized:
            print(f"{Color.yellow}Logs have already been initialized, do not instance more than once.{Color.reset}")

        print(f"\n{Color.yellow}Loading Logs...{Color.reset}")

        # Set logLocation in constructor so it doesnt initialize before Config does
        Logs._logLocation = Path(Config["logLocation"])

        # Make the logs folder
        Logs._logLocation.mkdir(parents=True, exist_ok=True)

        # Setup loggers
        for logName, logLevel in loggers.items():
            # Create the logger
            logger: logging.Logger = logging.getLogger(logName)
            Logs._loggers[logName] = logger

            # Create log handler
            logHandler = logging.FileHandler(Logs._logLocation / f"{logName}.log")
            logHandler.setFormatter(Logs._logFormatter)

            # Add handler to logger
            logger.addHandler(logHandler)

            # Set log level
            logger.setLevel(getattr(logging, logLevel.upper()))

        self._initalized = True
        print(f"{Color.green}Logs loaded successfully!{Color.reset}")

    # Quick loggers that are expected to exist
    @staticmethod
    def requestLogger() -> logging.Logger:
        return Logs.getLogger("RequestLogger")
    @staticmethod
    def errorLogger() -> logging.Logger:
        return Logs.getLogger("ErrorLogger")
    
    @classmethod
    def getLogger(cls, logger: str, default: Any=None) -> logging.Logger:
        return cls._loggers.get(logger, default)
    
    @classmethod
    def __class_getitem__(cls, logger: str) -> logging.Logger:
        try:
            return cls._loggers[logger]
        except KeyError as e:
            raise KeyError(f"{Color.red}Fatal error: logger {logger} does not exist{Color.reset}")
        

# Automagically create a Logs instance to load loggers
loggers: dict = {"RequestLogger" : "INFO", "ErrorLogger" : "ERROR", "CacheLogger" : "INFO", "TestLogger" : "INFO"}
logs: Logs = Logs(loggers)
del logs