# -*- coding: utf-8 -*-

from obelixtools import API
from .Law import Law
import time
import logging

class BGBl(object):
    def __init__(self, url=False):
        """Constructor method"""
        self.url = url or 'https://www.gesetze-im-internet.de/aktuDienst-rss-feed.xml'
        self.feed = API(url=self.url, format='xml')
        self.__logger = logging.getLogger('BMJV.BGBl')

    def fetch(self, limit=0):
        """Fetch items from the datasource.
        """
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
        """Get the formatted string for this item
        """
        return u'{} - {} - {}'.format(self.pubDate, self.title, self.description)
