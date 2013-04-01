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
import dialog_server as dialog_server
import dialog_server.command_matcher.TCommandMatcher as TCommandMatcher
import dialog_server.command_matcher.TParser as TParser
import dialog_server.dispatcher.TDispatcher as TDispatcher
import dialog_server.http_client.THttpReply as THttpReply
import dialog_server.http_server.THttpServer as THttpServer

PROJECT_BASE_DIR = common_ops.GetProjectBaseDir()
print PROJECT_BASE_DIR

class TDialogServer:
    def __init__(self):
        """put fields here"""

    def __call__(self):
        """put default action here"""

def main():

    # example of how to use root extractor
    #from extern_lib.derivat_bind import TDerivatBind
    #Derivat = TDerivatBind(\
    #        confPath=PROJECT_BASE_DIR + \
    #        "/conf/extern_lib.derivat_bind.conf")
    #print Derivat(u"новости", u"новостной")
    #sys.exit(0)

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
    

    # ---------------------- init client and server --------------------
    server = THttpServer.THttpServer(\
            confPath=PROJECT_BASE_DIR + \
            "/conf/dialog_server.http_server.conf")

    client = THttpReply.THttpReply(\
            confPath=PROJECT_BASE_DIR + \
            "/conf/dialog_server.http_reply.conf")
    client.SendReply("Hallo!")

    # ---------------------- init main dispatcher ----------------------    
    dispatcher = TDispatcher.TDispatcher(\
            client = client, \
            parser = parser, \
            commandMatcher = cmdMatcher)

    # set handle function
    server.RequestHandlerFunc = dispatcher.RequestHandlerFunc

    server.Start()


if __name__ == '__main__':
    main()

