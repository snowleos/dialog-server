# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
import copy
sys.path.append("../..")
import dialog_server
from dialog_server.command_matcher.TCommandType import *
from dialog_server.command.TCommand import *
import ConfigParser

class TProbCommandProps:
    def __init__(self, name="DefaultCommand", prob=1.0, wnum=[-1]):
        self.Prob = prob
        self.Name = name
        self.CmdTokensNumList = wnum
    def __str__(self):
        return "Prob = "+str(self.Prob)+", "+str(self.Name)+", "+str(self.CmdTokensNumList)

class TCommandCreator:
    ProjectBaseDir = ""
    @classmethod
    def Init(self, projectBaseDir=""):
        self.ProjectBaseDir = projectBaseDir

    @classmethod
    def CreateNewCommand(self, probCmd, sourceCmd=None):
        newCmd = TCommand()
        newCmd = copy.deepcopy(sourceCmd)
        newCmd.Prob = probCmd.Prob
        # returns new command object
        newCmd.CmdType = probCmd.Name
        if newCmd.CmdType not in TCommandType:
            print >> sys.stderr, "No such command" + probCmd.Name + ". DefaultCommand set."
            newCmd.CmdType = "DefaultCommand"
        # create Exec Object for operation
        cmdProps = TCommandType[newCmd.CmdType]
        defaultProps = TCommandType["DefaultCommand"]
        operationType = GetCommandProperty(newCmd.CmdType, "OperationType")
        try:
            # cmdProps["OperationType"] is type
            newCmd.CmdExecObj = operationType(newCmd.CmdType)
        except:
            raise Exception("No such class " + str(operationType))
        
        newCmd.CmdExecObj.Name = newCmd.CmdType
        newCmd.CmdExecObj.ModuleRelPath = GetCommandProperty(newCmd.CmdType, "ModuleRelPath")
        newCmd.RequestFields = GetCommandProperty(newCmd.CmdType, "RequestFields")
        #print "RequestFields", newCmd.RequestFields

        # TODO: set Preparer class instead of following operation
        if len(sourceCmd.LexemsList) > 0:
            newCmd.CommandLexems = [sourceCmd.LexemsList[wnum] \
                    for wnum in probCmd.CmdTokensNumList \
                    if ((wnum > -1) and (wnum < len(sourceCmd.LexemsList)))]

            newCmd.RequestLexems = [sourceCmd.LexemsList[i] \
                    for i in xrange(len(sourceCmd.LexemsList)) \
                    if i not in probCmd.CmdTokensNumList ]

        return newCmd


