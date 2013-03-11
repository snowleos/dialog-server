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
from dialog_server.exec_objects.TExecObjectSpecify import *
from dialog_server.exec_objects.TExecObjectOperation import *
from dialog_server.exec_objects.TExecObjectMetaCommand import *

class TCommandCreator:
    def __init__(self):
        """put fields here"""

    def __call__(self):
        """put default action here"""

    @staticmethod
    def CreateNewCommonCommand(name="NoCommand", prob=1.0, wnum=-1, sourceCmd=None):
        newCmd = TCommand()
        if sourceCmd != None:
            newCmd = copy.deepcopy(sourceCmd)
            newCmd.Prob = prob
            if len(sourceCmd.LexemsList) > 0:
                if (wnum > -1) and (wnum <  len(sourceCmd.LexemsList)):
                    newCmd.CommandLexems = sourceCmd.LexemsList[wnum]
                newCmd.RequestLexems = [sourceCmd.LexemsList[i] for i in xrange(len(sourceCmd.LexemsList)) if i != wnum ]
        newCmd.CmdType = TCommandType[name]
        return newCmd

    @staticmethod
    def CreateNewCommand(name="NoCommand", prob=1.0, wnum=-1, sourceCmd=None):
        # returns new command object
        newCmd = None
        if name == "NoCommand":
            newCmd = TCommandCreator.CreateNewCommonCommand(name, prob, wnum, sourceCmd)
        elif name == "Search":
            newCmd = TCommandCreator.CreateNewCommonCommand(name, prob, wnum, sourceCmd)
        elif name == "Wiki":
            newCmd = TCommandCreator.CreateNewCommonCommand(name, prob, wnum, sourceCmd)
        elif name == "News":
            newCmd = TCommandCreator.CreateNewCommonCommand(name, prob, wnum, sourceCmd)
        elif name == "Weather":
            newCmd = TCommandCreator.CreateNewCommonCommand(name, prob, wnum, sourceCmd)
        elif name == "ExternalDevice":
            raise Exception(" TCommandCreator: command not implemented: "+name)
        elif name == "Notify":
            raise Exception(" TCommandCreator: command not implemented: "+name)
        elif name == "ChatBotReply":
            raise Exception(" TCommandCreator: command not implemented: "+name)
        elif name == "DontUnderstand":
            raise Exception(" TCommandCreator: command not implemented: "+name)
        elif name == "RequestMoreInfo":
            raise Exception(" TCommandCreator: command not implemented: "+name)
        elif name == "StopCurrentCmd":
            raise Exception(" TCommandCreator: command not implemented: "+name)
        elif name == "RememberContext":
            raise Exception(" TCommandCreator: command not implemented: "+name)
        else:
            raise Exception(" TCommandCreator: unknown command: "+name)
        return newCmd
