# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
sys.path.append("../..")
import dialog_server
from dialog_server.command_matcher.TCommandType import *
from dialog_server.command.TCommandCreator import *
from dialog_server.classifier.TBaseFeatureExtractor import *
from dialog_server.classifier.TBaseModel import *

class TBaseClassifier:
    def __init__(self, confPath=""):
        self.Conf = ConfigParser.ConfigParser()
        self.Conf.read(confPath)
        self.Model = None #TBaseModel()
        self.FeatureExtractor = None #TBaseFeatureExtractor()
        
    def __call__(self, command, probCommandsDict):
        self.Classify(command, probCommandsDict)

    def Classify(self, command, probCommandsDict):
        print >> sys.stderr, "Classify() not implemented"
    def StartLearn(self):
        print >> sys.stderr, "StartLearn() not implemented"
    def Learn(self, command):
        print >> sys.stderr, "LearnCommand() not implemented"
    def FinishLearn(self):
        print >> sys.stderr, "FinishLearn() not implemented"
    def SaveModel(self):
        print >> sys.stderr, "SaveModel() not implemented"
    def LoadModel(self):
        print >> sys.stderr, "LoadModel() not implemented"

