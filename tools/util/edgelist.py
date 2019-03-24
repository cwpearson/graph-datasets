import logging
import mmap
import struct


def BELIter(mp):
    for i in range(0, len(mp), 24):
        dst,src = struct.unpack("<QQ", mp[i:i+16])
        yield src, dst


class BEL:
    def __init__(self,path):
        self.path = path
        self.f = open(path, "r+")
        self.mp = mmap.mmap(self.f.fileno(), 0)

    def __del__(self):
        self.f.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __iter__(self):
        return BELIter(self.mp)


def TSVIter(f):
    for line in f:
        fields = line.split()
        dst = int(fields[0])
        src = int(fields[1])
        yield src, dst


class TSV:
    def __init__(self,path):
        self.path = path
        self.f = open(path, "r")

    def __del__(self):
        self.f.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __iter__(self):
        return TSVIter(self.f)


class edgelist:
    def __init__(self, path):
        self.path = path
        self.reader = None
        

    def __enter__(self):
        if self.path.endswith(".bel"):
            self.reader = BEL(self.path)
        elif self.path.endswith(".tsv"):
            self.reader = TSV(self.path)
        else:
            assert False
        return self

    def __exit__(self):
        pass

    def __iter__(self):
        return iter(self.reader)