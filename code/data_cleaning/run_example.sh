#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "$0") && pwd)


# ALIAS=sample
# INPUT_FILE=$SCRIPT_DIR/../../data/data_input/sample.jsonl
# LANGUAGE=id
# OUTPUT_DIR=$SCRIPT_DIR/../../data/data_output/cleaned_data_output
# LM_RESOURCE=$SCRIPT_DIR/../../lm_resource
# CACHE=$SCRIPT_DIR/../../cache/data_clean_cache

ALIAS=$1
INPUT_FILE=$2
LANGUAGE=$3
OUTPUT_DIR=$4
LM_RESOURCE=$5
CACHE=$6


python $SCRIPT_DIR/main_filtering.py \
        --dataset_name $INPUT_FILE \
        --dataset_alias $ALIAS \
        --lang_dataset_id $LANGUAGE \
        --path_dir_save_dataset $OUTPUT_DIR \
        --path_sentencepiece_model $LM_RESOURCE/$LANGUAGE.sp.model \
        --path_kenlm_model $LM_RESOURCE/$LANGUAGE.arpa.bin \
        --path_fasttext_model $LM_RESOURCE/lid.176.bin \
        --hf_cache_dir $CACHE \
        --log_folder_path $SCRIPT_DIR/filtering_logs  

python $SCRIPT_DIR/write_arrow_to_jsonl.py \
        --folder_path $OUTPUT_DIR/$ALIAS
