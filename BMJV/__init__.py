# coding=utf-8

# Copyright 2019 Christian Lölkes

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import datetime
from obelixtools import API
import logging, time

logger = logging.getLogger(__name__)

class Law(object):
    def __init__(self, data):
        self.dateString = '%a, %d %b %Y %H:%M:%S GMT'
        self.__data = data
        return

    @property
    def title(self):
        return self.__data.find('title').text

    @property
    def description(self):
        return self.__data.find('description').text

    @property
    def link(self):
        return self.__data.find('link').text

    @property
    def guid(self):
        return self.__data.find('guid').text

    @property
    def pubDate(self):
        return datetime.strptime(self.__data.find('pubDate').text, self.dateString)

    @property
    def formatted(self):
        """Returns a formatted string with publication date, title and description."""
        return u'{} - {} - {}'.format(self.pubDate, self.title, self.description)

class Judicature(object):
    def __init__(self, data):
        self.dateString = '%d %b %Y %H:%M:%S'
        self.__data = data

    @property
    def title(self):
        return self.__data.find('title').text

    @property
    def description(self):
        try: # WTF BMJV, some items do not have a description?
            return self.__data.find('description').text
        except:
            return 'Keine Beschreibung vorhanden'

    @property
    def pubDate(self):
        return datetime.strptime(self.__data.find('pubDate').text[:-6], self.dateString)

    @property
    def formatted(self):
        """Returns a formatted string with publication date, title and description"""
        return u'{} - {} - {}'.format(self.pubDate, self.title, self.description)

class BGBl(object):
    def __init__(self, url=False):
        self.url = url or 'https://www.gesetze-im-internet.de/aktuDienst-rss-feed.xml'
        self.feed = API(url=self.url, format='xml')

    def fetch(self, limit=0):
        self.feed.query()
        self.items = []
        for item in self.feed.content[0].findall('item'):
            self.items.append(Law(item))
        self.items = sorted(self.items, key=lambda item: item.pubDate)
        if limit:
            self.items = self.items[:limit]
        self.lastRefresh = time.time()

    @property
    def formatted(self):
        return u'{} - {} - {}'.format(self.pubDate, self.title, self.description)


class RechtsprechungImInternet(object):

    URLS = {
        # Rechtssprechung des Bundesverfassungsgerichts
        'bverfg': 'https://www.rechtsprechung-im-internet.de/jportal/docs/feed/bsjrs-bverfg.xml',
        # Rechtsprechung des Bundesgerichtshofs
        'bgh': 'https://www.rechtsprechung-im-internet.de/jportal/docs/feed/bsjrs-bgh.xml',
        # Rechtsprechung des Bundesverwaltungsgerichts
        'bverwg': 'https://www.rechtsprechung-im-internet.de/jportal/docs/feed/bsjrs-bverwg.xml',
        # Rechtsprechung des Bundesfinanzhofs
        'bfh': 'https://www.rechtsprechung-im-internet.de/jportal/docs/feed/bsjrs-bfh.xml',
        # Rechtssprechung des Bundesarbeitsgerichts
        'bag': 'https://www.rechtsprechung-im-internet.de/jportal/docs/feed/bsjrs-bag.xml',
        # Rechtssprechung des Bundessoszialgerichts
        'bsg': 'https://www.rechtsprechung-im-internet.de/jportal/docs/feed/bsjrs-bsg.xml',
        # Rechtssprechung des Bundespatengerichts
        'bpatg': 'https://www.rechtsprechung-im-internet.de/jportal/docs/feed/bsjrs-bpatg.xml'
    }

    def __init__(self, id):
        self.id = id
        self.feed = self.selectCourt()
        self.dateString = '%a, %d %b %Y %H:%M:%S GMT'
        self.items = []
        return

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value if value else 'bverfg'

    def selectCourt(self):
        if self.id in self.URLS:
            return API(url=self.URLS[self.id], format='xml')
        else:
            return False

    def fetch(self, limit=0):
        self.feed.query()
        self.items = []
        for entry in self.feed.content[0].findall('item'):
            self.items.append(Judicature(entry))
        self.items = sorted(self.items, key=lambda law: law.pubDate)
        if limit:
            self.items = self.items[:limit]
        self.lastRefresh = time.time()
        logger.info('Found a total of {} results for {}'.format(len(self.items), self.id))
