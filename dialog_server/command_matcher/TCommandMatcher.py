# vim: set fileencoding=utf-8
import sys
import os
import re
import copy
import subprocess
sys.path.append("../..")
import dialog_server
from dialog_server.command_matcher.TCommandType import *
from dialog_server.command_matcher.TBayesClassifier import *
from dialog_server.command_matcher.TExactClassifier import *

class TCommandMatcher:
    def __init__(self):
        """put fields here"""

    def FindMostProbCommands(self, probCommandsList, commandsToExecList):
        if len(probCommandsList) != 0:
            mostProbCmd = probCommandsList[0]
            maxProb = probCommandsList[0].Prob
            for i in xrange(1, len(probCommandsList)):
                if probCommandsList[i].Prob > maxProb:
                    maxProb = probCommandsList[i].Prob
                    mostProbCmd = probCommandsList[i]
            commandsToExecList.append(copy.copy(mostProbCmd))
            print commandsToExecList[0].CmdType.Name

    def __call__(self, command, commandsToExecList):
        # got command with splitted words
        probCommandsList = list()
        cmdClassifier = TExactClassifier()
        cmdClassifier(command, probCommandsList)
        self.FindMostProbCommands(probCommandsList, commandsToExecList)
        print commandsToExecList[0].CmdType.Name
