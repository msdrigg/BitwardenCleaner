# BitwardenCleaner

This repository will safely clean your bitwarden vault csv. 

## Installation
  1. Clone this repository
  2. Install python on your system
  3. Install pandas using `python -m pip install pandas`

## Usage
  1. Export Bitwarden vault to a csv file.
  2. Run `python clean_vault.py path/to/vault.csv`
  3. Fix conflicts found in `conflicts.csv`. This means deleting duplicates and leaving in desired rows.
  4. The output vault is stored in `output.csv`.

## Warnings and Risks
Please use at your own risk. By default, urls are changed to
  1. Remove query parameters
  2. Remove url paths that look like signin paths

This script makes no connection to the internet so there is no risk of any vault secrets being stolen.
