# graph-datasets

A list of graph datasets, and tools to acquire and analyze them

Eventually, we could like to support
* [GraphChallenge](https://graphchallenge.mit.edu/data-sets)
* [Stanford Large Network Datasets (SNAP)](https://snap.stanford.edu/data/index.html
)
* [SuiteSparse](sparse.tamu.edu)
* [Web Data Commons - Hyperlink Graphs](webdatacommons.org/hyperlinkgraph)

## Tools

All tools require Python 3. If `python tool.py -h` causes an error, check your Python version.

### download.py

Download datasets.

`python tools/download.py -h` for more info.

### convert.py

Convert between data formats.
Especially from an ASCII to binary format.

`python tools/convert.py -h` for more info.

### hist-nbrs.py

Create a 2d histogram of edges binned by neighbor list lenghts.

### hist-id.py

Create a 2d histogram of edges binned by src/dst node IDs.

## Examples

Download graph data
```
$ python3 ~/repos/graph-datasets/tools/download.py --name scale18
MD5_MATCH ./graph500-scale18-ef16_adj.tsv.gz
EXTRACT_MATCH ./graph500-scale18-ef16_adj.tsv
```

Convert all tsv files to bel in parallel, skipping (with 0 exit) for existing bel files
```bash
$ for t in *.tsv; do python3 ~/repos/graph-datasets/tools/convert.py $t bel -s &; done
```

## Data Formats

### tsv

Tab-separated lines of integer `dst src weight`

### bel

Packed 8-byte little-endian integers of `dst` `src` `weight`.

the binary format is for each edge
* 64-bit integer dst
* 64-bit integer src
* 64-bit integer weight
all numbers are stored little endian (least significant byte first)

the number of edges is the byte-length of the file divided by 24

you can view the produced file with 
`xxd -c 24 <file>` to see one edge per line

## GraphChallenge

Includes GenBank 

