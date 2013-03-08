#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib
import re
from HTMLParser import HTMLParser
from lxml import etree
from pyquery import PyQuery as pq

def search(term):
    query_url = "http://xmlsearch.yandex.ru/xmlsearch?user=direvius&key=03.111162353:036864b8fd36c9f5203989ac2fdb6ac4&query=%s" % term
    response = urllib.urlopen(query_url).read()
    root = etree.fromstring(response)
    #doc_tree = urllib.urlopen(query_url.encode('utf-8')).read()
    return root.xpath('//doc/title')

try:
    doc_title = search(' '.join(sys.argv))[0]
    print HTMLParser().unescape(re.sub("(<[^<>]*>)", "", etree.tostring(doc_title)))
except:
    sys.exit(1)
