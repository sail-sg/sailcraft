### SailCraft

This repo provides the data process pipeline for large language model training.
It consists of data cleaning, near deduplication and exact deduplication.

### Requirements

```
pip install -r requirements.txt
mkdir lm_resource 
python data_cleaning/download_sentencepiece_kenlm_models.py --output_dir_path lm_resource
```

### Quickstart

```
bash run_example.sh
```


### Case Studies

1. for data cleaning, check the `code/data_cleaning/filtering_logs` for each filter.
2. run `exact_dedup/scripts/count_topk_occurrences.py` to obtain the top-k occurrences.


### Acknowledgement

Thanks to the contributor of the following projects: 
[text-dedup](https://github.com/ChenghaoMou/text-dedup),
[exact-dedup](https://github.com/google-research/deduplicate-text-datasets),
[bigscience-data-preparation](https://github.com/bigscience-workshop/data-preparation),
[bigscience-data-tooling](https://github.com/bigscience-workshop/data_tooling).

### Contact 

If you have any questions, please raise an issue in our Github or contact <a href="mailto:doulx@sea.com">doulx@sea.com</a>.