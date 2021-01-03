# -*- coding: utf-8 -*-

from datetime import datetime

class Judicature(object):
    def __init__(self, data):
        """Construtor method"""
        self.dateString = '%d %b %Y %H:%M:%S'
        self.__data = data

    @property
    def title(self):
        """Get the title of this item."""
        return self.__data.find('title').text

    @property
    def description(self):
        """Get the description of this item."""
        try:  # WTF BMJV, some items do not have a description?
            return self.__data.find('description').text
        except:  # TODO: fix this
            return 'Keine Beschreibung vorhanden'

    @property
    def pubDate(self):
        """Get the formatted publication date of this item"""
        return datetime.strptime(self.__data.find('pubDate').text[:-6], self.dateString)

    @property
    def formatted(self):
        """Get a formatted string with publication date, title and description"""
        return u'{} - {} - {}'.format(self.pubDate, self.title, self.description)
