"""
Dialog HTTP server
Got query like 
"""

import cherrypy
import sys

class TTSStub:
    def index(self):
        return '''
        Usage: http://127.0.0.1:8081/GetReply?ReqString=\<your request\>
        To change URL and port edit file dialog_server.conf
            '''
    index.exposed = True

    def GetReply(self, ReqString=None):
        print >> sys.stderr, "Got string " + ReqString
        if ReqString != None:
            return ReqString
        else:
            return ""
    GetReply.exposed = True

import os.path
tutconf = os.path.join(os.path.dirname(__file__), 'tts_stub.conf')

if __name__ == '__main__':
    cherrypy.quickstart(TTSStub(), config=tutconf)
