
import struct
import random


def partition(A, elem_start, elem_stop, elem_size):
    pivot = random.randint(elem_start, elem_stop)
    i = elem_start - 1
    j = elem_stop + 1


def quicksort(array, elem_start, elem_stop, elem_size):

    assert len(array) % elem_size == 0

    if elem_start < elem_stop:
        p = partition(array, elem_start, elem_stop, elem_size)
        quicksort(array, elem_start, p, elem_size)
        quicksort(array, p+1, elem_stop, elem_size)


def radix_sort_inplace(array, elem_start, elem_stop, elem_size, key_start, key_stop, digit):
    """array is a 2D array of bytes
    elem_start/elem_stop are the beginning and end index of array elements to sort
    base is the byte of the key to sort
    elem_size is the size of each element in array
    key_start is the offset in each element that the key starts at
    key_stop is the offset in each element that the key stops at
    """

    assert len(array) % elem_size == 0


    # print(f"sorting digit {digit} between {elem_start} and {elem_stop}")

    # pass 1: count of each kind of byte
    counts = [0 for _ in range(256)]
    for i in range(elem_start, elem_stop):
        key_byte = array[i * elem_size + key_start + digit]
        counts[key_byte] += 1

    # exclusive scan of counts to figure out where each byte should start in the sorted array
    total_count = elem_start
    offsets = []
    for c in counts:
        offsets += [total_count]
        total_count += c
    offsets += [total_count]
    
    # print(f"{offsets}")

    # pass 2: swap each element into its new position
    cur_block = 0
    i = elem_start
    while cur_block < 255: # radix-1
        # print(i, cur_block)

        if i >= offsets[cur_block+1]:
            cur_block += 1
            continue

        key_byte = array[i * elem_size + key_start + digit]

        # element is already in the right block
        if key_byte == cur_block:
            i += 1
            continue

        # print(f"swapping element {i} key_byte = {key_byte}")
        val = array[i * elem_size : (i+1) * elem_size]
        # print(f"element is {val}")

        swap_to = offsets[key_byte]
        # print(f"new offset will be {swap_to}")
        temp_elem = array[swap_to * elem_size : (swap_to + 1) * elem_size]
        # print(f"replacing {temp_elem}")
        array[swap_to * elem_size : (swap_to + 1) * elem_size] = val
        array[i * elem_size : (i+1) * elem_size] = temp_elem

        # next matching key should go one position later in the array
        offsets[key_byte] += 1    

    # sys.exit(1)

    if digit + key_start < key_stop:
        for bucket in range(256):
            bucket_start = offsets[bucket]
            bucket_stop = offsets[bucket+1]
            radix_sort_inplace(array, bucket_start, bucket_stop, elem_size, key_start, key_stop, digit + 1)
    else:
        # print("done")
        pass

array = struct.pack("<QQQQ", 3,2,1,0)
slices = [array[8*i:8*(1+i)] for i in range(len(array)//8)]
for s in slices:
    print(s)

radix_sort_inplace(bytearray(array), 0, len(array)//8, 8, 0, 8, 0)

slices = [array[8*i:8*(1+i)] for i in range(len(array)//8)]
for s in slices:
    print(s)