'''example'''

from __future__ import print_function

import logging
import numpy as np
from argparse import ArgumentParser
import sys
from time import time
import os.path

from preprocess import preprocess

################################################################################
# logging and options
################################################################################

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

parser = ArgumentParser()
parser.add_argument('fpath', type=str, action='store',
                    help='the name of the folder containing the text files')
parser.add_argument('--cols', type=int, nargs='+', action='store',
                    help='the columns to extract from the data file to use as features')

args = parser.parse_args()

if not os.path.exists(args.fpath):
    if 'data/' in args.fpath:
        parser.error('The file %s does not exist' % args.fpath)
        sys.exit(1)
    else:
        # try appending data
        args.fpath = 'data/' + args.fpath
        if not os.path.exists(args.fpath):
            parser.error('The file %s does not exist' % args.fpath)
            sys.exit(1)

if len(args.cols) == 0:
    parser.error('Please specify the columns you wish to parse')
    sys.exit(1)

print(__doc__)
parser.print_help()
print()

if __name__ == '__main__':
    print('file path: %s' % args.fpath)
    print('columns:')
    print(args.cols)
    print()

    data = preprocess(args.fpath, args.cols)

    print('Shape of data:')
    print(data.shape)
