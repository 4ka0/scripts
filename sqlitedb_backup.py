"""
Script to back up an SQLite database used in a Django app.
Copies the database file from one directory to another directory, extracts
the content of the database file (in this case glossaries and translations)
in a human-readable form (text files), and adds to a backup log whenever a
backup is made. Any errors are output as a text file to a desired location.
"""

import os
import sqlite3
import operator
import itertools
from shutil import copyfile
from datetime import datetime


SOURCE_DB = "<path>/db.sqlite3"
BACKUP_DB = "<path>/db.sqlite3"
BACKUP_LOG = "<path>/backup-log.txt"
GLOSSARY_OUTPUT_PATH = "<path>/extracted_glossary_files"
TRANSLATION_OUTPUT_PATH = "<path>/extracted_translation_files"
ERROR_LOG = "<path>/backup-error.txt"
ERRORS = []
NOW = str(datetime.now())


def copy_db():
    try:
        copyfile(SOURCE_DB, BACKUP_DB)
    except Exception as e:
        ERRORS.append("copy_db(): " + str(e))


def update_log():
    try:
        size = str(os.path.getsize(SOURCE_DB))
        with open(BACKUP_LOG, "a+") as f:
            f.write("Backup date/time: " + NOW + "\n")
            f.write("Backed up DB size (bytes): " + size + "\n\n")
    except Exception as e:
        ERRORS.append("update_log(): " + str(e))


def connect_to_db():
    try:
        con = sqlite3.connect(SOURCE_DB)
    except Exception as e:
        ERRORS.append("connect_to_db(): " + str(e))
    cur = con.cursor()
    return con, cur


def extract_glossaries_from_db(cursor):
    if not os.path.exists(GLOSSARY_OUTPUT_PATH):
        os.makedirs(GLOSSARY_OUTPUT_PATH)
    glossary_names_obj = cursor.execute("SELECT id, title FROM archive_glossary ORDER BY id;")
    glossary_names_dict = dict(glossary_names_obj)
    entries = cursor.execute(
        "SELECT glossary_id, source, target, notes FROM archive_entry ORDER BY glossary_id;"
    )
    for key, group in itertools.groupby(entries, operator.itemgetter(0)):
        glossary_name = glossary_names_dict.get(key, "Untitled")
        filename = f"{GLOSSARY_OUTPUT_PATH}/{glossary_name}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                for entry_tuple in group:
                    for item in entry_tuple[1:]:
                        cleaned_item = str(item).replace("\r\n", "/")
                        f.write(cleaned_item + "\t")
                    f.write("\n")
        except Exception as e:
            ERRORS.append("extract_glossaries_from_db(): " + str(e))


def extract_translations_from_db(cursor):
    translation_names_obj = cursor.execute(
        "SELECT id, job_number FROM archive_translation ORDER BY id;"
    )
    translation_names_dict = dict(translation_names_obj)
    segments_obj = cursor.execute(
        "SELECT translation_id, source, target FROM archive_segment ORDER BY translation_id;"
    )
    if not os.path.exists(TRANSLATION_OUTPUT_PATH):
        os.makedirs(TRANSLATION_OUTPUT_PATH)
    for key, group in itertools.groupby(segments_obj, operator.itemgetter(0)):
        glossary_name = translation_names_dict.get(key, "Untitled")
        filename = f"{TRANSLATION_OUTPUT_PATH}/{glossary_name}.txt"
        segments_list = list(group)
        try:
            with open(filename, "w", encoding="utf-8") as f:
                for segment in segments_list:
                    for item in segment[1:]:
                        f.write(str(item) + "\t")
                    f.write("\n")
        except Exception as e:
            ERRORS.append("extract_glossaries_from_db(): " + str(e))


def output_errors():
    with open(ERROR_LOG, "a+") as f:
        f.write("-----\n")
        f.write(NOW + "\n")
        for count, error in enumerate(ERRORS):
            f.write(f"Error {count + 1}:\n")
            f.write(error + "\n")


def main():
    copy_db()
    update_log()
    con, cur = connect_to_db()
    extract_glossaries_from_db(cur)
    extract_translations_from_db(cur)
    con.close()
    if ERRORS:
        output_errors()


if __name__ == "__main__":
    main()
