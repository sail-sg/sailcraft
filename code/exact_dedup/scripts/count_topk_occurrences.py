
import subprocess
import shlex
import os
import math
import glob
from collections import OrderedDict, defaultdict
from tqdm import tqdm
import json
import argparse

# Powers of 256 precomputed for use in byte manipulations.
powers_of_256 = [256**i for i in range(7)]  # Adjust the range as needed.

# Inspired by Yanai Elazar (@yanaiela).
# Source: https://github.com/google-research/deduplicate-text-datasets/issues/20#issuecomment-1258518761
# This function has been enhanced to adaptively calculate the size_of_pointer to prevent out-of-scope errors.
def get_dups_pointers(dups_f, sizes_f, size_of_pointer, threshold=100):
    # Read the dups file contents.
    with open(dups_f, 'rb') as f:
        dups = f.read()

    # Read the sizes file contents.
    with open(sizes_f, 'rb') as f:
        sizes = f.read()

    # Initialize the list for storing pointer data and frequency collections.
    pointers = []
    freq_collections = {}

    # Create a map of integers based on the specified size of pointer.
    int_map = powers_of_256[:size_of_pointer]

    # int manipulation
    extra = 0
    for i in range(0, len(sizes), size_of_pointer):
        count = 0
        for j, mult in zip(range(size_of_pointer), int_map):
            count += sizes[i + j] * mult
        if count > threshold:
            pointer = 0
            for j, mult in zip(range(size_of_pointer), int_map):
                pointer += dups[extra + j] * mult

            pointers.append(pointer)
            freq_collections[count] = pointer

        extra += (size_of_pointer * count)

    sorted_dict =  dict(sorted(freq_collections.items(), reverse=True))

    return pointers, sorted_dict

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Load a dataset.')
    parser.add_argument('--data_alias', type=str, default='sample')
    parser.add_argument('--split', type=str, default='train')
    parser.add_argument('--top_k_number', type=int, default=100)
    parser.add_argument('--threshold', type=int, default=100)
    parser.add_argument('--cache_dir', type=str, default='../../cache/data_clean_cache')
    args = parser.parse_args()

    data_alias = "{}.{}".format(args.data_alias, args.split)
    cache_dir=args.cache_dir
    top_k_number = args.top_k_number
    threshold = args.threshold

    print('====processing {}===='.format(data_alias))

    dups_prefix = os.path.join(cache_dir, 'dups_{}'.format(data_alias))
    sizes_prefix = os.path.join(cache_dir,'sizes_{}'.format(data_alias))

    dups_files = sorted(glob.glob(f'{dups_prefix}*'))
    sizes_files = sorted(glob.glob(f'{sizes_prefix}*'))

    ### Calculate the size of pointer based on the ratio of sizes between the raw data file and its suffix array.
    ### The raw data file contains concatenated data sets.
    ### The suffix array file aids in efficient text searches.
    ### Documentation: https://github.com/google-research/deduplicate-text-datasets#finding-all-repeated-substrings-within-a-document
    data_size = os.path.getsize(os.path.join(cache_dir, '{}'.format(data_alias)))
    suffix_size = os.path.getsize(os.path.join(cache_dir, '{}.table.bin'.format(data_alias)))
    size_of_pointer = math.ceil(suffix_size/data_size)

    print("There are {} files in total for {}".format(len(dups_files), data_alias))

    total_sorted_dict = defaultdict(int)
    for idx, (dups, sizes) in tqdm(enumerate(zip(dups_files, sizes_files))):
        _, sorted_dict = get_dups_pointers(dups, sizes, size_of_pointer, threshold)
        for key, value in sorted_dict.items():
            total_sorted_dict[value] += key

    # print(total_sorted_dict)
    total_sorted_dict = dict(sorted(total_sorted_dict.items(), key=lambda item: item[1], reverse=True))
    top_k_cnt = list(total_sorted_dict.values())[:top_k_number]
    top_k_values = list(total_sorted_dict.keys())[:top_k_number]
    print(top_k_values, '\n', top_k_cnt)

    f=open(os.path.join(cache_dir, data_alias),"rb").read()
    for idx, (p, cnt) in enumerate(zip(top_k_values,top_k_cnt)):
        dedup_text = f[p:p+100]
        sdedup_text = dedup_text.decode('utf-8', errors='ignore')
        sdedup_text = sdedup_text.strip()
        sdedup_text = shlex.quote(sdedup_text)
        print(cnt, '\n', sdedup_text)