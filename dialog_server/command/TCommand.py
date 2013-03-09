# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
sys.path.append("../..")
import dialog_server
from dialog_server.command_matcher.TCommandType import *

class TCommand:
    def __init__(self):
        self.RawText = ""
        self.LexemsList = list()
        self.CmdExecObj = None
        self.CmdType = TCommandType["NoCommand"]
        # split all lexems to types: Command and Request
        self.CommandLexems = list()
        self.RequestLexems = list()
        self.Prob = 0.0
        # result
        self.ExecStatus = 0
        self.ResultText = ""
        self.DebugText = ""

    def __call__(self):
        self.CmdExecObj = self.CmdType.GetExecObj()
        self.ExecStatus, self.ResultText, self.DebugText = self.CmdExecObj(self.RequestLexems)
