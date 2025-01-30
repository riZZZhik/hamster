import argparse

import pandas as pd


def check_duplicates(filepath: str, column: str):
    try:
        df = pd.read_csv(filepath)
        if column not in df.columns:
            print(f"Error: Column '{column}' not found in CSV file.")
            return

        duplicates = df[df.duplicated(subset=[column], keep=False)]
        if duplicates.empty:
            print("No duplicates found.")
        else:
            print("Duplicates found:")
            print(duplicates)
    except Exception as e:
        print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Check for duplicate values in a CSV file column."
    )
    parser.add_argument("filepath", type=str, help="Path to the CSV file")
    parser.add_argument("column", type=str, help="Column name to check for duplicates")
    args = parser.parse_args()

    check_duplicates(args.filepath, args.column)


if __name__ == "__main__":
    main()
