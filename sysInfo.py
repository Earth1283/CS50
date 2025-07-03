from logger import fileLog as fl
import platform
def getOS():
    fl.log("Getting OS info from API call")
    return platform.system()
def getPythonVersion():
    fl.log("Getting python version from API call")
    return platform.python_version()
def getMachine():
    fl.log("Getting machine type from API call")
    return platform.machine()

def getProcessor():
    fl.log("Getting processor info from API call")
    return platform.processor()

def getPlatform():
    fl.log("Getting platform info from API call")
    return platform.platform()