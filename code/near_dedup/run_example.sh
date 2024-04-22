#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "$0") && pwd)

# INPUT_FILE='/home/aiops/doulx/code/sailor_data_script/data/data_output/cleaned_data_output/sample/data_clean.jsonl'
# OUTPUT_DIR='/home/aiops/doulx/code/sailor_data_script/data/data_output/near_dedup_output/sample'
# CACHE_PATH='/home/aiops/doulx/code/sailor_data_script/cache/near_dedup_cache'

INPUT_FILE=$1
OUTPUT_DIR=$2
CACHE_PATH=$3

python -m text_dedup.minhash \
  --path "json" \
  --name "data_clean" \
  --data_files $INPUT_FILE \
  --output $OUTPUT_DIR \
  --cache_dir $CACHE_PATH \
  --column "text" \
  --split "train" \
  --batch_size 10000 \
  --num_perm 256

python $SCRIPT_DIR/../data_cleaning/write_arrow_to_jsonl.py \
        --folder_path $OUTPUT_DIR