#! /usr/bin/env python

'''
'''

from __future__ import print_function
import sys
import struct
import os
import argparse
import logging
from util.edgelist import edgelist

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("file", help="input file")
parser.add_argument("to", choices=["bel", "tsv"], help="convert to this output type")
parser.add_argument('-f', "--force", action="store_true", help="overwrite output file")
parser.add_argument('-s', "--skip", action="store_true", help="skip converting files where the output already exists")
parser.add_argument("--out-prefix", type=str, help="prefix for converted files", default="")
args = parser.parse_args()

# create / check output path
outputPath = None

inBaseName, _ = os.path.splitext(os.path.basename(args.file))
outputPath = os.path.join(args.out_prefix, inBaseName+"."+args.to)
if not args.force:
    if os.path.exists(outputPath):
        if args.skip:
            logging.info("{} already exists (skipping because of -s)".format(outputPath))
            sys.exit(0)
        logging.error("{} already exists (use -f to overwrite)".format(outputPath))
        sys.exit(-1)
logging.info("output will be {}".format(outputPath))


# don't overwrite input during output
if os.path.abspath(args.file) == os.path.abspath(outputPath):
    logging.error("{} and {} are the same file".format(args.file, outputPath))
    sys.exit(-1)

logging.info("convert {} -> {}".format(args.file, outputPath))
with edgelist(args.file) as inf, edgelist(outputPath) as outf:
    for edge in inf:
        outf.write(edge)

