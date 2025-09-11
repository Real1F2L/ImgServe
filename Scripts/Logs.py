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
        Logs._logLocation = Path(str(Config["logLocation"]))

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
        """ Get the Request Logger without possible None type or error (Since it will always exist) """
        reqLogger = Logs.getLogger("RequestLogger")

        assert reqLogger is not None
        return reqLogger
    @staticmethod
    def errorLogger() -> logging.Logger:
        """ Get the Error Logger without possible None type or error (Since it will always exist) """
        errLogger = Logs.getLogger("ErrorLogger")
        assert errLogger is not None
        return errLogger
    
    @classmethod
    def getLogger(cls, logger: str, default: Any=None) -> logging.Logger:
        foundLogger = cls._loggers.get(logger, default)

        if not foundLogger:
            raise KeyError(f"Logger {logger} does not exist")
        else:
            return foundLogger

# Automagically create a Logs instance to load loggers
loggers: dict = {"RequestLogger" : "INFO", "ErrorLogger" : "ERROR", "CacheLogger" : "INFO", "TestLogger" : "INFO"}
logs: Logs = Logs(loggers)
del logs