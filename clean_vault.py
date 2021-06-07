from typing import List
import pandas as pd
import sys
from urllib.parse import urlparse, urlunparse
import os
import re

UNIQUE_COLS_AND = [["login_uri", "login_username"], ["name"]]
DEFAULT_URL_COL = "login_uri"


def clean_url(url):
    if not isinstance(url, str):
        if not pd.isnull(url):
            print(f"Issue with url: {url}")
        return url
    try:
        parsed_url = urlparse(url)
    except Exception as ex:
        print(f"Issue with url: {url}")
        raise ex

    ignored_path_pattern = "signup|register|sign-up"
    ignored_path_re = re.compile(ignored_path_pattern, re.IGNORECASE)

    used_parts = [parsed_url.scheme, parsed_url.netloc, parsed_url.path, "", "", ""]

    if ignored_path_re.search(parsed_url.path):
        used_parts[2] = ""

    return urlunparse(used_parts)


def split_conflicts(df: pd.DataFrame, unique_columns_and: List[List[str]]):
    conflict_list = []
    for idx in range(0, len(unique_columns_and)):
        indexed_cols = unique_columns_and[idx]
        conflict_indices = df.duplicated(subset=indexed_cols, keep=False)
        conflict_indices = conflict_indices & ~(
            df[indexed_cols].isnull() | (df[indexed_cols] == "")
        ).all(axis="columns")
        conflict_list.append(conflict_indices)

    conflict_indices_total = conflict_list[0]
    for idx in range(1, len(unique_columns_and)):
        conflict_indices_total = conflict_indices_total | conflict_list[idx]

    return df[~conflict_indices], df[conflict_indices]


if __name__ == "__main__":
    input_csv = sys.argv[1]
    export_csv = os.path.join(os.getcwd(), "output.csv")
    if len(sys.argv) >= 3:
        export_csv = sys.argv[2]

    url_col = DEFAULT_URL_COL

    vault = pd.read_csv(input_csv)
    vault.loc[:, url_col] = vault[url_col].map(lambda a: clean_url(a))

    vault = vault.drop_duplicates()
    valid, conflicts = split_conflicts(vault, UNIQUE_COLS_AND)

    if len(conflicts) > 0:
        conflicts.to_csv("conflicts.csv", index=False)
        print("There were conflicts found in the vault.")
        print(f"These are stored at {os.path.join(os.getcwd(), 'conflicts.csv')} ")
        input("Resolve these conflicts and then press enter to continue...")
        merged = pd.concat([pd.read_csv("conflicts.csv"), valid], ignore_index=True)
    else:
        merged = valid

    merged.to_csv(export_csv, index=False)
    print(f"Cleaned vault stored at {export_csv}")
