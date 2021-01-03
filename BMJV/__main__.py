"""Retrieve Data from the BMJV

Usage:
  BMJV [options]
  BMJV [--mode <mode>] [--court <court>] [--loglevel LEVEL] [--limit <limit>] [--export-csv]
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
  --export-csv          Export the data as a CSV file

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
from .RechtsprechungImInternet import RechtsprechungImInternet
from .BGBl import BGBl

if __name__ == '__main__':
    logger = logging.getLogger('BMJV')
    if arguments['--list-courts']:
        logger.info('The follwing IDs are available for --court')
        for id, link in RechtsprechungImInternet.URLS.items():
            logger.info('{} - {}'.format(id, link))
    elif arguments['--mode'] == 'rim':
        rim = RechtsprechungImInternet(arguments['--court'])
        rim.fetch(int(arguments['--limit']))
        if arguments['--export-csv']:
            rim.export_csv()
        else:
            for item in rim.items:
                logger.info(item.formatted)
    elif arguments['--mode'] == 'bgbl':
        gim = BGBl()
        gim.fetch(int(arguments['--limit']))
        if arguments['--export-csv']:
            gim.export_csv()
        else:
            for item in gim.items:
                logger.info(item.formatted)
