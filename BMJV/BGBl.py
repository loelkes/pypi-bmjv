# -*- coding: utf-8 -*-

from obelixtools import API
from .Law import Law
import time
import logging
import csv

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

    def export_csv(self, filename=False):
        """Export the data as CSV file"""
        filename = filename or 'BGBl_export.csv'
        self.__logger.info('Export data to {}'.format(filename))
        fields = ['title', 'description', 'link', 'guid', 'pubDate']
        with open(filename, 'w', encoding='UTF-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(fields)
            for item in self.items:
                writer.writerow([getattr(item, key) for key in fields])
        self.__logger.debug('Wrote a total of {} lines to {}'.format(len(self.items), filename))
