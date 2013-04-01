import os
import ConfigParser

def ReadConfig(confPath):
    Conf = None
    if confPath != "":
        Conf = ConfigParser.ConfigParser()
        Conf.read(confPath)
    return Conf

def GetProjectBaseDir():
    # returns dir relate to class TDialogServer
    return os.getcwd() + "/../"

