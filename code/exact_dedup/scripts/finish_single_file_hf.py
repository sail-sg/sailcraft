import sys
import json
import re
from cmp_dedup import find_deleted_lines

original = sys.argv[1]
remove_file = sys.argv[2]
deduped = sys.argv[3]
# original_json = sys.argv[4]

remove = []
with open(remove_file) as fin:
    for line in fin:
        if 'out' in line: 
            break
    for line in fin:
        remove.append(list(map(int, line.split())))
remove = remove[::-1]

spliter = b'[DSEP]'
# pattern = b'(\xff|[\x00-\x1f])+?[\s\S]*?\x00*?'
pattern = b'(\xff|[\x00-\x09\x0b-\x1f])+?[\s\S]*?\x00*?'

with open(original, "rb") as ds, open(deduped, "w", encoding="utf-8") as new_ds:
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

# find_deleted_lines(
#     original_path=original_json,
#     deduped_path=deduped,
# )