'''preprocessing data
To preprocess a csv, just run `python name_of_csv.csv output_pickle_name.pkl`'''
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
parser.add_argument('source_path', type=str, action='store',
                    help='the path to the csv file')
parser.add_argument('dest_name', type=str, action='store',
                    help='the name to save the pickled object as')

#parser.add_argument('--cols', type=int, nargs='+', action='store',
#                    help='the columns to extract from the csv file to use as features')

args = parser.parse_args()

if not os.path.exists(args.source_path):
    if 'data/' in args.source_path:
        parser.error('The file %s does not exist' % args.source_path)
        sys.exit(1)
    else:
        # try appending data/
        args.source_path = 'data/' + args.source_path
        if not os.path.exists(args.source_path):
            parser.error('The file %s does not exist' % args.source_path)
            sys.exit(1)
'''
if len(args.cols) == 0:
    parser.error('Please specify the columns you wish to parse')
    sys.exit(1)
'''

print(__doc__)
parser.print_help()
print()

if __name__ == '__main__':
    print('file path: %s' % args.source_path)

    preprocess(args.source_path, args.dest_name)
