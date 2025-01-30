import argparse
import shutil
from pathlib import Path

import pandas as pd


def load_mapping(csv_path, column):
    df = pd.read_csv(
        csv_path, dtype={"phrase_code": str}
    )  # Ensure phrase_code is treated as string
    mapping = df.set_index("phrase_code")[column].to_dict()
    return mapping


def rename_and_copy_files(input_folder, output_folder, mapping):
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    total_input_files = len(list(input_folder.glob("*.wav")))
    print(f"Total files in input folder: {total_input_files}")

    for file in input_folder.glob("*.wav"):
        phrase_code = str(
            int(file.stem)
        )  # Convert to int and back to remove leading zeros

        if phrase_code in mapping:
            sanitized_name = mapping[phrase_code]  # .replace("/", ":")

            new_name = f"{sanitized_name}{file.suffix}"
            dest_path = output_folder / new_name

            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(file, dest_path)
            print(f"Copied: {file.name} -> {new_name}")
        else:
            print(f"Warning: No mapping found for {file.name}, skipping.")

    total_output_files = len(list(output_folder.rglob("*.wav")))
    print(f"Total files in input folder: {total_input_files}")
    print(f"Total files in output folder: {total_output_files}")
    if total_input_files != total_output_files:
        raise ValueError(
            "Mismatch between input and output file counts! Check for missing or skipped files."
        )


def main():
    parser = argparse.ArgumentParser(
        description="Rename and copy WAV files based on a CSV mapping."
    )
    parser.add_argument(
        "input_folder", help="Path to the input folder containing WAV files."
    )
    parser.add_argument(
        "csv_path", help="Path to the CSV file with phrase_code to name mapping."
    )
    parser.add_argument(
        "--output_folder",
        help="Path to the output folder (default: input_folder with _fixed appended).",
        default=None,
    )
    parser.add_argument(
        "--column",
        help="Column name in CSV to use for renaming (default: name).",
        default="name",
    )
    args = parser.parse_args()

    input_folder = Path(args.input_folder).resolve()
    output_folder = (
        Path(args.output_folder).resolve()
        if args.output_folder
        else input_folder.with_name(f"{input_folder.name}_fixed")
    )
    column = args.column

    mapping = load_mapping(args.csv_path, column)
    rename_and_copy_files(input_folder, output_folder, mapping)

    print("Processing completed.")


if __name__ == "__main__":
    main()
