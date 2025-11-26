# Shared Variants in COVID Diseases

This script identifies shared genetic variants between severe COVID and long COVID
based on provided CSV files containing selected features for each condition.

## Requirements

- Python 3.x
- pandas library

## Usage

Run the script using Python:

```bash
    python main.py file1.csv file2.csv
```

Replace `file1.csv` and `file2.csv` with the paths to your CSV files containing selected features for severe COVID and long COVID, respectively. The CSV files should have a column named `selected_features` containing the genetic variants and other named `n_features` containing the total number of features.
