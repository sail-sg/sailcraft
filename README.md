# SailCraft: Data Toolkit for Sailor Language Models

[![Homepage](https://img.shields.io/badge/🏠-Homepage-3C47EB.svg)](https://sea-sailor.github.io/) &nbsp;&nbsp; [![HuggingFace](https://img.shields.io/badge/🤗-HuggingFace-E87948.svg)](https://huggingface.co/sail/Sailor-7B) &nbsp;&nbsp; [![Technical Report](https://img.shields.io/badge/arXiv-2404.03608-b31b1b.svg)](https://arxiv.org/pdf/2404.03608.pdf)




This repository provides a data processing pipeline for large language model training. 
It consists of four stages: initial data cleaning, near deduplication, exact deduplication, and a second round of data cleaning.
The data cleaning part is especially optimized for south-east asian languages (e.g., Thai).

## Requirements

Install the packages and download the models for data cleaning. Here we only download the models for English, Chinese, Thai, Vietnamese, Indonesian, Malay, and Lao. You can add more languages by modifying the `--used_language_ids` parameter. The full language list can be found [here](data_cleaning/languages_id.py).

```
pip install -r requirements.txt
mkdir lm_resource
wget https://huggingface.co/datasets/sail/sailcraft_lm_resource/resolve/main/lid.176.bin -P lm_resource
python code/data_cleaning/download_sentencepiece_kenlm_models.py --used_language_ids en zh th vi id ms lo --output_dir_path lm_resource
```

Install Rust for exact deduplication, refer to [this guidance](https://github.com/google-research/deduplicate-text-datasets#installing) for more details.

```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
. "$HOME/.cargo/env"
```

## Quickstart

We sample 1,000 lines from the [cc100 Indonesian subset](https://data.statmt.org/cc-100/) for a preliminary analysis.

Execute the script by running:
```
bash run_example.sh
```

Upon successful execution, you should observe the following logs indicating the processing stages:

```
Counting lines in cleaned data output: 987
Counting lines in near deduplication output: 974
Counting lines in exact deduplication output: 963
Counting lines in final output: 949
```

This output confirms the sequential filtering and deduplication stages of the dataset.
The final output can be accessed at `data/data_output/final_output/sample/data_clean.jsonl`.

## Running with Your Own Dataset

To integrate your own dataset into the project, follow these steps:

1. **Prepare Your Dataset**: Place your dataset file, named `ALIAS.jsonl`, in the `./data/data_input/` directory.
2. **Configure Script Variables**: Adjust the `ALIAS` and `LANGUAGE` variables in the `./run_example.sh` script to correspond with your dataset details.

### Parameter Settings
Ensure proper configuration of the processes by setting the following parameters:

1. **Data Cleaning**: Set the parameters for each filter. Detailed configuration can be found [here](https://github.com/sail-sg/sailcraft/blob/main/code/data_cleaning/parameters_filtering.py).
2. **Near Deduplication**: Specify the number of permutations to use in MinHash by referring to the example [here](https://github.com/sail-sg/sailcraft/blob/c98a10458a92514d9922fa01a5f3ede631c546ac/code/near_dedup/run_example.sh#L22).
3. **Exact Deduplication**: Define the identified substrings of the given length as shown in the example [here](https://github.com/sail-sg/sailcraft/blob/c98a10458a92514d9922fa01a5f3ede631c546ac/code/exact_dedup/run_example.sh#L18).


## Case Studies

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

| Count | Span |
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

@article{sailor2report,
title  = {Sailor2: Sailing in South-East Asia with Inclusive Multilingual LLM},
author = {Longxu Dou and Qian Liu and Fan Zhou and Changyu Chen and Zili Wang and Ziqi Jin and Zichen Liu and Tongyao Zhu and Cunxiao Du and Penghui Yang and Haonan Wang and Jiaheng Liu and Yongchi Zhao and Xiachong Feng and Xin Mao and Man Tsung Yeung and Kunat Pipatanakul and Fajri Koto and Min Si Thu and Hynek Kydl{\'\i}{\v{c}}ek and Zeyi Liu and Qunshu Lin and Sittipong Sripaisarnmongkol and Kridtaphad Sae-Khow and Nirattisai Thongchim and Taechawat Konkaew and Narong Borijindargoon and Anh Dao and Matichon Maneegard and Phakphum Artkaew and Zheng-Xin Yong and Quan Nguyen and Wannaphong Phatthiyaphaibun and Hoang H. Tran and Mike Zhang and Shiqi Chen and Tianyu Pang and Chao Du and Xinyi Wan and Wei Lu and Min Lin},
journal={arXiv preprint arXiv:2502.12982},
year   = {2025}
}

```
@inproceedings{sailor1report,
    title = "Sailor: Open Language Models for South-{E}ast {A}sia",
    author = "Dou, Longxu and Liu, Qian and Zeng, Guangtao and Guo, Jia  and Zhou, Jiahui and Mao, Xin and Jin, Ziqi and Lu, Wei and Lin, Min",
    booktitle = "Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: System Demonstrations",
    year = "2024",
}
```

## Contact

If you have any questions, please raise an issue on our GitHub repository or contact <a href="mailto:doulx@sea.com">doulx@sea.com</a>.
