"""the webgraph download subcommand"""

from datasets import Webgraph


def webgraph(args):
    dst = args.out

    w = Webgraph(dst)
    w.fetch_gzs()
    w.extract_gzs()
