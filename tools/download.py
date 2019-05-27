"""
Download datasets
"""

import argparse
import sys

from util.datasets import GRAPH_CHALLENGE
from cmds.webgraph import webgraph
from cmds.graph_challenge import graphchallenge


parser = argparse.ArgumentParser()
parser.add_argument("--out", default=".", help="output dir")
parser.set_defaults(func=lambda x: parser.print_help())


subparsers = parser.add_subparsers()

parser_webgraph = subparsers.add_parser(
    'webgraph', help="download webgraph dataset")
parser_webgraph.set_defaults(func=webgraph)

parser_graph_challenge = subparsers.add_parser(
    'gc', help="download graph challenge datset")
parser_graph_challenge.add_argument(
    "--name", help="only download graphs with NAME in URL")
parser_graph_challenge.add_argument("--list", action="store_true",
                                    help="print matching graphs, do not download")
parser_graph_challenge.set_defaults(func=graphchallenge)

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()
args.func(args)
