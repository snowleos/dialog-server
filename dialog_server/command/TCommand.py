# vim: set fileencoding=utf-8
import sys
import os
import re
import json
import subprocess
sys.path.append("../..")
import dialog_server

class TCommand:
    def __init__(self):
        self.RawText = "" # to refactor
        self.Preprocessed = None
        self.Features = None

        self.LexemsList = list() # to refactor
        self.CmdExecObj = None
        self.CmdType = ""
        # split all lexems to types: Command and Request
        self.CommandLexems = list()
        self.RequestLexems = list()
        self.Prob = 0.0
        # result
        self.ExecStatus = 0
        self.ResultText = ""
        self.DebugText = ""

    def __call__(self):
        self.ExecStatus, self.ResultText, self.DebugText = self.CmdExecObj(self)

    def Read(self, line):
        jsonObj = json.loads(line)
        self.RawText = jsonObj["RawText"]
        self.Preprocessed = jsonObj["Preprocessed"]
        self.Features = jsonObj["Features"]
        self.LexemsList = jsonObj["LexemsList"]
        self.CmdExecObj = None
        self.CmdType = jsonObj["CmdType"]
        self.CommandLexems = jsonObj["CommandLexems"]
        self.RequestLexems = jsonObj["RequestLexems"]
        self.Prob = float(jsonObj["Prob"])
        self.ExecStatus = int(jsonObj["ExecStatus"])
        self.ResultText = jsonObj["ResultText"]
        self.DebugText = jsonObj["DebugText"]

    # returns JSON string
    def Write(self):
        binData = json.dumps({
            "RawText": self.RawText,
            "Preprocessed": self.Preprocessed,
            "Features": self.Features,
            "LexemsList": self.LexemsList,
            #"CmdExecObj": not serialized,
            "CmdType": self.CmdType,
            "CommandLexems": self.CommandLexems,
            "RequestLexems": self.RequestLexems,
            "Prob": self.Prob,
            "ExecStatus": self.ExecStatus,
            "ResultText": self.ResultText,
            "DebugText": self.DebugText
            })
        print binData
        return binData


