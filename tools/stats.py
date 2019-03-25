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
        return s[len(s) // 2]
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
args = parser.parse_args()

print("graph, nodes, edges, in_min, in_max, in_avg, in_med, out_min, out_max, out_avg, out_med, out_var, in_ssd, out_ssd, buckets")

for path in args.paths:

    print("{}, ".format(os.path.basename(path)), end = "")
    sys.stdout.flush()

    inc = defaultdict(int)
    adj = defaultdict(int)

    with edgelist(path) as edgelist:
        for src, dst in edgelist:
            if src < dst:
                inc[dst] += 1
                adj[src] += 1

    # compute nodes
    num_nodes = len(set(inc.keys()).union(set(adj.keys())))
    # print("nodes:", len(nodes))

    # compute in degree and out degree
    in_degrees = inc.values()
    out_degrees = adj.values()

    num_edges = sum(in_degrees)

    # in-degree statistics
    min_in = min(in_degrees)
    max_in = max(in_degrees)
    avg_in = avg(in_degrees)
    med_in = med(in_degrees)

    # out-degree statistics
    min_out = min(out_degrees)
    max_out = max(out_degrees)
    avg_out = avg(out_degrees)
    med_out = med(out_degrees)
    var_out = var(out_degrees)


    ssd_in = sum(d ** 2 for d in in_degrees)
    ssd_out = sum(d ** 2 for d in out_degrees)
    # print("out ssd:", out_ssd)
    # print("in ssd :", in_ssd)

    histo_in = histogram_power(in_degrees)
    histo_out = histogram_power(out_degrees)

    # histo_sf2 = make_sf(sum(in_degree), min_out, max_out, NUM_BUCKETS, 2)
    # histo_sf3 = make_sf(sum(in_degree), min_out, max_out, NUM_BUCKETS, 3)

    # print("sf2:", histo_sf2)
    # print("sf3:", histo_sf3)

    print("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(
        num_nodes,
        num_edges,
        min_in,
        max_in,
        avg_in,
        med_in,
        min_out,
        max_out,
        avg_out,
        med_out,
        var_out,
        ssd_in,
        ssd_out,
        ", ".join(str(e) for e in histo_out)
    ))