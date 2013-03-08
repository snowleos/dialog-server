import sys
import os
import re
import subprocess
sys.path.append("../..")
import dialog_server

class TParser:
    def __init__(self, confPath=""):
        """put fields here"""

    def __call__(self, command, rawText):
        command.RawText = rawText
        command.LexemsList = command.RawText.split(" ")
