# -*- coding: utf-8 -*-

from obelixtools import API
from .Judicature import Judicature
import time
import logging
import csv

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
        """Construtor method"""
        self.id = id
        self.feed = self.selectCourt()
        self.dateString = '%a, %d %b %Y %H:%M:%S GMT'
        self.items = []
        self.__logger = logging.getLogger('BMJV.RechtsprechungImInternet')
        return

    @property
    def id(self):
        """Get the ID of this item"""
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value if value else 'bverfg'

    def selectCourt(self):
        """Select the court to filter the results."""
        if self.id in self.URLS:
            return API(url=self.URLS[self.id], format='xml')
        else:
            return False

    def fetch(self, limit=0):
        """Fetch the data from the data source"""
        self.feed.query()
        self.items = []
        for entry in self.feed.content[0].findall('item'):
            self.items.append(Judicature(entry))
        self.items = sorted(self.items, key=lambda law: law.pubDate)
        if limit:
            self.items = self.items[:limit]
        self.lastRefresh = time.time()
        self.__logger.info('Found a total of {} results for {}'.format(len(self.items), self.id))

    def export_csv(self, filename=False):
        """Export the data as CSV file"""
        filename = filename or '{}_export.csv'.format(self.id)
        fields = ['title','description','pubDate']
        self.__logger.info('Export data to {}'.format(filename))
        with open(filename, 'w', encoding='UTF-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(fields)
            for item in self.items:
                writer.writerow([getattr(item, key) for key in fields])
        self.__logger.debug('Wrote a total of {} lines to {}'.format(len(self.items), filename))
