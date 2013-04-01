# vim: set fileencoding=utf-8
import sys
import os
import re
import json
import subprocess
sys.path.append("../..")
from collections import defaultdict
import dialog_server
from dialog_server.classifier.TBaseModel import *

class TBayesModel(TBaseModel):
    def __init__(self):
        TBaseModel.__init__(self)
        self.Classes = defaultdict(lambda:0)
        self.FeatureProbs = defaultdict(lambda:defaultdict(lambda:0))
        self.ClassSamplesCount = defaultdict(lambda:0)

    def Read(self, line):
        TBaseModel.Read(self, line)
        jsonObj = json.loads(self.BinData)
        self.Classes = jsonObj["Classes"]
        self.FeatureProbs = jsonObj["FeatureProbs"]
        self.ClassSamplesCount = jsonObj["ClassSamplesCount"]
        #print self.FeatureProbs

    # returns JSON string
    def Write(self):
        self.BinData = ""
        self.BinData = json.dumps({
            "Classes": self.Classes,
            "FeatureProbs": self.FeatureProbs,
            "ClassSamplesCount": self.ClassSamplesCount
            })
        #print self.BinData
        return self.BinData
