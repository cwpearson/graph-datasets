import logging
import mmap
import struct


def BELIter(path):
    with open(path, "r+") as f:
        mp = mmap.mmap(f.fileno(), 0)
        for i in range(0, len(mp), 24):
            dst,src = struct.unpack("<QQ", mp[i:i+16])
            yield src, dst


class BELReader:
    def __init__(self,path):
        self.path = path


    def __del__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __iter__(self):
        return BELIter(self.path)

class BELWriter:
    def __init__(self,path):
        self.path = path
        self.f = None 

    def __del__(self):
        if self.f:
            self.f.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def write(self, edge):
        if not self.f:
            self.f = open(self.path, "wb")
        src, dst = edge
        weightBytes = struct.pack("<Q", 1)
        dstBytes = struct.pack("<Q", int(dst))
        srcBytes = struct.pack("<Q", int(src))
        self.f.write(dstBytes + srcBytes + weightBytes)


def TSVIter(path):
    with open(path, "r") as f:
        for line in f:
            fields = line.split()
            dst = int(fields[0])
            src = int(fields[1])
            yield src, dst


class TSV:
    def __init__(self,path):
        self.path = path
        self.f = None

    def __del__(self):
        if self.f:
            self.f.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __iter__(self):
        return TSVIter(self.path)

    def write(self, edge):
        if not self.f:
            self.f = open(self.path, "w")
        src, dst = edge
        weight = str(1)
        self.f.write("{}\t{}\t{}\n".format(dst, src, weight))    


class edgelist:
    def __init__(self, path):
        self.path = path
        self.reader = None
        self.writer = None

    def _lazy_init(self):
        if not self.reader:
            if self.path.endswith(".bel"):
                self.reader = BELReader(self.path)
            elif self.path.endswith(".tsv"):
                self.reader = TSV(self.path)
            else:
                assert False
        if not self.writer:
            if self.path.endswith(".bel"):
                self.writer = BELWriter(self.path)
            elif self.path.endswith(".tsv"):
                self.writer = TSV(self.path)
            else:
                assert False

    def __enter__(self):
        self._lazy_init()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __iter__(self):
        return iter(self.reader)

    def write(self, edge):
        self._lazy_init()
        return self.writer.write(edge)