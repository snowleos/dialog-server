# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
sys.path.append("../..")
import dialog_server
from extern_lib.wizard_bind import TWizardBind

class TParser:
    def __init__(self, confPath="", wizardConfPath=""):
        self.WizardBind = TWizardBind(\
                confPath=wizardConfPath)

    def __call__(self, command, rawText):
        command.RawText = rawText
        jsonRespObj = self.WizardBind(rawText)
        command.Preprocessed = jsonRespObj
        command.LexemsList = list()
        for lexem in command.Preprocessed["Tokens"]:
            command.LexemsList.append(lexem["Text"])
        #command.RawText.split(" ")
