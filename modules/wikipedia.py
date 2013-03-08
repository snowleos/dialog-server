#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib
import json
import re
from pyquery import PyQuery as pq

def get_definition(term):
    query_url = "http://ru.wikipedia.org/w/api.php?action=query&titles=%s&format=json" % term
    page = json.load(urllib.urlopen(query_url))["query"]["pages"].iteritems().next()[1]["title"]
    text_url = "http://ru.wikipedia.org/w/api.php?format=json&action=parse&page=%s&prop=text" % page
    doc_string = json.load(urllib.urlopen(text_url.encode('utf-8')))['parse']['text']['*']
    doc = pq(doc_string)
    definition = doc('p').html().encode('utf-8')
    definition = re.sub("(<[^<>]*>|\[[^\[\]]*\])", "", definition)
    return definition

try:
    print get_definition(sys.argv[1])
except:
    sys.exit(1)
