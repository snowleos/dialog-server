# -*- coding: utf-8 -*-
import sys
import urllib
import json
import re
from pyquery import PyQuery as pq
from decorators import with_exceptions
from exceptions import NoSuchMinerException

class WikipediaMiner(object):
    def __init__(self):
        self.query_url = "http://ru.wikipedia.org/w/api.php?action=query&titles={0}&format=json"
        self.text_url = "http://ru.wikipedia.org/w/api.php?format=json&action=parse&page={0}&prop=text"

    @with_exceptions
    def __call__(self, term):
        """Wikipedia miner"""
        query_url = self.query_url.format(term)
        page = json.load(urllib.urlopen(query_url))["query"]["pages"].iteritems().next()[1]["title"]
        text_url = self.text_url.format(page)
        doc_string = json.load(urllib.urlopen(text_url.encode('utf-8')))['parse']['text']['*']
        doc = pq(doc_string)
        definition = doc('p').html().encode('utf-8')
        definition = re.sub("(<[^<>]*>|\[[^\[\]]*\])", "", definition)
        return definition


DATA_MINERS = {
    "Wiki": WikipediaMiner()
}

def get_miner(name):
    if name in DATA_MINERS:
        return DATA_MINERS[name]
    else:
        raise NoSuchMinerException()