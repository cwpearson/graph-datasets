#! /usr/bin/env python

"""
Partiton 
"""

from __future__ import print_function
import sys
import logging
from util.edgelist import edgelist
from collections import defaultdict
import argparse
import util.path
import os

logging.basicConfig(level=logging.INFO)
parser = argparse.ArgumentParser(description="Print some graph statistics")
parser.add_argument('path', type=str, help="graph file")
parser.add_argument('-r', '--rows', type=int, help="create row-wise partitions")
parser.add_argument('-o', '--out-dir', type=str, default="", help="output directory")
parser.add_argument('-f', '--force', action='store_true', help="overwrite existing output files")
args = parser.parse_args()

def upper_triangular(edge):
    return edge[0] < edge[1]

def lower_triangular(edge):
    return edge[1] < edge[0]

with edgelist(args.path) as el:
    # find the max node id
    maxID = max(max(src, dst) for src, dst in el)
    logging.info("max node ID is {}".format(maxID))

    ## create one partition file for each pair of partitions

    partELs = [[None for j in range(args.rows)]for i in range(args.rows)]
    for i in range(args.rows):
        for j in range(args.rows):

            # construct output file name
            infdir, infbase, infext = util.path.split(args.path)
            partBase = infbase + "_{}-{}".format(i,j)
            partFilePath = os.path.join(args.out_dir, partBase +infext)
            logging.info(partFilePath)
            if os.path.exists(partFilePath):
                if args.force:
                    logging.warn("overwriting {}".format(partFilePath))
                else:
                    logging.error("{} exists (-f to overwrite)".format(partFilePath))
                    sys.exit(1)
            partELs[i][j] = edgelist(partFilePath)

            # figure out the ranges that will be present in this partition
            def part_range(i):
                partSz = ((maxID // args.rows) + 1)
                partStart = partSz * i
                partEnd = partSz * (i + 1)
                return partStart, partEnd
            iBegin, iEnd = part_range(i)
            jBegin, jEnd = part_range(j)
            logging.info("[{}, {}) -> [{}, {})".format(iBegin, iEnd, jBegin, jEnd))

            # add corresponding edges to this partition
            inc = 0
            exc = 0
            for edge in el:
                src, _ = edge
                if (src >= iBegin and src < iEnd) or (src >= jBegin and src < jEnd):
                    partELs[i][j].write(edge)
                    inc += 1
                else:
                    exc += 1
            logging.info("included {}/{} edges".format(inc, inc+exc))

