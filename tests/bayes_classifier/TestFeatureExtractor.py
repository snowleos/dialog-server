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
from dialog_server.fact_extract.TFactExtractor import *
PROJECT_BASE_DIR = os.getcwd() + "/../.."

#TEST_PHRASES_FILE = "test_phrases_little.txt"
#PREPROC_CMDS_FILE = "preproc_cmds_little.txt"
TEST_PHRASES_FILE = "test_phrases.txt"
PREPROC_CMDS_FILE = "preproc_cmds.txt"

# init all main objects
parser = TParser(\
        confPath=PROJECT_BASE_DIR + \
        "/conf/dialog_server.parser.conf",\
        wizardConfPath=PROJECT_BASE_DIR + \
        "/conf/extern_lib.wizard_bind.conf")
command = TCommand()

factExtractor = TFactExtractor(PROJECT_BASE_DIR)

# make preprocessed commands
if not os.path.exists(PREPROC_CMDS_FILE):
    FCMD = open(TEST_PHRASES_FILE, "r")
    FSERCMD = open(PREPROC_CMDS_FILE, "w")
    for line in FCMD:
        if line.find("\t") != -1:
            cmdType, cmdText = line[:-1].decode('utf-8').split("\t")
            parser(command, cmdText)
            factExtractor(command)
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

extr = TBayesFeatureExtractor()
FSERCMD = open(PREPROC_CMDS_FILE, "r")
for line in FSERCMD:
    command.Read(line[:-1])
    print command.RawText
    extr(command)
    for ft in command.Features:
        print ft
    print ""


