# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
sys.path.append("../..")
import dialog_server
from dialog_server.classifier.TModelIO import *

class TBaseModel:
    def __init__(self):
       self.ModelId = TModelIO.GetNewModelId()
       self.ContextId = "common"
       self.Modified = False
       self.BinData = ""

    def Read(self, line):
        self.BinData = line
        """read data from line. parse fields to model objects"""

    def Write(self):
        return self.BinData
