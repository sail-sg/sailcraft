"""Download Sentencepiece and KenLM models for supported languages.

Usage:
    python download_sentencepiece_kenlm_models.py --output_dir_path /tmp/

All Sentencepiece and KenLM language models will be saved under /tmp.
"""

### To download the sentencepiece model and kenlm model, you have two options:
### (1) download from huggingface:
### https://huggingface.co/datasets/sail/sailcraft_lm_resource
### (2) run `python download_sentencepiece_kenlm_models.py`

import argparse
import subprocess
from typing import List
from languages_id import langs_id
import os

def download_sentencepiece_kenlm_models(used_language_ids: List[str], output_dir_path: str) -> None:
    supported_sentencepiece_langs = langs_id["sentencepiece_id"].dropna().unique()
    # take the intersection of supported languages and used languages
    download_language_ids = list(set(supported_sentencepiece_langs) & set(used_language_ids))
    for lang in download_language_ids:
        try:
            print("Downloading Sentencepiece model for language ", lang, "...")
            if os.path.exists(f"{output_dir_path}/{lang}.sp.model"):
                os.remove(f"{output_dir_path}/{lang}.sp.model")
            output_sentencepiece = subprocess.check_output(
                f"wget https://huggingface.co/datasets/sail/sailcraft_lm_resource/resolve/main/{lang}.sp.model -P {output_dir_path}",  # http://dl.fbaipublicfiles.com/cc_net/lm/{lang}.sp.model for FB models
                shell=True,
            )
        except Exception as e:
            print(
                f"Warning: Download failed for Sentencepiece model for language {lang}."
            )
    
    for lang in download_language_ids:
        try:
            print("Downloading KenLM model for language ", lang, "...")
            # if exists, remove the existing model
            if os.path.exists(f"{output_dir_path}/{lang}.arpa.bin"):
                os.remove(f"{output_dir_path}/{lang}.arpa.bin")
            output_kenlm = subprocess.check_output(
                f"wget https://huggingface.co/datasets/sail/sailcraft_lm_resource/resolve/main/{lang}.arpa.bin -P {output_dir_path}",  # http://dl.fbaipublicfiles.com/cc_net/lm/{lang}.arpa.bin for FB models
                shell=True,
            )
        except Exception as e:
            print(f"Warning: Download failed for KenLM model for language {lang}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download Sentencepiece and KenLM models for supported languages."
    )
    parser.add_argument('--used_language_ids', metavar='N', type=str, nargs='*',
                        help='A list of language IDs (e.g., `en id th`). Use spaces to separate multiple IDs.')
    parser.add_argument(
        "--output_dir_path",
        type=str,
        default="lm_resource",
        help="Output directory path to save models.",
    )
    args = parser.parse_args()

    download_sentencepiece_kenlm_models(used_language_ids=args.used_language_ids,
                                        output_dir_path=args.output_dir_path)
