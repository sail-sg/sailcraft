#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "$0") && pwd)

# INPUT_FILE=$SCRIPT_DIR/../../data/data_output/near_dedup_output/sample/data_clean.jsonl
# OUTPUT_DIR=$SCRIPT_DIR/../../data/data_output/exact_dedup_output/sample
# ALIAS=sample
# CACHE=$SCRIPT_DIR/../../cache/exact_dedup_cache
# DATA_DIR=$SCRIPT_DIR/../../cache/exact_dedup_cache

INPUT_FILE=$(realpath $1)
OUTPUT_DIR=$2
ALIAS=$3
CACHE=$(realpath $4)
DATA_DIR=$(realpath $5)

SPLIT=train
THRESHOLD=100

cd $SCRIPT_DIR

cargo build

python3 $SCRIPT_DIR/scripts/load_dataset_hf.py --data_dir $INPUT_FILE --save_dir $DATA_DIR --name $ALIAS --split $SPLIT

ulimit -Sn 100000
mkdir -p tmp
python3 $SCRIPT_DIR/scripts/make_suffix_array.py $DATA_DIR/$ALIAS.$SPLIT

cargo run self-similar --data-file $DATA_DIR/$ALIAS.$SPLIT --length-threshold $THRESHOLD --cache-dir $CACHE

cargo run collect --data-file $DATA_DIR/$ALIAS.$SPLIT  --length-threshold $THRESHOLD --cache-dir $CACHE > $CACHE/$ALIAS.$SPLIT.remove.byterange

cd $SCRIPT_DIR/../..
mkdir -p "$OUTPUT_DIR"
python3 $SCRIPT_DIR/scripts/finish_single_file_hf.py \
    --data_input_alias $DATA_DIR/$ALIAS.$SPLIT \
    --remove_file $CACHE/$ALIAS.$SPLIT.remove.byterange \
    --data_output $OUTPUT_DIR/$ALIAS.$SPLIT.jsonl
mv $OUTPUT_DIR/$ALIAS.$SPLIT.jsonl $OUTPUT_DIR/data_clean.jsonl 
