# -*- coding: utf-8 -*-

from datetime import datetime
from obelixtools import API
import logging, time

logger = logging.getLogger(__name__)

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

class Law(object):
    def __init__(self, data):
        self.dateString = '%a, %d %b %Y %H:%M:%S GMT'
        self.parse(data)
        return

    def parse(self, data):
        self.title = data.find('title').text
        self.description = data.find('description').text
        self.link = data.find('link').text
        self.guid = data.find('guid').text
        self.pubDate = datetime.strptime(data.find('pubDate').text, self.dateString)
        return

    @property
    def formatted(self):
        return u'{} - {} - {}'.format(self.pubDate, self.title, self.description)

class Judicature(object):
    def __init__(self, data):
        self.dateString = '%d %b %Y %H:%M:%S'
        self.parse(data)
        return

    def parse(self, data):
        self.title = data.find('title').text
        try: # WTF BMJV, some items do not have a description?
            self.description = data.find('description').text
        except:
            self.description = 'Keine Beschreibung vorhanden'
            # TODO: Better Parsing of Datetime string possible?
        self.pubDate = datetime.strptime(data.find('pubDate').text[:-6], self.dateString)
        return

    @property
    def formatted(self):
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
    def __init__(self, id='bverfg'):
        self.id = id
        self.feed = self.selectCourt()
        self.dateString = '%a, %d %b %Y %H:%M:%S GMT'
        self.items = []
        return

    def selectCourt(self):
        if self.id in URLS:
            return API(url=URLS[self.id], format='xml')
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

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger.info('Script is executed as standalone file.')

    logger.info('Fetching information from all court endoints...')
    for id, url in URLS.items():
        rim = RechtsprechungImInternet(id)
        rim.fetch(2)
        for item in rim.items:
            logger.info(item.formatted[:100] + '...')

    logger.info('Fetching information from legistation endoint...')
    gim = BGBl()
    gim.fetch(2)
    for item in gim.items:
        logger.info(item.formatted[:100] + '...')
