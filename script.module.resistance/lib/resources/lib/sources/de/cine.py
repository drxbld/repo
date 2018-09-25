# -*- coding: UTF-8 -*-
#           ________
#          _,.-Y  |  |  Y-._
#      .-~"   ||  |  |  |   "-.
#      I" ""=="|" !""! "|"[]""|     _____
#      L__  [] |..------|:   _[----I" .-{"-.
#     I___|  ..| l______|l_ [__L]_[I_/r(=}=-P
#    [L______L_[________]______j~  '-=c_]/=-^
#     \_I_j.--.\==I|I==_/.--L_]
#       [_((==)[`-----"](==)j
#          I--I"~~"""~~"I--I
#          |[]|         |[]|
#          l__j         l__j
#         |!!|         |!!|
#          |..|         |..|
#          ([])         ([])
#          ]--[         ]--[
#          [_L]         [_L]
#         /|..|\       /|..|\
#        `=}--{='     `=}--{='
#       .-^--r-^-.   .-^--r-^-.
# Resistance is futile @lock_down... 

import json
import re
import urllib
import urlparse

from resources.lib.modules import client
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['cine.to']
        self.base_link = 'https://cine.to'
        self.request_link = '/request/links'
        self.out_link = '/out/%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            return urllib.urlencode({'imdb': imdb})
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if url == None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            data = urllib.urlencode({'ID': re.sub('[^0-9]', '', str(data['imdb'])), 'lang': 'de'})

            data = client.request(urlparse.urljoin(self.base_link, self.request_link), post=data, XHR=True)
            data = json.loads(data)
            data = [(i, data['links'][i]) for i in data['links'] if 'links' in data]
            data = [(i[0], i[1][0], (i[1][1:])) for i in data]

            for hoster, quli, links in data:
                valid, hoster = source_utils.is_host_valid(hoster, hostDict)
                if not valid: continue

                for link in links:
                    try: sources.append({'source': hoster, 'quality': 'SD', 'language': 'de', 'url': self.out_link % link, 'direct': False, 'debridonly': False})
                    except: pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            url = urlparse.urljoin(self.base_link, url)
            url = client.request(url, output='geturl')
            if self.out_link not in url:
                return url
        except:
            return
