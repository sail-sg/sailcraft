import sys
import json
import re
from cmp_dedup import find_deleted_lines
import argparse


parser = argparse.ArgumentParser(description='Load a dataset.')
parser.add_argument('--data_input_alias', type=str, default='sample.train')
parser.add_argument('--remove_file', type=str, default='train')
parser.add_argument('--data_output', type=str, default='sample.jsonl')
parser.add_argument('--data_input_jsonl', type=str, default=None)
args = parser.parse_args()

data_input_alias = args.data_input_alias
remove_file = args.remove_file
data_output = args.data_output
data_input_jsonl = args.data_input_jsonl


remove = []
with open(remove_file) as fin:
    for line in fin:
        if 'out' in line: 
            break
    for line in fin:
        remove.append(list(map(int, line.split())))
remove = remove[::-1]

spliter = b'[DSEP]'
pattern = b'(\xff|[\x00-\x09\x0b-\x1f])+?[\s\S]*?\x00*?'

with open(data_input_alias, "rb") as ds, open(data_output, "w", encoding="utf-8") as new_ds:
    start = 0
    while len(remove) > 0:
        a, b = remove.pop()
        original_text_segment = ds.read(a - start)

        text_segment = re.sub(pattern, spliter, original_text_segment)

        for text_seg in text_segment.split(spliter):
            if len(text_seg) < 20:
                continue
            json_obj = {"text": text_seg.decode('utf-8', errors='ignore')}
            new_ds.write(json.dumps(json_obj, ensure_ascii=False) + "\n")
        ds.seek(b)
        start = b

    text_segment = ds.read()
    if text_segment:
        text_segment = re.sub(pattern,  spliter, text_segment)
        for text_seg in text_segment.split(spliter):
            if len(text_seg) < 20:
                continue
            json_obj = {"text": text_seg.decode('utf-8', errors='ignore')}
            new_ds.write(json.dumps(json_obj, ensure_ascii=False) + "\n") 

if data_input_jsonl:
    find_deleted_lines(
        original_path=data_input_jsonl,
        deduped_path=data_output,
    )