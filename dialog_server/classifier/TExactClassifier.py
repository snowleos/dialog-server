# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
sys.path.append("../..")
import dialog_server
from dialog_server.command_matcher.TCommandType import *
from dialog_server.command.TCommandCreator import *
from dialog_server.classifier.TBaseClassifier import *

class TExactClassifier(TBaseClassifier):
    def __init__(self):
        
        self.Model = {
                u"википедия": "Wiki",
                u"погода": "Weather",
                u"новости": "News",
                u"поиск": "Search"
                };

    def Classify(self, command, probCommandsDict):
        print " ".join(command.LexemsList).encode("utf-8")
        for wnum in xrange(len(command.LexemsList)):
            if command.LexemsList[wnum] in self.Model:
                _name=self.Model[command.LexemsList[wnum]]
                probCommandsDict[_name] = TProbCommandProps(\
                        name=_name, \
                        prob=1.0, wnum=[wnum])

        self.NormProbList(probCommandsDict)

