# vim: set fileencoding=utf-8
import sys
import os
import re
import copy
import subprocess
import weakref
sys.path.append("../..")
import dialog_server
import common_lib.common_ops as common_ops
from dialog_server.command.TCommandCreator import *
from dialog_server.command_matcher.TCommandType import *

class TCommandMatcher:
    def __init__(self):
        self.ClassifiersList = list()
        """put fields here"""

    def FindMostProbCommands(self, command, classifiersOutList, commandsToExecList):
        mostProbCmd = None
        maxProb = -1
        probsCnt = 0
        probsSum = 0.0
        for i in xrange(len(classifiersOutList)):
            for k in classifiersOutList[i].keys():
                probsCnt += 1
                probsSum += classifiersOutList[i][k].Prob
                if classifiersOutList[i][k].Prob > maxProb:
                    maxProb = classifiersOutList[i][k].Prob
                    mostProbCmd = weakref.ref(classifiersOutList[i][k])

        # find average prob
        probAvg = 0.0
        if probsCnt != 0:
            probAvg = probsSum / probsCnt
            # check mostProbCmd. if it differs less than 12% of average
            # then set it as DefaultCommand
            if ((mostProbCmd().Prob - probAvg) / probAvg) < 0.12 or (mostProbCmd().Prob < 0.07):
                mostProbCmd().Name = "DefaultCommand"
                print >> sys.stderr, "TCommandMatcher:\n" + \
                        "(mostProbCmd().Prob - probAvg) / probAvg) < 0.12\n"+ \
                        "("+str(mostProbCmd().Prob)+" - "+str(probAvg)+") / "+str(probAvg)+") = "+ \
                        str((mostProbCmd().Prob - probAvg) / probAvg) + "< 0.12"

        commandsToExecList.append(TCommandCreator.CreateNewCommand(mostProbCmd(), command))

    def __call__(self, command, commandsToExecList):
        classifiersOutList = list()
        print >> sys.stderr, "CLASSIFY COMMAND:"
        for ft, cl in self.ClassifiersList:
            if ft != None:
                ft(command)
            classifiersOutList.append(dict())
            cl(command, classifiersOutList[-1])
            for prob in classifiersOutList[-1].values():
                print prob

        self.FindMostProbCommands(command, classifiersOutList, commandsToExecList)

        # add most prob command as a fact
        command.FactsList.append(("CmdType", commandsToExecList[0].CmdType))

        # NOTE: now we return only one most prob command
        # among found by all classifiers
        print commandsToExecList[0].CmdType
