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

"""Retrieve Data from the BMJV

Usage:
  BMJV [options]
  BMJV [--mode <mode>] [--court <court>] [--loglevel LEVEL] [--limit <limit>]
  BMJV (-h | --help | -v | --version)

Options:
  -h --help           Show this screen
  -v --version        Show version
  --loglevel LEVEL    Set a specific log level [default: INFO]

Data options:
  --court <court>       Select a specific court [default: bverfg]
  --mode <mode>         Select a data source [default: rim]
  --limit <limit>       Limit the amount fo results to diplay [default: 0]
  --list-courts         Show all available courts

"""

VERSION = '1.2.0'

### docopt ###
from docopt import docopt
arguments = docopt(__doc__, version=VERSION)

### Logging ###
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    level=getattr(logging, arguments['--loglevel'])
)

from datetime import datetime
from obelixtools import API
import time
from BMJV import *

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    if arguments['--list-courts']:
        logger.info('The follwing IDs are available for --court')
        for id, link in RechtsprechungImInternet.URLS.items():
            logger.info('{} - {}'.format(id, link))
    elif arguments['--mode'] == 'rim':
        rim = RechtsprechungImInternet(arguments['--court'])
        rim.fetch(int(arguments['--limit']))
        for item in rim.items:
            logger.info(item.formatted)
    elif arguments['--mode'] == 'bgbl':
        gim = BGBl()
        gim.fetch(int(arguments['--limit']))
        for item in gim.items:
            logger.info(item.formatted)
