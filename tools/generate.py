'''
'''

import sys
import argparse
import logging
import pathlib
from generator import RandomUT

logging.basicConfig(level=logging.INFO)


def generate_random_ut(args):
    out_path = pathlib.Path(args.out)
    num_rows = int(args.num_rows)
    num_edges = int(args.num_edges)
    g = RandomUT(num_rows, num_edges)
    g.write(out_path)


parser = argparse.ArgumentParser()
parser.set_defaults(func=lambda x: parser.print_help())


subparsers = parser.add_subparsers()

parser_random_ut = subparsers.add_parser(
    'random-ut', help="random upper triangular")
parser_random_ut.add_argument("out", help="output file")
parser_random_ut.add_argument("num_rows", help="number of rows")
parser_random_ut.add_argument("num_edges", help="total number of edges")
parser_random_ut.set_defaults(func=generate_random_ut)

args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()
args.func(args)
