# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
sys.path.append("../..")
import dialog_server

class TCommandType:
    NoCommand = 0
    Search = NoCommand + 1
    Wiki = Search + 1
    News = Wiki + 1
    Weather = News + 1
    ExternalDevice = Weather + 1
    Notify = ExternalDevice + 1
    TypesCount = Notify + 1

class TCommandMatcher:
    def __init__(self):
        """put fields here"""

    def __call__(self, command):
        # got command with splitted words
        probList = [0] * TCommandType.TypesCount

        outStr = " ".join(command.LexemsList).encode("utf-8")
        print outStr

        for word in command.LexemsList:
            if word == u"википедия":
                probList[TCommandType.Wiki] = 1.0
            elif word == u"погода":
                probList[TCommandType.Weather = 1.0

        mostProbCmd = TCommandType.NoCommand
        maxProb = -1.0
        for i in xrange(len(probList)):
            if probList[i] > maxProb:
                maxProb = probList[i]
                mostProbCmd = i




    

