#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib
import json
import re
from pyquery import PyQuery as pq

DEBUG = False

def SafeExec(func):
    try:
        func()
    except Exception as inst:
        print >> sys.stderr, type(inst)
        print >> sys.stderr, inst
        sys.exit(1)
def PrintDebug(obj):
    if DEBUG == True:
        print >> sys.stderr, obj


class TWikiGetDefinition:
    term = None
    query_url = None
    page = None
    text_url = None
    doc_string = None
    doc = None
    definition = None

    def Do_term(self):
        self.term = ""
        for line in sys.stdin:
            self.term += line[:-1] + " "
        PrintDebug(self.term)
    def Do_query_url(self):
        self.query_url = "http://ru.wikipedia.org/w/api.php?action=query&titles=%s&format=json" % self.term
        PrintDebug(self.query_url)

    def Do_page(self):
        self.page = json.load(urllib.urlopen(self.query_url))["query"]["pages"].iteritems().next()[1]["title"]
        PrintDebug(self.page)

    def Do_text_url(self):
        self.text_url = "http://ru.wikipedia.org/w/api.php?format=json&action=parse&page=%s&prop=text" % self.page
        PrintDebug(self.text_url)

    def Do_doc_string(self):
        self.doc_string = json.load(urllib.urlopen(self.text_url.encode('utf-8')))['parse']['text']['*']
        PrintDebug(self.doc_string)

    def Do_doc(self):
        self.doc = pq(self.doc_string)
        PrintDebug(self.doc)

    def Do_definition_doc(self):
        self.definition = self.doc('p').html().encode('utf-8')
        PrintDebug(self.definition)

    def Do_definition_sub(self):
        self.definition = re.sub("(<[^<>]*>|\[[^\[\]]*\])", "", self.definition)
        PrintDebug(self.definition)


    def GetDefinition(self):
        SafeExec(self.Do_term)
        SafeExec(self.Do_query_url)
        SafeExec(self.Do_page)
        SafeExec(self.Do_text_url)
        SafeExec(self.Do_doc_string)
        SafeExec(self.Do_doc)
        SafeExec(self.Do_definition_doc)
        SafeExec(self.Do_definition_sub)
        return self.definition

WikiGetDefinition = TWikiGetDefinition()
print WikiGetDefinition.GetDefinition()

