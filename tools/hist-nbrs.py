#! /usr/bin/env python
"""

"""



from __future__ import print_function
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import argparse
from util.edgelist import edgelist
import logging
import warnings
import imageio
import os
import sys
import math
from collections import defaultdict
# have numpy raise warnings so we can silence them
np.seterr(all='warn')

FONTSIZE=14

logging.basicConfig(level=logging.INFO)
parser = argparse.ArgumentParser(description="Draw NxN visualization of matrix sparsity")
parser.add_argument('edgeListPath', type=str, help="path to edge list file")
parser.add_argument('-k', '--kind', choices=["show", "img", "fig"], help="show figure, or save raw image or labeled figure", default="show")
parser.add_argument('-t', '--out-type', help="file type for output file")
parser.add_argument('--out-prefix', help='prefix for output file', default=os.getcwd())
parser.add_argument('-f', "--force", action="store_true", help="overwrite output file if it exists")
args = parser.parse_args()

# choose output type by figure vs img
if args.kind == "img" and not args.out_type:
    args.out_type="png"
if args.kind == "fig" and not args.out_type:
    args.out_type="pdf"

# create / check output path
outputPath = None
if args.kind != "show":
    outputPath = args.out_prefix
    elBaseName, _ = os.path.splitext(os.path.basename(args.edgeListPath))
    outputPath = os.path.join(args.out_prefix, elBaseName+"."+args.out_type)
    if not args.force:
        if os.path.exists(outputPath):
            logging.error("{} already exists (use -f to overwrite)".format(outputPath))
            sys.exit(-1)
    logging.info("output will be {}".format(outputPath))



nbrLengths = defaultdict(int)

logging.info("opening {}".format(args.edgeListPath))
with edgelist(args.edgeListPath) as el:
    # find the length of each edge
    logging.info("determine neighbor list lengths")
    for src, dst in el:
        if src < dst:
            nbrLengths[src] += 1

    # compute the maximum bin size
    maxLen = max(nbrLengths.values())
    logging.info("maxLen: {}".format(maxLen))
    maxBin = math.log2(maxLen)
    maxBin = int(maxBin)+2
    logging.info("maxBin: {}".format(maxBin))

    arr = np.zeros((maxBin, maxBin))

    # histogram the edges
    logging.info("binning edges")
    for src, dst in el:
        if src < dst:
            srcLen = nbrLengths[src]
            dstLen = nbrLengths[dst]
            # 0 -> bin 0 (<1)
            # 1 -> bin 1 (<2)
            # 2 -> bin 2 (<4)
            # 3 -> bin 2 (<4)
            # 4 -> bin 3 (<8)
            if srcLen != 0:
                srcBin = int(math.log2(srcLen))+1
            else:
                srcBin = 0
            if dstLen != 0:
                dstBin = int(math.log2(dstLen))+1
            else:
                dstBin = 0
            arr[srcBin][dstBin] += 1

# scale counts by log for visualization purposes
logging.info("scale")
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    arr = np.where(arr > 0, np.log2(arr), 0)

# save image and quit
if args.kind == "img":
    arr = arr * 255.0 / np.max(arr)
    arr = 255 - arr
    arr = arr.astype(np.uint8)
    imageio.imwrite(outputPath, arr)
    sys.exit(0)

# create figure
fig, ax = plt.subplots()
im = ax.imshow(arr, cmap="viridis")

ax.xaxis.tick_top()
ax.set_xlabel('log2 |N(j)|', fontsize=FONTSIZE)
ax.set_ylabel('log2 |N(i)|', fontsize=FONTSIZE)
ax.set_title('E(i,j) Counts by Neighbor List Length', fontsize=FONTSIZE, pad=30)


cbar = plt.colorbar(im)
cbar.ax.set_ylabel("log2 NZ count", fontsize=FONTSIZE)


fig.tight_layout()
if args.kind == "fig":
    plt.savefig(outputPath)
else:
    plt.show()

