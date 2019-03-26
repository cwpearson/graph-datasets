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
parser = argparse.ArgumentParser(description="partition edge list file")
parser.add_argument('path', type=str, help="graph file")
parser.add_argument('rows', type=int, help="number of partitions")
parser.add_argument('-o', '--out-dir', type=str, default="", help="output directory")
parser.add_argument('-f', '--force', action='store_true', help="overwrite existing output files")
args = parser.parse_args()

def block_overwrite(path):
    if os.path.exists(path):
        if args.force:
            logging.warn("overwriting {}".format(path))
        else:
            logging.error("{} exists (-f to overwrite)".format(path))
            sys.exit(1)

def upper_triangular(edge):
    return edge[0] < edge[1]

def lower_triangular(edge):
    return edge[1] < edge[0]

with edgelist(args.path) as el:
    # find the max node id
    maxID = max(max(src, dst) for src, dst in el)
    logging.info("max node ID is {}".format(maxID))

    ## create one partition file for each pair of partitions

    edgelists = [[None for j in range(args.rows)]for i in range(args.rows)]
    csrs = [[None for j in range(args.rows)]for i in range(args.rows)]
    for i in range(args.rows):
        for j in range(args.rows):

            # construct output file names
            infdir, infbase, infext = util.path.split(args.path)
            edgesBase = infbase + "_edges_{}-{}".format(i,j)
            csrBase = infbase + "_csr_{}-{}".format(i,j)
            edgesFilePath = os.path.join(args.out_dir, edgesBase +infext)
            csrFilePath = os.path.join(args.out_dir, csrBase +infext)
            logging.info(edgesFilePath)
            block_overwrite(edgesFilePath)
            logging.info(csrFilePath)
            block_overwrite(csrFilePath)
            edgelists[i][j] = edgelist(edgesFilePath)
            csrs[i][j] = edgelist(csrFilePath)

            # figure out the ranges that will be present in this partition
            def part_range(i):
                partSz = ((maxID // args.rows) + 1)
                partStart = partSz * i
                partEnd = partSz * (i + 1)
                return partStart, partEnd
            iBegin, iEnd = part_range(i)
            jBegin, jEnd = part_range(j)
            logging.info("triangle edges from [{}, {}) -> [{}, {})".format(iBegin, iEnd, jBegin, jEnd))
            logging.info("csr edges from [{}, {}) -> [all] and [{}, {}) -> [all]".format(iBegin, iEnd, jBegin, jEnd))

            # add corresponding edges to this partition
            numCsr = 0
            numEl = 0
            for edge in el:
                src, dst = edge
                if (src >= iBegin and src < iEnd) or (src >= jBegin and src < jEnd):
                    csrs[i][j].write(edge)
                    numCsr += 1
                if (src >= iBegin and src < iEnd) and (dst >= jBegin and dst < jEnd):
                    edgelists[i][j].write(edge)
                    numEl += 1
            logging.info("included {} edges and {} csr nzs".format(numEl, numCsr))

