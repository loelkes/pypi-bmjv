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
import argparse
from BMJV import *

if __name__ == '__main__':
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['bgbl', 'rim'], help='Seth mode.')
    parser.add_argument('--court', type=str, default='bverfg', help='Select a court. Only relevant if in rim mode.')
    parser.add_argument('--limit', type=int, default=0, help='Limit the number of results.')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    if args.mode == 'rim':
        rim = RechtsprechungImInternet(args.court)
        rim.fetch(args.limit)
        for item in rim.items:
            logger.info(item.formatted)

    elif args.mode == 'bgbl':
        gim = BGBl()
        gim.fetch(args.limit)
        for item in gim.items:
            logger.info(item.formatted)
