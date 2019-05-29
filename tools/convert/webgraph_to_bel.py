"""the convert webgraph subcommand"""

import pathlib
import collections
import pickle

from datasets import Webgraph
from utils.edgelist import TSV


def webgraph_to_bel(src, dst, force):

    # ensure that src is a webgraph dataset
    canary_path = src / ".webgraph"
    if not canary_path.exists():
        print(f"{canary_path} does not exist")
        sys.exit(1)

    if dst.exists() and not args.force:
        print(f"{dst} exists (-f to overwrite)")
        sys.exit(2)

    # figure out which nodes are referenced in each arc file
    node_files = collections.defaultdict([])
    for arc_path in dst.iterdir():
        if "part-r-" not in arc_path.name or arc_path.suffix == ".gz":
            continue
        with open(arc_path, "r") as arc_file:
            try:
                for line in arc_file:
                    src_node, dst_node = map(int, line.split())
                node_files[src_node] += [arc_path]
                node_files[dst_node] += [arc_path]
            except KeyboardInterrupt:
                with open("arc_index", "wb") as f:
                pickle.dump(node_files, f)
                raise
        break  # try one to debug

    # dump to carry on later
    with open("arc_index", "wb") as f:
        pickle.dump(node_files, f)

    # find all the srcs that point to each dst
    bel_file = TSV(dst)
    for node, paths in sorted(node_files):
        src_nodes = []
        print(node)
        for path in paths:
            with open(path, "r") as arc_file:
                for line in arc_file:
                    src_node, dst_node = map(int, line.split())
                    if dst_node == node:
                        src_nodes += [src_node]
        src_nodes = sorted(src_nodes)
        with open(dst, "ab") as f:
            for src_node in src_nodes:
                bel_file.write((src_node, node))

    w = Webgraph(dst)
    w.fetch_gzs()
    w.extract_gzs()
