#!/bin/bash

# Default values
INPUT_DIR=$(pwd)
FORMAT="pcm_s16le"
SAMPLERATE="8000"
OUTPUT_DIR=""

# Function to display help message
show_help() {
    echo "Usage: $(basename "$0") [OPTIONS] [DIRECTORY]"
    echo "Recursively converts WAV files in the specified directory to the desired format."
    echo "If no directory is provided, the current directory is used."
    echo "Converted files are saved in a '_fixed' subdirectory unless specified otherwise."
    echo -e "\nOptions:"
    echo "  --format TYPE     Specify audio format (default: pcm_s16le)."
    echo "  --samplerate HZ   Set the audio sample rate (default: 8000 Hz)."
    echo "  --output_dir DIR  Specify the output directory (default: INPUT_DIR_fixed)."
    echo "  --help            Show this help message and exit."
    exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
    --help)
        show_help
        ;;
    --format)
        FORMAT="$2"
        shift 2
        ;;
    --samplerate)
        SAMPLERATE="$2"
        shift 2
        ;;
    --output_dir)
        OUTPUT_DIR="$2"
        shift 2
        ;;
    *)
        INPUT_DIR="$1"
        shift
        ;;
    esac
done

# Set default output directory if not specified
if [ -z "$OUTPUT_DIR" ]; then
    OUTPUT_DIR="${INPUT_DIR}_fixed"
fi
mkdir -p "$OUTPUT_DIR"

# Recursively find all WAV files
find "$INPUT_DIR" -type f -iname "*.wav" | while read -r file; do
    # Preserve directory structure
    relative_path="${file#"$INPUT_DIR"/}"
    output_file="$OUTPUT_DIR/${relative_path%.*}.wav"
    output_dir="$(dirname "$output_file")"
    mkdir -p "$output_dir"

    if ffmpeg -nostdin -loglevel quiet -i "$file" -acodec "$FORMAT" -ac 1 -ar "$SAMPLERATE" "$output_file"; then
        echo "Converted: $file -> $output_file"
    else
        echo "Failed to convert: $file"
    fi

done

echo -e "\nConverted from $INPUT_DIR to $OUTPUT_DIR with the following settings:"
echo "Audio format: $FORMAT"
echo "Sample rate: $SAMPLERATE Hz"

original_count=$(find "$INPUT_DIR" -type f -iname "*.wav" | wc -l)
converted_count=$(find "$OUTPUT_DIR" -type f -iname "*.wav" | wc -l)

if [ "$original_count" -eq "$converted_count" ]; then
    echo "All $original_count files converted successfully."
else
    echo "Only $converted_count out of $original_count files were converted."
fi
