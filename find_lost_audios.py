import argparse
import os

import pandas as pd


def find_missing_files(csv_path, audio_dir):
    df = pd.read_csv(csv_path)
    if "file_name" not in df.columns:
        raise ValueError("CSV file must contain a 'file_name' column.")

    df["file_name"] = df["file_name"].astype(str).str
    csv_files = set(
        df["file_name"].apply(lambda x: f"{x}.wav" if not x.endswith(".wav") else x)
    )

    audio_files = set(os.listdir(audio_dir))
    missing_files = csv_files - audio_files
    if missing_files:
        print(f"Missing {len(missing_files)} files:")
        for file in missing_files:
            print(file)
    else:
        print("No missing files. All audio files are present.")


def main():
    parser = argparse.ArgumentParser(
        description="Find missing audio files from a CSV file."
    )
    parser.add_argument(
        "csv_path",
        type=str,
        help="Path to the CSV file containing the file_name column",
    )
    parser.add_argument(
        "audio_dir", type=str, help="Path to the directory containing audio files"
    )
    args = parser.parse_args()

    find_missing_files(args.csv_path, args.audio_dir)


if __name__ == "__main__":
    main()
