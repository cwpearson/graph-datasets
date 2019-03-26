import os

def split(path):
    root, ext = os.path.splitext(path)
    head, tail = os.path.split(root)
    return head, tail, ext