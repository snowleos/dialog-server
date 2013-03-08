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

    def RequestHandlerFunc(self, ReqString):

        command = TCommand.TCommand()

        self.Parser(command, ReqString)
        self.CommandMatcher(command)

        
