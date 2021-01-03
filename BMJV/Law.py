# -*- coding: utf-8 -*-

from datetime import datetime


class Law(object):
    def __init__(self, data):
        """Constructor method"""
        self.dateString = '%a, %d %b %Y %H:%M:%S GMT'
        self.__data = data
        return

    @property
    def title(self):
        """Get the item of this item"""
        return self.__data.find('title').text

    @property
    def description(self):
        """Get the description of this item"""
        return self.__data.find('description').text

    @property
    def link(self):
        """Get the resource link of this item"""
        return self.__data.find('link').text

    @property
    def guid(self):
        """Get the GUID of this item"""
        return self.__data.find('guid').text

    @property
    def pubDate(self):
        """Get the formatted publication date of this item"""
        return datetime.strptime(self.__data.find('pubDate').text, self.dateString)

    @property
    def formatted(self):
        """Get a formatted string with publication date, title and description."""
        return u'{} - {} - {}'.format(self.pubDate, self.title, self.description)
