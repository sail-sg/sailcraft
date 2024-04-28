### SailCraft

This repo provides the data process pipeline for large language model training.
It consists of data cleaning, near deduplication and exact deduplication.

### Requirements

Install the package and download the models
```
pip install -r requirements.txt
mkdir lm_resource 
python data_cleaning/download_sentencepiece_kenlm_models.py --output_dir_path lm_resource
```

Install Rust for exact dedup, refer to [this guidance](https://github.com/google-research/deduplicate-text-datasets#installing).
```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
. "$HOME/.cargo/env"
```

### Quickstart

We sample 1000 lines from [cc100](https://data.statmt.org/cc-100/) Indonesian subset for quick check.

```
bash run_example.sh
```

As expected, you should observe the following log
```
Counting lines in cleaned data output: 987
Counting lines in near deduplication output: 974
Counting lines in exact deduplication output: 979
Counting lines in final output: 949
```
The final output are `/data/data_output/exact_dedup_output/sample/sample.jsonl`.

### Case Studies

1. for data cleaning, check the `code/data_cleaning/filtering_logs` for each filter.

2. run `code/exact_dedup/scripts/count_topk_occurrences.py` to obtain the top-k occurrences.
```
python code/exact_dedup/scripts/count_topk_occurrences.py \
    --data_alias sample \
    --split train \
    --top_k_number 100 \
    --threshold 2 \
    --cache_dir cache/exact_dedup_cache 
```
This script displays the 100 most frequent spans with a frequency greater than two.


| Count | Excerpt                                                                                           |
|-------|---------------------------------------------------------------------------------------------------|
| 4     | 'pernah disentuh oleh manusia sebelum mereka (penghuni-penghuni surga yang menjadi suami mereka) dan' |
| 4     | 'k pernah disentuh oleh manusia sebelum mereka (penghuni-penghuni surga yang menjadi suami mereka) da' |
| 4     | 'nah disentuh oleh manusia sebelum mereka (penghuni-penghuni surga yang menjadi suami mereka) dan tid' |
| 4     | 'sentuh oleh manusia sebelum mereka (penghuni-penghuni surga yang menjadi suami mereka) dan tidak pul' |
| 4     | 'uh oleh manusia sebelum mereka (penghuni-penghuni surga yang menjadi suami mereka) dan tidak pula ol' |
| 4     | 'ah disentuh oleh manusia sebelum mereka (penghuni-penghuni surga yang menjadi suami mereka) dan tida' |
| 4     | 'ak pernah disentuh oleh manusia sebelum mereka (penghuni-penghuni surga yang menjadi suami mereka) d' |
| 4     | 'ernah disentuh oleh manusia sebelum mereka (penghuni-penghuni surga yang menjadi suami mereka) dan t' |
| 3     | 'manusia sebelum mereka (penghuni-penghuni surga yang menjadi suami mereka) dan tidak pula oleh jin.'  |
| 3     | 'tidak pernah disentuh oleh manusia sebelum mereka (penghuni-penghuni surga yang menjadi suami mereka' |
| 3     | 'tidak pernah disentuh oleh manusia sebelum mereka (penghuni-penghuni surga yang menjadi suami merek'  |



### Acknowledgement

Thanks to the contributor of the following projects: 
[text-dedup](https://github.com/ChenghaoMou/text-dedup),
[exact-dedup](https://github.com/google-research/deduplicate-text-datasets),
[bigscience-data-preparation](https://github.com/bigscience-workshop/data-preparation),
[bigscience-data-tooling](https://github.com/bigscience-workshop/data_tooling).

### Contact 

If you have any questions, please raise an issue in our Github or contact <a href="mailto:doulx@sea.com">doulx@sea.com</a>.