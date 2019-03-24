#! /usr/bin/env python

"""
Draw an NxN visualization of the edge list

"""


from __future__ import print_function
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import struct
import os
import mmap


FONTSIZE=14

bel_path = sys.argv[1]
px = int(sys.argv[2])

assert bel_path.endswith(".bel")
assert os.path.getsize(bel_path) % 24 == 0

arr = np.zeros((px, px))

adj = {}
with open(bel_path, 'r+') as inf:
    mf = mmap.mmap(inf.fileno(), 0)

    # find the max non-zero index
    maxI = 0
    for i in range(0, len(mf), 24):
        dst,src = struct.unpack("<QQ", mf[i:i+16])
        maxI = max(maxI, dst, src)
    maxI += 1
    print("max nz idx = {}".format(maxI))

    # insert each edge into image
    for i in range(0, len(mf), 24):
        dst,src = struct.unpack("<QQ", mf[i:i+16])
        if (src < dst):
            i = int(src * px / maxI)
            j = int(dst * px / maxI)
            arr[i][j] += 1

# scale counts by log for visualization purposes
arr = np.where(arr > 0, np.log2(arr), 0)

fig, ax = plt.subplots()
im = ax.imshow(arr, cmap="Greys")

ax.xaxis.tick_top()
ax.set_xlabel('j * {} / {}'.format(px, maxI), fontsize=FONTSIZE)
ax.set_ylabel('i * {} / {}'.format(px, maxI), fontsize=FONTSIZE)
ax.set_title('{} {}x{}'.format(os.path.basename(bel_path), px, px), fontsize=FONTSIZE, pad=30)


cbar = plt.colorbar(im)
cbar.ax.set_ylabel("log2 NNZ count", fontsize=FONTSIZE)


fig.tight_layout()
plt.show()