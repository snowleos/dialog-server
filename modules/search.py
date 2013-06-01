#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib
import re
from HTMLParser import HTMLParser
from lxml import etree
from pyquery import PyQuery as pq

DEBUG = True

def SafeExec(func):
    try:
        func()
    except Exception as inst:
        print >> sys.stderr, "FUNC", func
        print >> sys.stderr, "TYPE", type(inst)
        print >> sys.stderr, "INST", inst
        print "Не удалось найти. Попробуйте переформулировать:)"
        sys.exit(1)
def PrintDebug(obj):
    if DEBUG == True:
        print >> sys.stderr, obj

class TSearchGetResult:
    def __init__(self):
        self.term = None
        self.query_url = None
        self.response = None
        self.root = None
        self.doc_title = None
        self.parsed_doc = None

    def Do_term(self):
        self.term = ""
        for line in sys.stdin:
            self.term += line[:-1] + " "
        PrintDebug(self.term)
    def Do_query_url(self):
        self.query_url = "http://xmlsearch.yandex.ru/xmlsearch?user=direvius&key=03.111162353:036864b8fd36c9f5203989ac2fdb6ac4&query=%s" % self.term
        PrintDebug(self.query_url)

    def Do_response(self):
        self.response = urllib.urlopen(self.query_url).read()
        PrintDebug(self.response)

    def Do_root(self):
        self.root = etree.fromstring(self.response)
        PrintDebug(self.root)

    def Do_doc_title(self):
        doc_title = self.root.xpath('//doc/title')
        PrintDebug(self.doc_title)

    def Do_parsed_doc(self):
        self.parsed_doc = HTMLParser().unescape(re.sub("(<[^<>]*>)", "", etree.tostring(self.doc_title)))
        PrintDebug(self.parsed_doc)

    def search(self):
        SafeExec(self.Do_term)
        SafeExec(self.Do_query_url)
        SafeExec(self.Do_response)
        SafeExec(self.Do_root)
        SafeExec(self.Do_doc_title)
        SafeExec(self.Do_parsed_doc)


SearchGetResult = TSearchGetResult()
print SearchGetResult.search().encode('utf-8')
