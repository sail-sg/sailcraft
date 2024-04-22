from tqdm import tqdm
from datasets import load_dataset
import os
import glob
import shutil
import json
import argparse


def write_arrow_to_jsonl(folder_path):
    ### (1) delete dataset_info.json and state.json
    json_files = glob.glob(os.path.join(folder_path, '*.json'))
    for file_path in json_files:
        os.remove(file_path)

    ### (2) make directory named `arrows`, then place all arrows file into `arrows`
    arrows_folder = os.path.join(folder_path, 'arrows')
    if not os.path.exists(arrows_folder):
        os.makedirs(arrows_folder)
    arrow_files = glob.glob(os.path.join(folder_path, '*arrow'))

    for file_path in arrow_files:
        destination_path = os.path.join(arrows_folder, os.path.basename(file_path))
        shutil.move(file_path, destination_path)

    ### (3) read lines from arrow file, and write line to the jsonl file
    arrow_files = glob.glob(os.path.join(arrows_folder, '*arrow'))
    # print(data_files)

    dataset = load_dataset(
        path = os.path.join(folder_path, 'arrows'),
        data_files=arrow_files,   
        split = 'train',
        num_proc = 64,
    )

    output_file = os.path.join(folder_path, 'data_clean.jsonl')
    with open(output_file, 'w') as f:
        for idx in tqdm(range(len(dataset))):
            json.dump({"text": dataset[idx]['text']}, f, ensure_ascii=False)
            f.write('\n')

    # output_file = os.path.join(folder_path, 'data_clean_para_level.jsonl')
    # with open(output_file, 'w', encoding='utf-8') as f:
    #     num_iterations = len(dataset) // 5 + (1 if len(dataset) % 5 != 0 else 0)
        
    #     for i in tqdm(range(num_iterations)):
    #         start_index = i * 5
    #         end_index = min((i + 1) * 5, len(dataset))
    #         combined_text = '\n'.join([dataset[idx]['text'] for idx in range(start_index, end_index)])
    #         json.dump({"text": combined_text}, f, ensure_ascii=False)
    #         f.write('\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder_path', default='data_output/after_cleaned_data_output/sample', type=str)
    args = parser.parse_args()

    folder_path = args.folder_path
    folder_path = os.path.abspath(folder_path)

    write_arrow_to_jsonl(folder_path)
