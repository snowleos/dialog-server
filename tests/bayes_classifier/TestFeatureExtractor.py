# vim: set fileencoding=utf-8
import sys
import os
import re
import json
import time
import subprocess
sys.path.append("../..")
import dialog_server
from dialog_server.command_matcher.TCommandType import *
from dialog_server.command.TCommand import *
from dialog_server.command_matcher.TParser import *
from dialog_server.classifier.TBayesFeatureExtractor import *
PROJECT_BASE_DIR = os.getcwd() + "/../.."

# init all main objects
parser = TParser(\
        confPath=PROJECT_BASE_DIR + \
        "/conf/dialog_server.parser.conf",\
        wizardConfPath=PROJECT_BASE_DIR + \
        "/conf/extern_lib.wizard_bind.conf")
command = TCommand()


# make preprocessed commands
FCMD = open("test_phrases.txt", "r")
FSERCMD = open("preproc_cmds.txt", "w")
for line in FCMD:
    cmdType, cmdText = line[:-1].decode('utf-8').split("\t")
    parser(command, cmdText)
    time.sleep(0.5)
    command.CmdType = cmdType
    outStr = command.Write()
    FSERCMD.write(outStr+"\n")
FSERCMD.close()

# test json serializing
"""
FSERCMD = open("preproc_cmds.txt", "r")
FSERCMD2 = open("preproc_cmds2.txt", "w")
for line in FSERCMD:
    command.Read(line[:-1])
    FSERCMD2.write(command.Write()+"\n")
# files have to be same
"""

# TestFeatureExtractor
"""
extr = TBayesFeatureExtractor()
FSERCMD = open("preproc_cmds.txt", "r")
for line in FSERCMD:
    command.Read(line[:-1])
    extr(command)
    print ""

"""
