#!/usr/bin/env python
# -*- coding: utf-8 -*-
import feedparser
from HTMLParser import HTMLParser

WORLD_NEWS_URL = "http://news.yandex.ru/world.rss"

for entry in feedparser.parse(WORLD_NEWS_URL)['entries'][0:3]:
    print HTMLParser().unescape(entry['summary_detail']['value']).encode('utf-8')

