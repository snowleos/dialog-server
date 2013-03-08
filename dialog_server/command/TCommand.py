# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
sys.path.append("../..")
import dialog_server

class TCommand:
    def __init__(self):
        self.RawText = ""
        self.LexemsList = list()
        self.CmdType = None
        self.CmdExecObj = None


    def __call__(self):
        self.CmdExecObj(self)
