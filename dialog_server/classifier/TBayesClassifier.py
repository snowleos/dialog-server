# vim: set fileencoding=utf-8
from __future__ import division
import sys
import os
import re
import subprocess
sys.path.append("../..")
from collections import defaultdict
from math import log

import dialog_server
from dialog_server.command_matcher.TCommandType import *
from dialog_server.command.TCommandCreator import *
from dialog_server.classifier.TBaseClassifier import *
from dialog_server.classifier.TBayesModel import *
from dialog_server.classifier.TBayesFeatureExtractor import *

class TBayesClassifier(TBaseClassifier):
    def __init__(self, confPath=""):
        TBaseClassifier.__init__(self, confPath)
        self.Model = None #TBayesModel()
        self.ModelType = TBayesModel
        self.FeatureExtractor = TBayesFeatureExtractor()

    def Classify(self, command, probCommandsDict):
        maxCl = ""
        maxClProb = -1
        for cl in self.Model.Classes.keys():
            sumClassFeatures = 0
            clProbDict = self.Model.FeatureProbs.get(cl, None)
            if clProbDict != None:
                for feat in command.Features:
                    featProb = clProbDict.get(feat, 10**(-7))
                    sumClassFeatures += -log(featProb)
            # make probabilities from sum logs
            # TODO: make recognition of words, most specific to chosen command
            if not self.Equals(sumClassFeatures, 0.0):
                sumClassFeatures = 1/sumClassFeatures
            probCommandsDict[cl] = TProbCommandProps(\
                    name=cl, prob=sumClassFeatures, wnum=[])
            if sumClassFeatures > maxClProb:
                maxClProb = sumClassFeatures
                maxCl = cl
        self.NormProbList(probCommandsDict)
        return maxCl

    """
    def Classify(self, command, probCommandsDict):
        minCl = ""
        minClProb = 100000000
        for cl in self.Model.Classes.keys():
            sumClassFeatures = 0
            clProbDict = self.Model.FeatureProbs.get(cl, None)
            if clProbDict != None:
                for feat in command.Features:
                    sumClassFeatures += -log(clProbDict.get(feat, 10**(-7)))
            probCommandsDict[cl] = sumClassFeatures
            if sumClassFeatures < minClProb:
                minClProb = sumClassFeatures
                minCl = cl
        return minCl
    """

    def StartLearn(self):
        self.Model = TBayesModel()
        self.Model.Modified = True

    def Learn(self, command):
        self.Model.Classes[command.CmdType] += 1
        self.Model.ClassSamplesCount[command.CmdType] += 1
        for feat in command.Features:
            self.Model.FeatureProbs[command.CmdType][feat] += 1

    def FinishLearn(self):
        for cl in self.Model.Classes:
            for feat in self.Model.FeatureProbs[cl]:
                self.Model.FeatureProbs[cl][feat] /= self.Model.ClassSamplesCount[cl]
            self.Model.Classes[cl] /= sum(self.Model.ClassSamplesCount.values())
        

    #def SaveModel(self): implemented in base class
    #def LoadModel(self): implemented in base class
