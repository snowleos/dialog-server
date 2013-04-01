# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
sys.path.append("..")
import common_lib.common_ops as common_ops
import dialog_server
from dialog_server.command_matcher.TCommandType import *
from dialog_server.command.TCommandCreator import *
from dialog_server.classifier.TBaseFeatureExtractor import *
from dialog_server.classifier.TBaseModel import *
from dialog_server.classifier.TModelIO import *
import common_lib.common_ops as common_ops

class TBaseClassifier:
    Epsilon = 0.00000000001
    def __init__(self, confPath=""):
        print >> sys.stderr , confPath 
        self.Conf = common_ops.ReadConfig(confPath)
        self.Model = None #TBaseModel()
        self.ModelType = TBaseModel # must be set at child class
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
        ModelIO = TModelIO()
        modelTableName = self.Conf.get("Model", "ModelTableName")
        ModelIO.Write(common_ops.GetProjectBaseDir() + \
                modelTableName, None, [self.Model])

    def LoadModel(self):
        ModelIO = TModelIO()
        modelTableName = self.Conf.get("Model", "ModelTableName")
        modelList = list()
        ModelIO.Read(common_ops.GetProjectBaseDir() + \
                modelTableName, None, self.ModelType, modelList)
        self.Model = modelList[-1]

    @classmethod
    def Equals(self, num1, num2):
        return abs(num1 -num2) < self.Epsilon

    @classmethod
    def NormProbList(self, probCommandsDict):
        probSum = 0.0
        for probCmd in probCommandsDict.values():
            probSum += probCmd.Prob
        if not self.Equals(probSum, 0.0):
            for probCmd in probCommandsDict.keys():
                probCommandsDict[probCmd].Prob = \
                        probCommandsDict[probCmd].Prob / probSum

