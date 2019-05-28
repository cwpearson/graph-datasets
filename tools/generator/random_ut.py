import random
import math
import time

from util.edgelist import BELWriter


class RandomUT(object):
    def __init__(self, num_rows, num_edges, seed=None):
        self.num_rows = num_rows

        max_edges = sum(range(self.num_rows))
        self.num_edges = min(num_edges, max_edges)
        self.num_edges = max(0, self.num_edges)

        self.seed = seed

    def write(self, path):

        edge_list_file = BELWriter(path)

        edges_left = self.num_edges
        max_dst = self.num_rows

        start_time = time.time()
        nnz_counter = 0
        for row in range(self.num_rows):
            elapsed_time = time.time() - start_time
            if elapsed_time > 10:  # report every 10s
                nnzps = (nnz_counter) / elapsed_time
                if nnzps == 0:
                    eta = None
                    print(f"{nnzps:.0f} nz/s: eta {eta}s")
                else:
                    eta = edges_left / nnzps
                    print(f"{nnzps:.0f} nz/s: eta {eta:.0f}s")
                nnz_counter = 0
                start_time = time.time()

            # generate edges proportional to row length
            row_length = self.num_rows - row - 1
            min_dst = row + 1  # all dsts should be to larger rows

            edge_fraction = row_length / \
                (self.num_rows * (self.num_rows - 1) / 2)
            edges_to_generate, rem = divmod(self.num_edges * edge_fraction, 1)
            edges_to_generate = int(edges_to_generate)
            if rem > 0.5:
                edges_to_generate += 1
            if edges_to_generate == 0 and rem > 0:
                edges_to_generate += 1

            edges_to_generate = min(edges_left, edges_to_generate)

            dsts = random.sample(range(min_dst, max_dst), edges_to_generate)
            dsts.sort()
            # print(dsts)

            edges_left -= len(dsts)
            nnz_counter += len(dsts)

            for dst in dsts:
                edge_list_file.write((row, dst))

        assert edges_left == 0
