from logger import fileLog as fl, LogLevel
import platform
def getOS():
    fl.logger(LogLevel.INFO, "Getting OS info from API call")
    return platform.system()
def getPythonVersion():
    fl.logger(LogLevel.INFO, "Getting Python Version info from API call")
    return platform.python_version()
def getMachine():
    fl.logger(LogLevel.INFO, "Getting machine info from API call")
    return platform.machine()

def getProcessor():
    fl.logger(LogLevel.INFO, "Getting processor info from API call")
    return platform.processor()

def getPlatform():
    fl.logger(LogLevel.INFO, "Getting general platform info from API call")
    return platform.platform()