import sys
import os
import re
import subprocess
sys.path.append("../..")
import dialog_server

class TSameRootClassifier:
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
                probCommandsList.append(TCommandCreator.CreateNewCommand(\
                        name="Wiki", prob=1.0, wnum=wnum, sourceCmd=command))
            elif command.LexemsList[wnum] == u"погода":
                probCommandsList.append(TCommandCreator.CreateNewCommand(\
                        name="Weather", prob=1.0, wnum=wnum, sourceCmd=command))
            elif command.LexemsList[wnum] == u"новости":
                probCommandsList.append(TCommandCreator.CreateNewCommand(\
                        name="News", prob=1.0, wnum=wnum, sourceCmd=command))
            elif command.LexemsList[wnum] == u"поиск":
                probCommandsList.append(TCommandCreator.CreateNewCommand(\
                        name="Search", prob=1.0, wnum=wnum, sourceCmd=command))

        self.NormProbList(probCommandsList)

