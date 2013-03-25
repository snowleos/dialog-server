import sys
import os
import re
import subprocess
sys.path.append("../..")
import dialog_server
import ConfigParser
import urllib2
from httplib import HTTPConnection

class THttpReply:
    def __init__(self, confPath=""):
        self.Conf = ConfigParser.ConfigParser()
        self.Conf.read(confPath)
        socketHost = self.Conf.get("THttpReplyConnection", "socket_host")
        socketPort = self.Conf.get("THttpReplyConnection", "socket_port")
        print socketHost, socketPort
        self.Conn = HTTPConnection(socketHost, socketPort)
        self.Conn.set_debuglevel(5)
        self.SendReply("Ping")

    def __call__(self):
        """put default action here"""

    def SendReply(self, replyStr):
        print >> sys.stderr, "Send reply:", replyStr.encode("utf-8")
        print >> sys.stdout, "Reply:", replyStr.encode("utf-8")
        self.Conn.request("GET", "/GetReply?ReqString=" + urllib2.quote(replyStr.encode("utf-8")))
        resp = self.Conn.getresponse()
        print >> sys.stderr, "Reply sent. Answer:", resp.read()

