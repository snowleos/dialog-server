# vim: set fileencoding=utf-8
import sys
import os
import re
import shlex
import subprocess
import ConfigParser
sys.path.append("../..")
import common_lib.common_ops as common_ops

"""
получаем факты в виде списка factsList словарей вида
"RuleName": "name",
"RuleNumber": "порядковый номер в выдаче реморфа, 0 - самый главный",
"StartSymbol": "начальный символ факта в строке запроса",
"EndSymbol": "конечный символ + 1",
"Value": {"имя факта": ["строка текста с фактом", "еще факт"], "имя факта": ["строка"], ... }

Пример:
        0       15      ROUTE   cmd[поехал]     to.title[дом]
"""

class TRemorphBind:
    def __init__(self, projBaseDir="", confPath=""):
        self.Conf = ConfigParser.ConfigParser()
        self.Conf.read(confPath)
        self.ProjectBaseDir = projBaseDir
        self.BinName = self.Conf.get("Main", "RemorphExec")
        self.Options = self.Conf.get("Main", "RemorphOptions")
        self.MainRulesPath = self.Conf.get("Main", "RemorphMainRulesPath")
        self.MainRulesFile = self.Conf.get("Main", "RemorphMainRulesFile")

    def __HandleOutput(self, outStr, factsList):
        outStrLines = outStr.split("\n")
        lineNum = 0
        for line in outStrLines:
            print "LINE", line
            # Пропускаем первую строчку с исходным запросом
            if lineNum != 0 and line != "":
                factFields = line.split("\t")
                if len(factFields) < 5:
                    raise Exception("Wrong format of fact\n"+line)
                factsList.append( {
                        "RuleName": factFields[3],
                        "RuleNumber": lineNum - 1,
                        "StartSymbol": factFields[1],
                        "EndSymbol": factFields[2],
                        "Value": {}
                        }
                        )
                for factNum in xrange(4, len(factFields)):
                    # to.title[дом]
                    # пока что только одно значение, больше не встречал
                    valuePos = factFields[factNum].find("[")
                    factName = factFields[factNum][:valuePos]
                    valueEndPos = factFields[factNum].find("]")
                    factValue = factFields[factNum][valuePos+1:valueEndPos]
                    factsList[-1]["Value"][factName] = [factValue]


                print factsList[-1]

            lineNum += 1

    def __call__(self, queryStr):
        MainRulesFileRealPath = self.ProjectBaseDir + "/" + \
                self.MainRulesFile
        cmd = "( " + \
                "cd " + self.ProjectBaseDir + "/" + \
                self.MainRulesPath + " && " + \
                self.BinName + " " + \
                self.Options + " " + \
                " -f " + self.MainRulesFile + \
                " )"
        #print cmd
        proc = subprocess.Popen(["-c", cmd],
                stdin = subprocess.PIPE,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                shell=True)
        moduleInput = queryStr#.encode("utf-8")
        if moduleInput[-1] != "\n":
            moduleInput += "\n"
        #print moduleInput
        out, err = proc.communicate(input=moduleInput)
        retVal = proc.returncode
        #print "     ERR:"
        #print err
        #print "     OUT:"
        #print out
        #print "     RET:"
        #print retVal
        factsList = list()
        self.__HandleOutput(out, factsList)
        if retVal != 0:# or out == None or out == "":
            errorMes = "Something wrong with TRemorphBind\n"
            if err != None:
                errorMes += err
            raise Exception(errorMes)
        return factsList
