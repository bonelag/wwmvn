##
# Copyright (c) 2025 und3fy.dev. All rights reserved.
# Created by und3fined <me@und3fy.dev> on 2025 Nov 26.
##

import json
import os
import sys

def merge_text_files(base_dir, patch_dir):
    merged_data = {}
    
    text_dir = os.path.join(base_dir, 'text')
    output_file = os.path.join(base_dir, 'entries.json')

    # merge original data first
    for filename in os.listdir(text_dir):
        if filename.endswith('.json'):
            orig_filepath = os.path.join(text_dir, filename)
            with open(orig_filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                merged_data.update(data)

    # apply patches
    for filename in os.listdir(patch_dir):
        if filename.endswith('.json'):
            try:
                patch_filepath = os.path.join(patch_dir, filename)
                with open(patch_filepath, 'r', encoding='utf-8') as f:
                    patch_data = json.load(f)
                    # check key in has in merged_data then update, else add skip
                    for key, value in patch_data.items():
                        if key in merged_data:
                            if isinstance(value, str):
                                merged_data[key] = value
                            elif isinstance(value, list) and len(value) > 0:
                                merged_data[key] = value[-1]
                            elif isinstance(value, dict) and len(value) > 0:
                                last_key = list(value.keys())[-1]
                                merged_data[key] = value[last_key]

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from `{filename}`: {e}")

    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python merge-text.py <base_dir> <patch_dir>")
        sys.exit(1)
    
    base_dir = sys.argv[1]
    patch_dir = sys.argv[2]
    
    merge_text_files(base_dir, patch_dir)
    print(f"Merged text files {patch_dir} into {base_dir}/entries.json")