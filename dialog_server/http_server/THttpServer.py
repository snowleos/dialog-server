# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
sys.path.append("../..")
import dialog_server
import cherrypy

"""
Dialog HTTP server
Got query like 
"""

def TestRequestHandlerFunc(ReqString):
    # for test
    print ReqString


class THttpServer:
    def __init__(self, confPath=""):
        self.RequestHandlerFunc = TestRequestHandlerFunc
        self.Conf = os.path.join(os.path.dirname(__file__), confPath)

    def Start(self):
        cherrypy.quickstart(self, config=self.Conf)

    def index(self):
        return '''
        Usage: http://127.0.0.1:8080/GetReply?ReqString=\<your request\>
        To change URL and port edit file dialog_server.conf
            '''
    index.exposed = True

    def GetReply(self, ReqString=None):
        if ReqString != None:
            return ReqString
        else:
            return ""
    GetReply.exposed = True

    def SendRequest(self, ReqString=None):
        print >>sys.stderr, "ReqString", ReqString.encode("utf-8")
        self.RequestHandlerFunc(ReqString)
        return "OK"
    SendRequest.exposed = True

