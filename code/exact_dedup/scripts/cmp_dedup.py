import argparse

def read_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

def find_deleted_lines(original_path, deduped_path):
    original_lines = read_jsonl(original_path)
    deduped_lines = read_jsonl(deduped_path)
    deduped_set = set(deduped_lines)
    deleted_lines = [line for line in original_lines if line not in deduped_set]
    print(f"Total deleted lines: {len(deleted_lines)}")
    if len(deleted_lines) > 0:
        print("Deleted lines:")
        for line in deleted_lines:
            print(line)

    return deleted_lines

def main():
    parser = argparse.ArgumentParser(description='Compare two JSONL files to find deleted lines.')
    parser.add_argument('original_file', help='Path to the original JSONL file')
    parser.add_argument('deduped_file', help='Path to the deduplicated JSONL file')
    args = parser.parse_args()

    deleted_lines = find_deleted_lines(args.original_file, args.deduped_file)


if __name__ == '__main__':
    main()
