"""the graphchallenge download subcommand"""

import hashlib
import os
import urllib.request
from urllib.parse import urlparse
import sys
import struct
import gzip
import shutil

from datasets import GRAPH_CHALLENGE


def get_remote_size(url):
    site = urllib.urlopen(url)
    meta = site.info()
    print(meta.getheaders("Content-Length")[0])


def get_file_size(path):
    return os.stat(path).st_size


def is_file(path):
    return os.path.isfile(path)


def hash_file(path):
    with open(path, "rb") as f:
        hasher = hashlib.md5()
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
        return hasher.hexdigest().lower()


def get_basename(url):
    parsed = urlparse(url)
    path = os.path.basename(parsed.path)
    return path


def urlretrieve(url, file_name):
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)


def graphchallenge(args):
    output_dir = args.out

    # check if output directory exists
    if not os.path.isdir(output_dir):
        print("output directory {} does not exist".format(output_dir))
        sys.exit(-1)

    if args.name:
        matching_graphs = [(u, m) for (
            u, m) in GRAPH_CHALLENGE if args.name.lower() in u.lower()]
    else:
        matching_graphs = GRAPH_CHALLENGE

    if args.list:
        for (url, _) in matching_graphs:
            print(url)
        sys.exit(0)

    for (url, expected_md5) in matching_graphs:
        if expected_md5:
            assert len(expected_md5) == 32
        needs_download = ""
        name = get_basename(url)
        dst = os.path.join(output_dir, name)

        # check if dst exists
        if not needs_download and not is_file(dst):
            needs_download = name + " missing"

        # compare hashes
        if not needs_download and expected_md5:
            try:
                actual_md5 = hash_file(dst)
                if actual_md5 != expected_md5.lower():
                    needs_download = "hash mismatch"
                else:
                    print("MD5_MATCH", dst)

            except IOError as e:
                needs_download = "file open error"

        if needs_download:
            print("DOWNLOAD", dst, "reason:", needs_download)
            try:
                urlretrieve(url, dst)
            except IOError as e:
                print("IOERROR", url, str(e))
                continue
            if hash_file(dst) != expected_md5:
                print("MISMATCH", dst)

        # check if the file needs to be extracted
        if dst.endswith(".gz"):
            needs_extract = ""
            extracted_path = dst[:-3]
            if not needs_extract:
                try:
                    actual_size = os.path.getsize(extracted_path)
                except OSError:
                    needs_extract = extracted_path + " missing"

            if not needs_extract:
                with open(dst, "rb") as f:
                    f.seek(-4, os.SEEK_END)
                    buf = f.read(4)
                    expected_size = struct.unpack("I", buf)[0]

                if actual_size % 2**32 != expected_size:
                    needs_extract = "size mismatch"

            if needs_extract:
                print("EXTRACT", dst, "reason:", needs_extract)
                with gzip.open(dst, 'rb') as f_in, open(extracted_path, "w") as f_out:
                    shutil.copyfileobj(f_in, f_out)
            else:
                print("EXTRACT_MATCH", extracted_path)
