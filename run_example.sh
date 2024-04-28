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
mkdir -p data/data_output/final_output

ALIAS=sample
LANGUAGE=id


# ### step1: data-cleaning
bash code/data_cleaning/run_example.sh \
    $ALIAS \
    data/data_input/$ALIAS.jsonl \
    $LANGUAGE \
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


### step4: data-clean
bash code/data_cleaning/run_example.sh \
    $ALIAS \
    data/data_output/exact_dedup_output/$ALIAS/data_clean.jsonl \
    $LANGUAGE \
    data/data_output/final_output \
    lm_resource \
    cache/data_clean_cache


### step5: output stats
echo "Counting lines in cleaned data output: $(wc -l < data/data_output/cleaned_data_output/$ALIAS/data_clean.jsonl)"
echo "Counting lines in near deduplication output: $(wc -l < data/data_output/near_dedup_output/$ALIAS/data_clean.jsonl)"
echo "Counting lines in exact deduplication output: $(wc -l < data/data_output/exact_dedup_output/$ALIAS/data_clean.jsonl)"
echo "Counting lines in final output: $(wc -l < data/data_output/final_output/$ALIAS/data_clean.jsonl)"

