"""
Script to remove duplicate entries from glossary text files.

Make sure text file has been saved as "UTF-8" not "UTF-8(BOM 付き)".
With "UTF-8(BOM 付き)" an extra control char is included at the start of the
file, which can prevent duplicates of the first line being removed.
"""

import os
import sys


input_file_path = sys.argv[1]

with open(input_file_path, 'r', encoding="utf-8") as reader:
    raw_lines = reader.readlines()

# The below approach maintains the same order as in the original file.
cleaned_lines = []
for line in raw_lines:
    if line not in cleaned_lines:
        cleaned_lines.append(line)

# The below approach loses the original order.
# cleaned_lines = set(raw_lines)

input_filename = os.path.splitext(input_file_path)[0]

output_file_path = input_filename + '-duplicates-removed.txt'

with open(output_file_path, 'w', encoding='utf-8') as file:
    file.writelines(cleaned_lines)
