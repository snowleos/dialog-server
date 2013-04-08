# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
sys.path.append("..")

from dialog_server.classifier.TBayesClassifier import *
from dialog_server.classifier.TExactClassifier import *
from dialog_server.command.TCommand import *
from dialog_server.command.TCommandCreator import *
from dialog_server.exec_objects.TExecObjectBase import *
import common_lib.common_ops as common_ops
#import dialog_server as dialog_server
import dialog_server.command_matcher.TCommandMatcher as TCommandMatcher
import dialog_server.command_matcher.TParser as TParser
#import dialog_server.dispatcher.TDispatcher as TDispatcher
#import dialog_server.http_client.THttpReply as THttpReply
#import dialog_server.http_server.THttpServer as THttpServer

PROJECT_BASE_DIR = common_ops.GetProjectBaseDir()
print PROJECT_BASE_DIR

class TDialogServer:
    def __init__(self):
        """put fields here"""

    def __call__(self):
        """put default action here"""

def main():

    # ------------------------init all main objects --------------------
    parser = TParser.TParser(\
            confPath=PROJECT_BASE_DIR + \
            "/conf/dialog_server.parser.conf",\
            wizardConfPath=PROJECT_BASE_DIR + \
            "/conf/extern_lib.wizard_bind.conf")
    command = TCommand()

    cmdMatcher = TCommandMatcher.TCommandMatcher()
    exactClassifier = TExactClassifier()
    cmdMatcher.ClassifiersList.append((None, exactClassifier))
    bayesClassifier = TBayesClassifier(common_ops.GetProjectBaseDir() + \
            "/conf/bayes_classifier.conf")
    bayesClassifier.LoadModel()
    cmdMatcher.ClassifiersList.append((TBayesFeatureExtractor(), bayesClassifier))

    # Dispatcher, http clientt  and server are not used here
    # Instead the program listens  to  stdin, recognizes command
    # writes cmd type to stdout and lots of info to stderr

    print "Exit by Ctrl+d"
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        print "You typed " + line[:-1]
        reqString = line[:-1].decode("utf-8")

        command = TCommand()
        parser(command, reqString)
        # we could have some commands in input one
        commandsToExecList = list()
        cmdMatcher(command, commandsToExecList)

        for execCommand in commandsToExecList:
            print "CmdType:", execCommand.CmdType
        


if __name__ == '__main__':
    main()

