class Color:
    def __new__(cls, *args, **kwargs):
        raise TypeError("Colors class should not be instanced!")

    # Font colors
    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    blue = '\033[94m'
    magenta = '\033[95m'
    cyan = '\033[96m'
    white = '\033[97m'

    # Text changes
    bold = '\033[1m'
    underline = '\033[4m'

    # Background colors
    redBg = '\033[41m'
    greenBg = '\033[42m'
    yellowBg = '\033[43m'
    blueBg = '\033[44m'
    magentaBg = '\033[45m'
    cyanBg = '\033[46m'
    whiteBg = '\033[47m'

    # reset
    reset = '\033[0m'

# Do something when this file is __main__
if __name__ == "__main__":
    print(f"{Color.red}This file literally does nothing. Run main.py instead.{Color.reset}")
    exit(0)