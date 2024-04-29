# SailCraft: Data Toolkit for Sailor Language Models

[![Homepage](https://img.shields.io/badge/🏠-Homepage-3C47EB.svg)](https://sailorllm.github.io/) &nbsp;&nbsp; [![HuggingFace](https://img.shields.io/badge/🤗-HuggingFace-E87948.svg)](https://huggingface.co/sail/Sailor-7B) &nbsp;&nbsp; [![Technical Report](https://img.shields.io/badge/arXiv-2404.03608-b31b1b.svg)](https://arxiv.org/pdf/2404.03608.pdf)


This repository provides a data processing pipeline for large language model training. It consists of data cleaning, near deduplication, and exact deduplication. The data cleaning part is espeecially optimized for south-east asian languages (e.g., Thai).

## Requirements

Install the package and download the models:

```
pip install -r requirements.txt
mkdir lm_resource
python data_cleaning/download_sentencepiece_kenlm_models.py --output_dir_path lm_resource
```

Install Rust for exact deduplication, refer to [this guidance](https://github.com/google-research/deduplicate-text-datasets#installing).

```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
. "$HOME/.cargo/env"
```

## Quickstart

We sample 1000 lines from the [cc100](https://data.statmt.org/cc-100/) Indonesian subset for a quick check.

```
bash run_example.sh
```

As expected, you should observe the following log:

```
Counting lines in cleaned data output: 987
Counting lines in near deduplication output: 974
Counting lines in exact deduplication output: 963
Counting lines in final output: 949
```

The final output is located at `data/data_output/exact_dedup_output/sample/sample.jsonl`.

### Run on Your Own Dataset

1. Place the `ALIAS.jsonl` in `data/data_input/`
2. Change the `ALIAS` and `LANGUAGE` in `run_example.sh`.

### Case Studies

1. For data cleaning, check the `code/data_cleaning/filtering_logs` for each filter.
2. Run `code/exact_dedup/scripts/count_topk_occurrences.py` to obtain the top-k occurrences.

```shell
python code/exact_dedup/scripts/count_topk_occurrences.py \
--data_alias sample \
--split train \
--top_k_number 100 \
--threshold 2 \
--cache_dir cache/exact_dedup_cache
```

This script displays the top 100 most frequent text spans that occur more than twice in the dataset.

| Count | Excerpt |
|-------|---------------------------------------------------------------------------------------------------|
| 4 | 'pernah disentuh oleh manusia sebelum mereka (penghuni-penghuni surga yang menjadi suami mereka) dan' |
| 4 | 'k pernah disentuh oleh manusia sebelum mereka (penghuni-penghuni surga yang menjadi suami mereka) da' |
| 4 | 'nah disentuh oleh manusia sebelum mereka (penghuni-penghuni surga yang menjadi suami mereka) dan tid' |
| 4 | 'sentuh oleh manusia sebelum mereka (penghuni-penghuni surga yang menjadi suami mereka) dan tidak pul' |
| 4 | 'uh oleh manusia sebelum mereka (penghuni-penghuni surga yang menjadi suami mereka) dan tidak pula ol' |
| 4 | 'ah disentuh oleh manusia sebelum mereka (penghuni-penghuni surga yang menjadi suami mereka) dan tida' |
| 4 | 'ak pernah disentuh oleh manusia sebelum mereka (penghuni-penghuni surga yang menjadi suami mereka) d' |
| 4 | 'ernah disentuh oleh manusia sebelum mereka (penghuni-penghuni surga yang menjadi suami mereka) dan t' |
| 3 | 'manusia sebelum mereka (penghuni-penghuni surga yang menjadi suami mereka) dan tidak pula oleh jin.' |
| 3 | 'tidak pernah disentuh oleh manusia sebelum mereka (penghuni-penghuni surga yang menjadi suami mereka' |
| 3 | 'tidak pernah disentuh oleh manusia sebelum mereka (penghuni-penghuni surga yang menjadi suami merek' |

## Acknowledgment

Thanks to the contributors of the following projects:

- [text-dedup](https://github.com/ChenghaoMou/text-dedup)
- [exact-dedup](https://github.com/google-research/deduplicate-text-datasets)
- [bigscience-data-preparation](https://github.com/bigscience-workshop/data-preparation)
- [bigscience-data-tooling](https://github.com/bigscience-workshop/data_tooling)

## Citing this work

If you use this repository or sailor models, please cite

```
@misc{dou2024sailor,
      title={Sailor: Open Language Models for South-East Asia}, 
      author={Longxu Dou and Qian Liu and Guangtao Zeng and Jia Guo and Jiahui Zhou and Wei Lu and Min Lin},
      year={2024},
      eprint={2404.03608},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

## Contact

If you have any questions, please raise an issue on our GitHub repository or contact <a href="mailto:doulx@sea.com">doulx@sea.com</a>.
