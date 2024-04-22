#!/bin/bash

### step0: 

### install package
# pip install -r requirements.txt

### download resource, including kenlm model and sentenpiece model
# mkdir lm_resource 
# python data_cleaning/download_sentencepiece_kenlm_models.py --output_dir_path lm_resource

mkdir -p cache/data_clean_cache
mkdir -p cache/near_dedup_cache
mkdir -p cache/exact_dedup_cache

mkdir -p data/data_input 
mkdir -p data/data_output/cleaned_data_output 
mkdir -p data/data_output/near_dedup_output 
mkdir -p data/data_output/exact_dedup_output

ALIAS=sample
INPUT_FILE=./data/data_output/cleaned_data_output/$ALIAS/data_clean.jsonl
OUTPUT_DIR=./data/data_output/near_dedup_output/$ALIAS


### step1: data-cleaning
bash code/data_cleaning/run_example.sh \
    data/data_input/sample.jsonl \
    id \
    data/data_output/cleaned_data_output \
    lm_resource \
    cache/data_clean_cache


### step2: near-dedup
bash code/near_dedup/run_example.sh \
    data/data_output/cleaned_data_output/$ALIAS/data_clean.jsonl \
    data/data_output/near_dedup_output/$ALIAS \
    cache/near_dedup_cache


### step3: exact-dedup
bash code/exact_dedup/run_example.sh \
    data/data_output/near_dedup_output/$ALIAS/data_clean.jsonl \
    data/data_output/exact_dedup_output/$ALIAS \
    $ALIAS \
    cache/exact_dedup_cache \
    cache/exact_dedup_cache 


### step4: output stats

echo "Counting lines in cleaned data output: $(wc -l < data/data_output/cleaned_data_output/sample/data_clean.jsonl)"
echo "Counting lines in near deduplication output: $(wc -l < data/data_output/near_dedup_output/sample/data_clean.jsonl)"
echo "Counting lines in exact deduplication output: $(wc -l < data/data_output/exact_dedup_output/sample/sample.jsonl)"

