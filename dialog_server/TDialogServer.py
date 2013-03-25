# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
sys.path.append("..")
import dialog_server as dialog_server
import dialog_server.http_server.THttpServer as THttpServer
import dialog_server.http_client.THttpReply as THttpReply
import dialog_server.command_matcher.TCommandMatcher as TCommandMatcher
import dialog_server.command.TCommand as TCommand
import dialog_server.dispatcher.TDispatcher as TDispatcher
import dialog_server.command_matcher.TParser as TParser
import dialog_server.exec_objects.TExecObjectBase as TExecObjectBase

PROJECT_BASE_DIR = os.getcwd() + "/.."
print PROJECT_BASE_DIR

class TDialogServer:
    def __init__(self):
        """put fields here"""

    def __call__(self):
        """put default action here"""

def main():

    #from extern_lib.derivat_bind import TDerivatBind
    #Derivat = TDerivatBind(\
    #        confPath=PROJECT_BASE_DIR + \
    #        "/conf/extern_lib.derivat_bind.conf")
    #print Derivat(u"новости", u"новостной")
    #sys.exit(0)

    # init all main objects
    parser = TParser.TParser(\
            confPath=PROJECT_BASE_DIR + \
            "/conf/dialog_server.parser.conf",\
            wizardConfPath=PROJECT_BASE_DIR + \
            "/conf/extern_lib.wizard_bind.conf")
    command = TCommand.TCommand()
    #parser(command, u"мама мыла раму")
    #sys.exit(0)

    server = THttpServer.THttpServer(\
            confPath=PROJECT_BASE_DIR + \
            "/conf/dialog_server.http_server.conf")

    client = THttpReply.THttpReply(\
            confPath=PROJECT_BASE_DIR + \
            "/conf/dialog_server.http_reply.conf")
    client.SendReply("Hallo!")

    TExecObjectBase.TExecObjectBase.ProjectBaseDir = PROJECT_BASE_DIR+"/"
    TExecObjectBase.TExecObjectBase.ConfPath = \
            PROJECT_BASE_DIR + \
            "/conf/dialog_server.exec_objects.conf"

    cmdMatcher = TCommandMatcher.TCommandMatcher() 
    dispatcher = TDispatcher.TDispatcher(\
            client = client, \
            parser = parser, \
            commandMatcher = cmdMatcher)

    server.RequestHandlerFunc = dispatcher.RequestHandlerFunc

    #dispatcher.RequestHandlerFunc(u"некоторая погода команда на русском")
    #dispatcher.RequestHandlerFunc(u"википедия барселона")
    server.Start()


if __name__ == '__main__':
    main()

