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
import dialog_server.dispatcher.TDispatcher as TDispatcher
import dialog_server.command_matcher.TParser as TParser

PROJECT_BASE_DIR = os.getcwd() + "/.."
print PROJECT_BASE_DIR

class TDialogServer:
    def __init__(self):
        """put fields here"""

    def __call__(self):
        """put default action here"""

def main():

    # init all main objects
    server = THttpServer.THttpServer(\
            confPath=PROJECT_BASE_DIR + \
            "/conf/dialog_server.http_server.conf")

    client = THttpReply.THttpReply(\
            confPath=PROJECT_BASE_DIR + \
            "/conf/dialog_server.http_reply.conf")
    client.SendReply("Hallo!")

    parser = TParser.TParser(\
            confPath=PROJECT_BASE_DIR + \
            "/conf/dialog_server.parser.conf")

    cmdMatcher = TCommandMatcher.TCommandMatcher() 
    dispatcher = TDispatcher.TDispatcher(\
            client = client, \
            parser = parser, \
            commandMatcher = cmdMatcher)

    server.RequestHandlerFunc = dispatcher.RequestHandlerFunc

    dispatcher.RequestHandlerFunc(u"некоторая команда на русском")
    #server.Start()


if __name__ == '__main__':
    main()

