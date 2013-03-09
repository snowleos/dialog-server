# vim: set fileencoding=utf-8
import sys
import os
import re
import copy
import subprocess
sys.path.append("../..")
import dialog_server
from dialog_server.command_matcher.TCommandType import *

class TBayesClassifier:
    Epsilon = 0.00000000001
    def __init__(self):
        """put fields here"""

    def NormProbList(self, probCommandsList):
        probSum = 0.0
        for i in xrange(len(probCommandsList)):
            probSum += probCommandsList[i].Prob
        if (probSum - 0.0) > self.Epsilon:
            for i in xrange(len(probCommandsList)):
                probCommandsList[i].Prob = probCommandsList[i].Prob / probSum

    def __call__(self, command, probCommandsList):
        print " ".join(command.LexemsList).encode("utf-8")
        for wnum in xrange(len(command.LexemsList)):
            if command.LexemsList[wnum] == u"википедия":
                newCmd = copy.deepcopy(command)
                newCmd.Prob = 1.0
                newCmd.CommandLexems = command.LexemsList[wnum]
                newCmd.RequestLexems = [command.LexemsList[i] for i in xrange(len(command.LexemsList)) if i != wnum ]
                newCmd.CmdType = TCommandType["Wiki"]
                probCommandsList.append(newCmd)
            elif command.LexemsList[wnum] == u"погода":
                newCmd = copy.deepcopy(command)
                newCmd.Prob = 1.0
                newCmd.CommandLexems = command.LexemsList[wnum]
                newCmd.RequestLexems = [command.LexemsList[i] for i in xrange(len(command.LexemsList)) if i != wnum ]
                newCmd.CmdType = TCommandType["Weather"]
                probCommandsList.append(newCmd)
            elif command.LexemsList[wnum] == u"новости":
                newCmd = copy.deepcopy(command)
                newCmd.Prob = 1.0
                newCmd.CommandLexems = command.LexemsList[wnum]
                newCmd.RequestLexems = [command.LexemsList[i] for i in xrange(len(command.LexemsList)) if i != wnum ]
                newCmd.CmdType = TCommandType["News"]
                probCommandsList.append(newCmd)

        self.NormProbList(probCommandsList)

