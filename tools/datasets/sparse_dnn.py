import hashlib
import pathlib
import urllib.request
import gzip
import shutil
import tarfile


def hash_file(path):
    with open(path, "rb") as f:
        hasher = hashlib.md5()
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
        return hasher.hexdigest().lower()


def get_remote_size(url):
    site = urllib.request.urlopen(url)
    meta = site.info()
    return int(meta["Content-Length"])


class SparseDNN(object):
    layers = {
        "1024": ("https://graphchallenge.s3.amazonaws.com/synthetic/sparsechallenge_2019/dnn/neuron1024.tar.gz",
                 "8ccdd73e06ff905f7c72410e9a5cc4be"),
        "4096": ("https://graphchallenge.s3.amazonaws.com/synthetic/sparsechallenge_2019/dnn/neuron4096.tar.gz", "ebf3785df180ae921db7c805e5c9adfb"),
        "16384": ("https://graphchallenge.s3.amazonaws.com/synthetic/sparsechallenge_2019/dnn/neuron16384.tar.gz", "92a48c20050e3d8fcf511b810eb56faf"),
        "65536": ("https://graphchallenge.s3.amazonaws.com/synthetic/sparsechallenge_2019/dnn/neuron65536.tar.gz", None),
    }

    cats = {
        "1024": {
            "120": (
                "https://graphchallenge.s3.amazonaws.com/synthetic/sparsechallenge_2019/dnn/neuron1024-l120-categories.tsv", None),
            "480": (
                "https://graphchallenge.s3.amazonaws.com/synthetic/sparsechallenge_2019/dnn/neuron1024-l480-categories.tsv", None),
            "1920": (
                "https://graphchallenge.s3.amazonaws.com/synthetic/sparsechallenge_2019/dnn/neuron1024-l1920-categories.tsv", None),
        },
        "4096": {
            "120": (
                "https://graphchallenge.s3.amazonaws.com/synthetic/sparsechallenge_2019/dnn/neuron4096-l120-categories.tsv", None),
            "480": (
                "https://graphchallenge.s3.amazonaws.com/synthetic/sparsechallenge_2019/dnn/neuron4096-l480-categories.tsv", None),
            "1920": (
                "https://graphchallenge.s3.amazonaws.com/synthetic/sparsechallenge_2019/dnn/neuron4096-l1920-categories.tsv", None),
        },
        "16384": {
            "120": (
                "https://graphchallenge.s3.amazonaws.com/synthetic/sparsechallenge_2019/dnn/neuron16384-l120-categories.tsv", None),
            "480": (
                "https://graphchallenge.s3.amazonaws.com/synthetic/sparsechallenge_2019/dnn/neuron16384-l480-categories.tsv", None),
            "1920": (
                "https://graphchallenge.s3.amazonaws.com/synthetic/sparsechallenge_2019/dnn/neuron16384-l1920-categories.tsv", None),
        },
        "65536": {
            "120": (
                "https://graphchallenge.s3.amazonaws.com/synthetic/sparsechallenge_2019/dnn/neuron65536-l120-categories.tsv", None),
            "480": (
                "https://graphchallenge.s3.amazonaws.com/synthetic/sparsechallenge_2019/dnn/neuron65536-l480-categories.tsv", None),
            "1920": (
                "https://graphchallenge.s3.amazonaws.com/synthetic/sparsechallenge_2019/dnn/neuron65536-l1920-categories.tsv", None),
        },
    }

    def __init__(self, dst):
        self.dst = pathlib.Path(dst).resolve()

    def retrieve_file(dst, url, md5_sum, num_retries=3):
        """try to download a file"""
        target_path = dst/pathlib.Path(url).name

        # if the local path exists, redownload if the size doesn't match
        if target_path.exists():
            local_size = target_path.stat().st_size
            remote_size = get_remote_size(url)
            if local_size == remote_size:
                return

        # if the local path exists, redownload if the hash doesn't match
        if target_path.exists():
            if m5d_sum:
                local_hash = hash_file(target_path)
                if local_hash == hash:
                    return

        # try to download
        print(f"{url} -> {target_path}")
        remaining_download_tries = num_retries
        while remaining_download_tries > 0:
            try:
                urllib.request.urlretrieve(
                    url, target_path)
            except e:
                # error while downloading, try again
                print(
                    f"error {e} downloading {url}. {remaining_download_tries} tries remaining")
                remaining_download_tries -= 1
                continue

            # check the hash after a download
            if md5_sum:
                local_hash = hash_file(target_path)
                if local_hash == md5_sum:
                    break  # hash matched
                else:
                    print(
                        f"hash mismatch after download {url}. {remaining_download_tries} tries remaining")

            remaining_download_tries -= 1
        return

    def extract_gz(src, dst):
        # read the edges from the compressed file and write into dst/src order big-endian
        # for later sorting with qsort
        print(f"{src} -> {dst}")

        with tarfile.open(src, "r:gz") as tar:
            
            import os
            
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner) 
                
            
            safe_extract(tar, path=dst)

    def fetch(self, name):

        dst = self.dst
        # make dataset directory
        dst.mkdir(exist_ok=True)

        # download layer gz
        SparseDNN.retrieve_file(
            dst, SparseDNN.layers[name][0], SparseDNN.layers[name][1])

        # extract layer gz
        gz_name = f"neuron{name}.tar.gz"
        SparseDNN.extract_gz(dst/gz_name, dst)

        # download category files
        for depth, tup in SparseDNN.cats[name].items():
            SparseDNN.retrieve_file(dst, tup[0], tup[1])


d = SparseDNN("/home/pearson/graph/sparse-dnn-1024")
d.fetch("1024")

d = SparseDNN("/home/pearson/graph/sparse-dnn-4096")
d.fetch("4096")

d = SparseDNN("/home/pearson/graph/sparse-dnn-16384")
d.fetch("16384")

d = SparseDNN("/home/pearson/graph/sparse-dnn-65536")
d.fetch("65536")
