#! /usr/bin/env python

from __future__ import print_function
import sys
import os
import math
import logging
from util.edgelist import edgelist
from collections import defaultdict
import argparse

def histogram(xs, num_buckets):
    min_x = min(xs)
    max_x = max(xs)
    bucket_size = (max_x - min_x + num_buckets) / num_buckets
    buckets = [0 for i in range(num_buckets)]
    for x in xs:
        bucket_id = int((x - min_x) / bucket_size)
        buckets[bucket_id] += 1
    return buckets

def histogram_power(xs):
    max_x = max(xs)
    max_bucket = int(math.ceil(math.log(max_x, 2.0)))
    if max_x % 2 == 0:
        max_bucket += 1
    buckets = [0 for i in range(max_bucket)]
    for x in xs:
        bucket_id = int(math.log(x, 2.0))
        buckets[bucket_id] += 1
    return buckets

def make_sf(num_edges, min_degree, max_degree, num_buckets, gamma):
    bucket_size = (max_degree - min_degree + num_buckets) / num_buckets
    buckets = [0 for _ in range(num_buckets)]
    for i in range(num_buckets):
        bucket_floor = min_degree + i * num_buckets
        bucket_ceil = bucket_floor + bucket_size
        bucket_count = 0
        for k in range(bucket_floor, bucket_ceil):
            p = k ** (-1 * gamma)
            bucket_count += p * num_edges
        buckets[i] = bucket_count

    # scale = num_edges / sum(buckets)
    # buckets = [int(round(b * scale)) for b in buckets ]
    buckets = [int(round(b)) for b in buckets ]
    return buckets

def avg(xs):
    return sum(xs) / float(len(xs))

def med(xs):
    s = sorted(xs)
    if len(s) % 2 == 0:
        return float(s[len(s) // 2])
    else:
        return (s[len(s) // 2 - 1] + s[len(s) // 2]) / 2.0

def var(xs):
    x_bar = avg(xs)
    num = sum((x - x_bar)**2 for x in xs)
    den = len(xs) - 1
    return num / den


logging.basicConfig(level=logging.INFO)
parser = argparse.ArgumentParser(description="Print some graph statistics")
parser.add_argument('paths', type=str, nargs="+", help="graph files")
parser.add_argument('-d', '--dag', type=str, choices=["lower", "upper"], nargs="+", default=["lower", "upper"], help="lower (src > dst) or upper (src < dst)")
args = parser.parse_args()

def upper_triangular(edge):
    return edge[0] < edge[1]

def lower_triangular(edge):
    return edge[1] < edge[0]

print("graph, dag, nodes, edges, out_min, out_max, out_avg, out_med, out_var, out_ssd, buckets")

for path in args.paths:
    for dag in args.dag:

        if dag == "upper":
            dag_filter = upper_triangular
        elif dag == "lower":
            dag_filter = lower_triangular
        else:
            logging.error("Unhandled DAG filter")
            sys.exit(-1)

        print("{}, {}, ".format(os.path.basename(path), dag), end = "")
        sys.stdout.flush()

        adj = defaultdict(int)
        dsts = set()

        with edgelist(path) as el:
            for edge in el:
                if dag_filter(edge):
                    src, dst = edge
                    adj[src] += 1
                    dsts.add(dst)

        # compute nodes
        num_nodes = len(set(dsts).union(set(adj)))
        # print("nodes:", len(nodes))

        # compute in degree and out degree
        out_degrees = adj.values()
        num_edges = sum(out_degrees)

        # out-degree statistics
        min_out = min(out_degrees)
        max_out = max(out_degrees)
        avg_out = avg(out_degrees)
        med_out = med(out_degrees)
        var_out = var(out_degrees)


        ssd_out = sum(d ** 2 for d in out_degrees)
        # print("out ssd:", out_ssd)
        # print("in ssd :", in_ssd)

        histo_out = histogram_power(out_degrees)

        # histo_sf2 = make_sf(sum(in_degree), min_out, max_out, NUM_BUCKETS, 2)
        # histo_sf3 = make_sf(sum(in_degree), min_out, max_out, NUM_BUCKETS, 3)

        # print("sf2:", histo_sf2)
        # print("sf3:", histo_sf3)

        print("{}, {}, {}, {}, {}, {}, {}, {}, {}".format(
            num_nodes,
            num_edges,
            min_out,
            max_out,
            avg_out,
            med_out,
            var_out,
            ssd_out,
            ", ".join(str(e) for e in histo_out)
        ))