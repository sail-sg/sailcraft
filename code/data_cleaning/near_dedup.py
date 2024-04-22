from tqdm import tqdm
from datasets import load_dataset, load_from_disk
import pyarrow as pa
import os
import shutil
import json
import argparse
import subprocess
from write_arrow_to_jsonl import write_arrow_to_jsonl

def run_cmd(cmd):
  try:
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
  except subprocess.CalledProcessError as e:
      print("Error executing command:", e)
      print("Return code:", e.returncode)
      print("Error output:", e.stderr)


if __name__ == "__main__":
  # parser = argparse.ArgumentParser()
  # parser.add_argument('--llama_tokenizer_dir', default='llama2_tokenizer.model', type=str)
  # parser.add_argument('--indonesian_sp_model_file', default='indo4b_ind_30k.model', type=str)
  # parser.add_argument('--output_folder', type=str, required=True)
  # args = parser.parse_args()

  cache_path="/home/aiops/doulx/code/sailor_data_script/cache/near_dedup_cache"
  cache_path = os.path.abspath(cache_path)

  input_path = '/home/aiops/doulx/code/sailor_data_script/data/data_output/cleaned_data_output/sample/data_clean.jsonl'
  output_path = '/home/aiops/doulx/code/sailor_data_script/data/data_output/near_dedup_output/sample'

  command = [
      'python', '-m', 'text_dedup.minhash',
      '--path', 'json',
      '--name', 'data_clean',
      '--data_files', input_path,
      '--cache_dir', cache_path,
      '--output', output_path,
      '--column', 'text',
      '--split', 'train',
      '--batch_size', '10000',
      '--num_perm', '256'
  ]

  run_cmd(command)
  write_arrow_to_jsonl(output_path)
