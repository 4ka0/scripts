"""
Script to
- read in the contents of a glossary
- remove duplicates
- sort entries according to the source text
- combine similar entries, and
- write to a new file.
"""

import os
import sys


def read_glossary(input_file_path):
    """ Reads in content from glossary file and removes trailing newline chars
        from each line. """

    with open(input_file_path, 'r', encoding="utf-8") as reader:
        raw_lines = reader.readlines()

    # Remove newline chars
    stripped_lines = [line.rstrip() for line in raw_lines]

    return stripped_lines


def extract_lines(stripped_lines):
    """ Extract lines including two separated by a tab character. Other entries
        are labelled as discarded to be written to a separate file later on. """

    extracted_lines = []  # List of lists
    discarded_lines = []  # List of lists

    for line in stripped_lines:

        split_elems = line.split('\t')

        if len(split_elems) == 2:
            extracted_lines.append(split_elems)
        else:
            discarded_lines.append(split_elems)

    return extracted_lines, discarded_lines


def remove_duplicates(extracted_lines):
    """ Discard all duplicates and only retain unique lines. """

    unique_lines = []  # List of lists

    for line in extracted_lines:
        if line not in unique_lines:
            unique_lines.append(line)

    return unique_lines


def sort_lines(unique_lines):
    """ Sort the unique_lines (list of lists) according to the source text """
    sorted_lines = sorted(unique_lines, key=lambda x: x[0])
    return sorted_lines


def combine_lines(sorted_lines):
    """ Combine similar entries (entries containing same source text and
        different target texts), and output as a dictionary (source text as the
        key and the different targets as values for that key). """

    combined_lines = {}

    for line in sorted_lines:
        if line[0] in combined_lines:
            combined_lines[line[0]] = combined_lines[line[0]] + ', ' + line[1]
        else:
            combined_lines[line[0]] = line[1]

    return combined_lines


def output_to_file(input_file_path, combined_lines, discarded_lines):
    """ combined_lines is written to file as the final reorganized glossary,
        and discarded_lines (lines from the original file not containing 2 or 3
        elements) is written as another file to be manually checked that nothing
        useful has been discarded. """

    # Write combined_lines (dict) to file

    # Build filenames for file to be written
    input_filename = os.path.splitext(input_file_path)[0]
    output_file_path = input_filename + '-reorganized.txt'

    with open(output_file_path, 'w', encoding='utf-8') as file:
        for key, value in combined_lines.items():
            file.write(key + '\t' + value + '\n')

    # Write discarded_lines (list of lists) to file

    output_file_path = input_filename + '-discarded-entries.txt'

    with open(output_file_path, 'w', encoding='utf-8') as file:
        for lst in discarded_lines:
            for item in lst:
                file.write(item + '\t')
            file.write('\n')


def main():
    input_file_path = sys.argv[1]
    stripped_lines = read_glossary(input_file_path)
    extracted_lines, discarded_lines = extract_lines(stripped_lines)
    unique_lines = remove_duplicates(extracted_lines)
    sorted_lines = sort_lines(unique_lines)
    combined_lines = combine_lines(sorted_lines)
    output_to_file(input_file_path, combined_lines, discarded_lines)


if __name__ == '__main__':
    main()
