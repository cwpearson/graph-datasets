#! /usr/bin/env python

"""
Drawn an NxN visualization of the matrix sparsity
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
# have numpy raise warnings so we can silence them
np.seterr(all='warn')

FONTSIZE=14

logging.basicConfig(level=logging.INFO)
parser = argparse.ArgumentParser(description="Draw NxN visualization of matrix sparsity")
parser.add_argument('edgeListPath', type=str, help="path to edge list file")
parser.add_argument('px', type=int, help="output image size in pixels")
parser.add_argument('--kind', choices=["show", "img", "fig"], help="show figure, or save raw image or labeled figure", default="show")
parser.add_argument('-t', '--out-type', help="file type for output file")
parser.add_argument('--out-prefix', help='prefix for output file', default=os.getcwd())
parser.add_argument('-f', "--force", action="store_true", help="overwrite output file if it exists")
parser.add_argument('-s', "--skip", action="store_true", help="skip generation if the output file exists")
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
            if args.skip:
                logging.info("{} already exists (skipping because of -s)".format(outputPath))
                sys.exit(0)
            else:
                logging.error("{} already exists (use -f to overwrite)".format(outputPath))
                sys.exit(-1)
    logging.info("output will be {}".format(outputPath))



arr = np.zeros((args.px, args.px))
adj = {}
logging.info("opening {}".format(args.edgeListPath))
with edgelist(args.edgeListPath) as el:
    # find the max non-zero index
    maxI = 0
    for src, dst in el:
        maxI = max(maxI, dst, src)
    maxI += 1
    logging.info("max nz idx = {}".format(maxI))

    # insert each edge into image
    for src, dst in el:
        if (src < dst):
            i = int(src * args.px / maxI)
            j = int(dst * args.px / maxI)
            arr[i][j] += 1
    logging.info("inserted edges")

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
im = ax.imshow(arr, cmap="Greys")

ax.xaxis.tick_top()
ax.set_xlabel('j * {} / {}'.format(args.px, maxI), fontsize=FONTSIZE)
ax.set_ylabel('i * {} / {}'.format(args.px, maxI), fontsize=FONTSIZE)
ax.set_title('{} {}x{}'.format(os.path.basename(args.edgeListPath), args.px, args.px), fontsize=FONTSIZE, pad=30)


cbar = plt.colorbar(im)
cbar.ax.set_ylabel("log2 NNZ count", fontsize=FONTSIZE)


fig.tight_layout()
if args.kind == "fig":
    plt.savefig(outputPath)
else:
    plt.show()