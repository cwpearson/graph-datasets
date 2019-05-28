import random
import math

class RandomUT(object):
    def __init__(self, num_rows, num_edges, seed = None):
        self.num_rows = num_rows

        max_edges = sum(range(self.num_rows))
        self.num_edges = min(num_edges, max_edges)
        self.num_edges = max(0, self.num_edges)

        self.seed = seed

    def write(self, path):

        edges_left = self.num_edges
        max_dst = self.num_rows
        for row in range(self.num_rows):

            # generate edges proportional to row length
            row_length = self.num_rows - row - 1
            min_dst = row + 1 # all dsts should be to larger rows

            edge_fraction = row_length / (self.num_rows * (self.num_rows - 1) / 2)
            edges_to_generate, rem = divmod(self.num_edges * edge_fraction, 1)
            edges_to_generate = int(edges_to_generate)
            if rem > 0.5:
                edges_to_generate += 1
            if edges_to_generate == 0 and rem > 0:
                edges_to_generate += 1

            edges_to_generate = min(edges_left, edges_to_generate)

            print(edge_fraction, edges_to_generate, edges_left)
            print(min_dst, max_dst)
            dsts = random.sample(range(min_dst, max_dst), edges_to_generate)
            dsts.sort()

            print(dsts)
            edges_left -= len(dsts)

        print(edges_left)
        assert edges_left == 0

r = RandomUT(10, 46)

r.write("ehhlo")