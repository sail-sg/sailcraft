
import subprocess
import shlex
import os
import glob
from collections import OrderedDict, defaultdict
from tqdm import tqdm
import json

a = 256**0
b = 256**1
c = 256**2
d = 256**3
e = 256**4

def get_dups_pointers(dups_f, sizes_f, threshold=100):
    with open(dups_f, 'rb') as f:
        dups = f.read()

    with open(sizes_f, 'rb') as f:
        sizes = f.read()

    pointers = []
    freq_collections = {}

    # int manipulation
    extra = 0
    for i in range(0, len(sizes), 5):
        count = 0
        for j, mult in zip(range(5), [a,b,c,d,e]):
            count += sizes[i + j] * mult

        if count > threshold:
            pointer = 0
            
            for j, mult in zip(range(5), [a,b,c,d,e]):
                pointer += dups[extra + j] * mult

            pointers.append(pointer)
            freq_collections[count] = pointer

        extra += (5 * count)

    sorted_dict =  dict(sorted(freq_collections.items(), reverse=True))
    top_k_values = [value for _, value in list(sorted_dict.items())[:10]]

    return pointers, sorted_dict, top_k_values

if __name__ == "__main__":
    data_alias = 'cleaned_cc100_ind_dedup_doc_1.train'

    print('====processing {}===='.format(data_alias))
    
    dups_prefix = 'tmp/cache/dups_{}'.format(data_alias)
    sizes_prefix = 'tmp/cache/sizes_{}'.format(data_alias)
    dups_files = sorted(glob.glob(f'{dups_prefix}*'))
    sizes_files = sorted(glob.glob(f'{sizes_prefix}*'))

    print("There are {} files in total for {}".format(len(dups_files), data_alias))

    total_sorted_dict = defaultdict(int)
    for idx, (dups, sizes) in tqdm(enumerate(zip(dups_files, sizes_files))):
        _, sorted_dict, _ = get_dups_pointers(dups, sizes)
        for key, value in sorted_dict.items():
            total_sorted_dict[value] += key

    # print(total_sorted_dict)
    total_sorted_dict = dict(sorted(total_sorted_dict.items(), key=lambda item: item[1], reverse=True))
    top_k_number = 100
    top_k_cnt = list(total_sorted_dict.values())[:top_k_number]
    top_k_values = list(total_sorted_dict.keys())[:top_k_number]
    print(top_k_values, '\n', top_k_cnt)

    with open(f'{data_alias}.json', 'w') as json_file:
        json.dump(total_sorted_dict, json_file)
    zipped_lists = zip(top_k_values, top_k_cnt)
    with open(f'{data_alias}.txt', 'w') as f:
        for value, cnt in zipped_lists:
            f.write(f"{value}\t{cnt}\n")


    # top_k_values = []
    # top_k_cnt = []
    # last_cnt = 0
    # with open(f'{data_alias}.json', 'r') as f:
    #     data = json.load(f)

    #     for key, value in data.items():
    #         if abs(value - last_cnt)<100:
    #             continue
    #         last_cnt = value

    #         top_k_values.append(int(key))
    #         top_k_cnt.append(int(value))

    f=open("/sail-data/sealm/cleaned_data/dedup_exp/google_exp/{}".format(data_alias),"rb").read()
    for idx, (p, cnt) in enumerate(zip(top_k_values,top_k_cnt)):
        if idx>10:
            continue

        dedup_text = f[p:p+100]

        sdedup_text = dedup_text.decode('utf-8', errors='ignore')
        sdedup_text = sdedup_text.strip()
        sdedup_text = shlex.quote(sdedup_text)
        print(cnt, '\n', sdedup_text)