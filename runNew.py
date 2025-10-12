#!/bin/bash
# Adding activating venv
source .venv/bin/activate

# Configuration
MINDMAP_REPO_PATH="/Users/eminduperera/dev/mindmap_repo"  # Change this to your desired path

# Record audio
python record.py

# # Convert audio to text
python text.py

# Generate mindmap JSON and capture root node filename
echo "Generating mindmap..."
output=$(python create_json.py)
echo "$output"

python create_notes.py


# Extract the root node filename (last line of output)
root_filename=$(echo "$output" | tail -1 | xargs)

echo ""
echo "================================================"
echo "Captured root node filename: $root_filename"
echo "================================================"
echo ""

# Create date folder (ddMMYYYY format)
date_folder=$(date +"%d%m%Y")
echo "📅 Date folder: $date_folder"

# Create full path: REPO_PATH/ddMMYYYY/root_filename
target_path="$MINDMAP_REPO_PATH/$date_folder/$root_filename"
echo "📁 Target path: $target_path"

# Create directories if they don't exist
if [ ! -d "$MINDMAP_REPO_PATH" ]; then
    echo "Creating mindmap repository at: $MINDMAP_REPO_PATH"
    mkdir -p "$MINDMAP_REPO_PATH"
fi

if [ ! -d "$MINDMAP_REPO_PATH/$date_folder" ]; then
    echo "Creating date folder: $date_folder"
    mkdir -p "$MINDMAP_REPO_PATH/$date_folder"
fi

if [ ! -d "$target_path" ]; then
    echo "Creating topic folder: $root_filename"
    mkdir -p "$target_path"
else
    echo "⚠️  Topic folder already exists, files will be overwritten"
fi

# Copy files to target location
echo ""
echo "📋 Copying files..."
cp index.html "$target_path/" && echo "✅ Copied index.html"
cp mindmap_data.js "$target_path/" && echo "✅ Copied mindmap_data.js"
cp note.md "$target_path/" && echo "✅ Copied note.md"

echo ""
echo "================================================"
echo "✅ Files saved to: $target_path"
echo "================================================"
echo ""

# Open the mindmap HTML from the new location
open "$target_path/index.html"
