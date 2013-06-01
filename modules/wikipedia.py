#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib
import urllib2
import json
from xml.dom import minidom
import re
from pyquery import PyQuery as pq

DEBUG = True

def SafeExec(func):
    try:
        func()
    except Exception as inst:
        print >> sys.stderr, func
        print >> sys.stderr, type(inst)
        print >> sys.stderr, inst
        print "Не удалось найти. Попробуйте переформулировать:)"
        sys.exit(1)
def PrintDebug(obj):
    if DEBUG == True:
        print >> sys.stderr, obj

# Беру заголовок страницы через opensearch и xml, чтобы избежать редиректов и получить 
# реальный заголовок страницы
# http://habrahabr.ru/post/104480/
# http://ru.wikipedia.org/w/api.php?action=opensearch&search=%D0%96%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%BB%D1%8C%20%D0%B1%D0%B5%D0%BB%D1%8C%D0%BC%D0%BE%D0%BD%D0%B4%D0%BE&format=xml
# http://ru.wikipedia.org/w/api.php?format=json&action=parse&page=%D0%91%D0%B5%D0%BB%D1%8C%D0%BC%D0%BE%D0%BD%D0%B4%D0%BE,%20%D0%96%D0%B0%D0%BD-%D0%9F%D0%BE%D0%BB%D1%8C&prop=text

class TWikiGetDefinition:
    term = None
    query_url = None
    page = None
    text_url = None
    doc_string = None
    doc = None
    definition = None
    completeurl = None

    def Do_term(self):
        self.term = ""
        for line in sys.stdin:
            self.term += line[:-1] + " "
        PrintDebug(self.term)
    def Do_query_url(self):
        #self.query_url = "http://ru.wikipedia.org/w/api.php?action=query&titles=%s&format=json" % self.term
        self.query_url = "http://ru.wikipedia.org/w/api.php?action=opensearch&format=xml&search=%s" % self.term
        PrintDebug(self.query_url)

    def Do_page(self):
        #self.page = json.load(urllib.urlopen(self.query_url))["query"]["pages"].iteritems().next()[1]["title"]
        xmlDoc = minidom.parse(urllib.urlopen(self.query_url))
        SearchSuggestion = xmlDoc.getElementsByTagName("SearchSuggestion")[0]
        PrintDebug(SearchSuggestion)
        Section = xmlDoc.getElementsByTagName("Section")[0]
        PrintDebug(Section)
        Item = xmlDoc.getElementsByTagName("Item")[0]
        PrintDebug(Item)
        Text = Item.getElementsByTagName("Text")[0]
        PrintDebug(Text)
        Url = Item.getElementsByTagName("Url")[0]
        PrintDebug(Url)
        Description = Item.getElementsByTagName("Description")[0]
        
        self.page = Text.childNodes[0].nodeValue
        PrintDebug(self.page)
        self.completeurl = Url.childNodes[0].nodeValue
        PrintDebug(self.completeurl)
        self.definition = Description.childNodes[0].nodeValue
        PrintDebug(self.definition)

    def Do_text_url(self):
        #self.text_url = "http://ru.wikipedia.org/w/api.php?format=json&action=parse&page=%s&prop=text" % self.page
        # берем текст из exstracts вместо полной статьи
        # ХРЕНЬ! нормальные результаты дает через раз
        self.text_url = "http://ru.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exsentences=10&titles=%s" % self.page
        PrintDebug(self.text_url)

    def Do_doc_string(self):
        """ Example:
            {
                    "query": {
                        "pages": {
                            "192203": {
                                "pageid": 192203,
                                "ns": 0,
                                "title": "Бельмондо, Жан-Поль",
                                "extract": "<p><b>Жан-Поль Бельмондо́</b> (фр.&#160;<i>Jean-Paul Belmondo</i>; род. 9 апреля 1933)&#160;— французский актёр, славу которому принесла роль аморального поклонника Хамфри Богарта в манифесте французской «новой волны»&#160;— фильме «На последнем дыхании» (1960). В первых своих картинах он создал образ юного бунтаря с неотразимой улыбкой (сродни голливудскому Джеймсу Дину) и стал предметом культового поклонения европейской молодёжи. В более зрелом возрасте переключился на острохарактерные роли в комедиях и боевиках.</p>"
                                }
                            }
                        }
                    }
        """

        PrintDebug(urllib2.quote(self.text_url.encode('utf-8')))
        jsonString = json.load(urllib.urlopen(self.text_url.encode('utf-8')))
        PrintDebug(jsonString)
        pageJson = jsonString["query"]["pages"]
        pageProps = pageJson.values()[0]
        self.doc_string = pageProps["extract"]
        PrintDebug(self.doc_string)

    def Do_doc(self):
        self.doc = pq(self.doc_string)
        PrintDebug(self.doc)

    def Do_definition_doc(self):
        self.definition = self.doc('p').html().encode('utf-8')
        PrintDebug(self.definition)

    def Do_definition_sub(self):
        #self.definition = re.sub("(<[^<>]*>|\[[^\[\]]*\])", "", self.definition)
        self.definition = re.sub("(<[^<>]*>|\[[^\[\]]*\])", "", self.doc_string)
        PrintDebug(self.definition)


    def GetDefinition(self):
        SafeExec(self.Do_term)
        SafeExec(self.Do_query_url)
        SafeExec(self.Do_page)
        #SafeExec(self.Do_text_url)
        #SafeExec(self.Do_doc_string)
        #SafeExec(self.Do_doc)
        #SafeExec(self.Do_definition_doc)
        #SafeExec(self.Do_definition_sub)
        return self.definition + u"\n" + self.completeurl 

WikiGetDefinition = TWikiGetDefinition()
print WikiGetDefinition.GetDefinition().encode('utf-8')

