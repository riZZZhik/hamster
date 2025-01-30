import argparse
from pathlib import Path
from warnings import warn

import pandas as pd


def fix_duplicates(
    file_path: Path,
    output_path: Path | None = None,
    delimiter: str = ":",
    file_name_column: str = "file_name",
    directory_column: str = "директория",
):
    df = pd.read_csv(file_path)
    df[file_name_column] = df[file_name_column].astype(str).str.replace("/", delimiter)

    directory_exist = True
    if directory_column not in df.columns:
        directory_exist = False
        warn(
            f"Column '{directory_column}' not found in the input file. Postfix will be added instead."
        )

    duplicate_counts = df[file_name_column].str.lower().value_counts()
    duplicates = duplicate_counts[duplicate_counts > 1].index

    changes = []
    if not duplicates.empty:
        for duplicate in duplicates:
            duplicate_rows = df[df[file_name_column].str.lower() == duplicate.lower()]
            for idx, row in duplicate_rows.iterrows():
                if directory_exist:
                    directory = (
                        row[directory_column].replace("/", delimiter).strip(delimiter)
                    )
                    new_file_name = f"{directory}{delimiter}{row[file_name_column]}"
                else:
                    new_file_name = f"{row[file_name_column]}_{idx}"
                changes.append((row[file_name_column], new_file_name))
                df.at[idx, file_name_column] = new_file_name

    if not output_path:
        output_path = file_path.with_name(f"{file_path.stem}_fixed{file_path.suffix}")
    df.to_csv(output_path, index=False)

    print(f"Number of changes: {len(changes)}")
    print(f"Output file: {output_path}")
    if changes:
        print("Files changed:")
        for old_name, new_name in changes:
            print(f"{old_name} -> {new_name}")

    duplicate_counts = df[file_name_column].str.lower().value_counts()
    duplicates = duplicate_counts[duplicate_counts > 1].index
    if not duplicates.empty:
        print(f"\n{len(duplicates)} duplicates found in the output file:")
        for duplicate in duplicates:
            print(duplicate)


def main():
    parser = argparse.ArgumentParser(
        description="Fix duplicate file names by adding a directory prefix."
    )
    parser.add_argument("file_path", type=Path, help="Path to the input CSV file.")
    parser.add_argument(
        "-o", "--output_path", type=Path, help="Path to save the output CSV file."
    )
    parser.add_argument(
        "-d",
        "--delimiter",
        type=str,
        default=":",
        help="Delimiter to replace '/' in directory names.",
    )
    parser.add_argument(
        "--file_name_column",
        type=str,
        default="file_name",
        help="Name of the column containing file names.",
    )
    parser.add_argument(
        "--directory_column",
        type=str,
        default="директория",
        help="Name of the column containing directory names.",
    )
    args = parser.parse_args()

    fix_duplicates(
        args.file_path,
        args.output_path,
        args.delimiter,
        args.file_name_column,
        args.directory_column,
    )


if __name__ == "__main__":
    main()
