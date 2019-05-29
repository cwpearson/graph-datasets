
import struct
import random
import sys
import pathlib
import mmap
import heapq

path = pathlib.Path(sys.argv[1])


def partition(A, elem_start, elem_stop, elem_size, key_start, key_stop):
    
    pivot_index = random.randint(elem_start, elem_stop)
    pivot = A[pivot_index * elem_size + key_start : pivot_index * elem_size + key_stop]

    # print(f"pivot: {pivot}")

    i = elem_start - 1
    j = elem_stop + 1

    while True:
        while True:
            i += 1
            if A[i * elem_size + key_start : i * elem_size + key_stop] < pivot:
                continue
            else:
                break

        while True:
            j -= 1
            if A[j * elem_size + key_start : j * elem_size + key_stop] > pivot:
                continue
            else:
                break

        if i >= j:
            return j

        # print(f"pivot is {pivot}")
        # print(f"swap {i} and {j}")

        # print(f"{A[i * elem_size: (i+1) * elem_size]} {A[j * elem_size: (j+1) * elem_size]}")

        tmp = bytes(A[i * elem_size : (i+1) * elem_size])
        A[i * elem_size: (i+1) * elem_size] = A[j * elem_size: (j+1) * elem_size]
        A[j * elem_size: (j+1) * elem_size] = tmp
        # print(f"{A[i * elem_size: (i+1) * elem_size]} {A[j * elem_size: (j+1) * elem_size]}")

def quicksort(array, elem_start, elem_stop, elem_size, key_start, key_stop):

    assert len(array) % elem_size == 0

    # print(f"start sorting [{elem_start} {elem_stop}]")

    if elem_start < elem_stop:
        p = partition(array, elem_start, elem_stop, elem_size, key_start, key_stop)
        quicksort(array, elem_start, p, elem_size, key_start, key_stop)
        quicksort(array, p+1, elem_stop, elem_size , key_start, key_stop)
    # print(f"done sorting [{elem_start} {elem_stop})")


def external_sort(array, elem_size, key_start, key_stop, f_out):

    assert len(array) % elem_size == 0

    # size a block to fit in-memory
    BLOCK_BYTES = 65536 * 2048
    BLOCK_ELEMS = BLOCK_BYTES // elem_size

    ARRAY_ELEMS = len(array) // elem_size
    ARRAY_BLOCKS = (ARRAY_ELEMS + BLOCK_ELEMS - 1) // BLOCK_ELEMS

    # record the element idx where each block starts and stops
    block_starts = []
    block_stops = []
    for block_idx in range(ARRAY_BLOCKS):
        block_start = block_idx * BLOCK_ELEMS
        block_stop = min(block_start + BLOCK_ELEMS, ARRAY_ELEMS)
        block_starts += [block_start]
        block_stops += [block_stop]

    print(f"{block_starts}")
    print(f"{block_stops}")

    # input("")

    # pass 1: sort each block
    for block_start, block_stop in zip(block_starts, block_stops):
        print(f"sorting block {block_start}, {block_stop}")
        block = array[block_start * elem_size : block_stop * elem_size]
        quicksort(array, block_start, block_stop-1, elem_size, key_start, key_stop)
        
    # pass 2: merge each block



    # push each key into the heap
    h = []
    block_ptrs = []
    for block_idx, (block_start, block_stop) in enumerate(zip(block_starts, block_stops)):
        key = array[block_start * elem_size + key_start : block_start * elem_size + key_stop]
        heapq.heappush(h, (key, block_idx))
        block_ptrs += [block_start + 1]

    # start at the beginning of each sorted block, but already read the first element


    while len(h):
        # get the smallest element to merge
        key, block_idx = heapq.heappop(h)

        # write
        elem_ptr = block_ptrs[block_idx] - 1
        elem = array[elem_ptr * elem_size:(elem_ptr+1) * elem_size]
        f_out.write(elem)

        # read next item from block, if the block is not exhausted
        next_ptr = block_ptrs[block_idx]
        block_stop = block_stops[block_idx]
        if next_ptr < block_stop:
            key = array[next_ptr * elem_size + key_start : next_ptr * elem_size + key_stop]
            heapq.heappush(h, (key, block_idx))
            block_ptrs[block_idx] += 1




"""
array = bytearray(struct.pack("<QQQQ", 3,2,1,0))
slices = [array[8*i:8*(1+i)] for i in range(len(array)//8)]
for s in slices:
    print(s)


# slices.sort()
external_sort(array, 8, 0, 1)

slices = [array[8*i:8*(1+i)] for i in range(len(array)//8)]
for s in slices:
    print(s)
    """

# sys.exit()

with open(path, "r+b") as f, open(path.parent/(path.name + ".sorted"), "wb") as f_out:
    mm = mmap.mmap(f.fileno(), 0)
    # read content via standard file methods
    # read content via slice notation
    external_sort(mm, 16, 0, 16, f_out)
    # close the map
    mm.close()    