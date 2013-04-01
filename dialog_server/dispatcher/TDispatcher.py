# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
sys.path.append("../..")
import dialog_server
import dialog_server.command.TCommand as TCommand

class TDispatcher:
    def __init__(self, client=None, parser=None, commandMatcher=None):
        self.ReplyClient = client
        self.Parser = parser
        self.CommandMatcher = commandMatcher

    def __call__(self):
        """put default action here"""

    def SendResult(self, command):
        print command.ExecStatus
        print command.ResultText
        print command.DebugText
        replyText = command.ResultText
        self.ReplyClient.SendReply(replyText)

    def RequestHandlerFunc(self, ReqString):
        command = TCommand.TCommand()
        self.Parser(command, ReqString)
        # we could have some commands in input one
        commandsToExecList = list()
        self.CommandMatcher(command, commandsToExecList)

        for execCommand in commandsToExecList:
            print "CmdType:", execCommand.CmdType
            execCommand()
            self.SendResult(execCommand)
