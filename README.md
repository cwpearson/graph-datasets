# graph-datasets

A list of graph datasets, and tools to acquire and analyze them.

Some information about the datasets may be present at https://graphchallenge-datasets.netlify.com/


## Tools

All tools require Python 3. If `python tool.py -h` causes an error, check your Python version.

```
python --version
```

or possibly

```
python3 --version
```

### download.py

Download datasets.

`python tools/download.py -h` for more info.

This will download and extract graph files.
All supported files are so far in the tsv format (described below).

### convert.py

Convert between data formats.
Especially from an ASCII to binary format.

`python tools/convert.py -h` for more info.

### hist-nbrs.py

Create a 2d histogram of edges binned by neighbor list lenghts.

### hist-id.py

Create a 2d histogram of edges binned by src/dst node IDs.

### partition.py

`python tools/rows.py <file> --rows N`

Partition a graph into NxN partitions consisting of roughly ` 2 * num_rows / N` rows each.

The partition strategy is to partition the nodes into N sets.
Then, edges with a source in both node paritions are included.
Edges for each of the NxN source/dst node parition pairs is placed into a separate file.
Only the edges that go from one partition to the other in each file should be counted, there are also additional edges to ensure that the count is correct.

## Examples

Download graph data.
`DOWNLOAD` means that a file was downloaded, and a reason is provided.
`MD5_MATCH` means that a file with the same name and MD5 was already discovered in the output directory.
`EXTRACT_MATCH` means that an extracted file of the correct size was already discovered in the output directory.
```
$ python3 ~/repos/graph-datasets/tools/download.py --name scale18
MD5_MATCH ./graph500-scale18-ef16_adj.tsv.gz
EXTRACT_MATCH ./graph500-scale18-ef16_adj.tsv
```

Convert all `tsv` files to `bel` in parallel, skipping (with 0 exit) existing bel files
```bash
$ for t in *.tsv; do python3 ~/repos/graph-datasets/tools/convert.py $t bel -s &; done
```

Generate statistics for all `bel` files
```
$ python3 ~/repos/graph-datasets/tools/stats.py *.bel
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

## Wishlist


- [x] [GraphChallenge](https://graphchallenge.mit.edu/data-sets)
- [ ] [Stanford Large Network Datasets (SNAP)](https://snap.stanford.edu/data/index.html)
- [ ] [SuiteSparse](sparse.tamu.edu)
- [ ] [Web Data Commons - Hyperlink Graphs](webdatacommons.org/hyperlinkgraph)

