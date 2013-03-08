#!/usr/bin/env python
# -*- coding: utf-8 -*-
import feedparser
from HTMLParser import HTMLParser
from pprint import pprint

WEATHER_FEED_URL = "http://meteoinfo.ru/rss/moscow/"

entry = feedparser.parse(WEATHER_FEED_URL)['entries'][0]
print(entry['summary'].encode('utf-8'))