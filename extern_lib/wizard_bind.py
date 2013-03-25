# vim: set fileencoding=utf-8
import sys
import os
import ConfigParser
import urllib2
from httplib import HTTPConnection
import json

class TWizardBind:
    def __init__(self, confPath=""):
        self.Conf = ConfigParser.ConfigParser()
        self.Conf.read(confPath)
        self.SocketHost = self.Conf.get("Service", "SocketHost")
        self.SocketPort = self.Conf.get("Service", "SocketPort")
        self.GetRequestParameters = self.Conf.get("Service", "GetRequestParameters")

    def __call__(self, queryText):
        print queryText.encode("utf-8")
        #try:
        self.Conn = HTTPConnection(self.SocketHost, self.SocketPort)
        self.Conn.set_debuglevel(5)
        self.Conn.request("GET", self.GetRequestParameters + urllib2.quote(queryText.encode("utf-8")))
        resp = self.Conn.getresponse()
        responseString = resp.read()
        self.Conn.close()
        print >> sys.stderr, "TWizardBind:Answer:", responseString
        jsonReplyObj = None
        try:
            jsonReplyObj = json.loads(responseString)
            print >> sys.stderr, "TWizardBind: Json object: ", jsonReplyObj
        except:
            print >> sys.stderr, "TWizardBind: can't parse json response"
        #except:
        #    print >> sys.stderr, "TWizardBind: Something wrong with connection"
        return jsonReplyObj




