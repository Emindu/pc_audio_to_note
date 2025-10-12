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
date_display=$(date +"%B %d, %Y")  # Human readable date
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
cp note_data.js "$target_path/" && echo "✅ Copied note_data.js"
cp note.md "$target_path/" && echo "✅ Copied note.md"

# Function to create/update root index.html
create_root_index() {
    local index_file="$MINDMAP_REPO_PATH/index.html"
    
    cat > "$index_file" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mind Map Repository</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #343541;
            color: #ececf1;
            margin: 0;
            padding: 40px 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            color: #7a7d9c;
        }
        .subtitle {
            font-size: 1.1em;
            color: #a0a2b0;
            margin-bottom: 40px;
        }
        .date-list {
            list-style: none;
            padding: 0;
        }
        .date-item {
            background-color: #4b4e5a;
            margin-bottom: 15px;
            border-radius: 8px;
            border: 1px solid #636675;
            transition: all 0.2s ease;
        }
        .date-item:hover {
            background-color: #5d5f7b;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        .date-link {
            display: block;
            padding: 20px 25px;
            color: #ececf1;
            text-decoration: none;
            font-size: 1.2em;
            font-weight: 600;
        }
        .date-link:hover {
            color: #ffffff;
        }
        .no-dates {
            text-align: center;
            padding: 60px 20px;
            color: #a0a2b0;
            font-size: 1.1em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Mind Map Repository</h1>
        <p class="subtitle">Browse your mind maps by date</p>
        <ul class="date-list" id="dateList">
            <!-- Date folders will be listed here -->
        </ul>
        <div class="no-dates" id="noDates" style="display: none;">
            No mind maps created yet. Start recording to create your first mind map!
        </div>
    </div>
    <script>
        // Auto-populate from directory structure
        const dateList = document.getElementById('dateList');
        const noDates = document.getElementById('noDates');
        
        // This will be populated by the script
        const dates = [
EOF

    # Add date entries (list all date directories)
    local first=true
    for date_dir in "$MINDMAP_REPO_PATH"/[0-9]*; do
        if [ -d "$date_dir" ]; then
            local date_name=$(basename "$date_dir")
            if [ "$first" = true ]; then
                first=false
            else
                echo "," >> "$index_file"
            fi
            echo -n "            \"$date_name\"" >> "$index_file"
        fi
    done
    
    cat >> "$index_file" << 'EOF'

        ];
        
        if (dates.length === 0) {
            noDates.style.display = 'block';
        } else {
            dates.sort().reverse().forEach(date => {
                const li = document.createElement('li');
                li.className = 'date-item';
                
                // Format date for display
                const dateObj = new Date(
                    date.substring(4, 8),  // year
                    date.substring(2, 4) - 1,  // month (0-indexed)
                    date.substring(0, 2)   // day
                );
                const displayDate = dateObj.toLocaleDateString('en-US', { 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric' 
                });
                
                li.innerHTML = `<a href="${date}/index.html" class="date-link">📅 ${displayDate}</a>`;
                dateList.appendChild(li);
            });
        }
    </script>
</body>
</html>
EOF
    
    echo "✅ Updated root index.html"
}

# Function to create/update date folder index.html
create_date_index() {
    local date_path="$MINDMAP_REPO_PATH/$date_folder"
    local index_file="$date_path/index.html"
    
    cat > "$index_file" << EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mind Maps - $date_display</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #343541;
            color: #ececf1;
            margin: 0;
            padding: 40px 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .breadcrumb {
            margin-bottom: 30px;
            font-size: 0.95em;
        }
        .breadcrumb a {
            color: #7a7d9c;
            text-decoration: none;
        }
        .breadcrumb a:hover {
            color: #a0a2b0;
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            color: #7a7d9c;
        }
        .subtitle {
            font-size: 1.1em;
            color: #a0a2b0;
            margin-bottom: 40px;
        }
        .topic-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            list-style: none;
            padding: 0;
        }
        .topic-card {
            background-color: #4b4e5a;
            border-radius: 8px;
            border: 1px solid #636675;
            transition: all 0.2s ease;
            overflow: hidden;
        }
        .topic-card:hover {
            background-color: #5d5f7b;
            transform: translateY(-3px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.3);
        }
        .topic-link {
            display: block;
            padding: 25px;
            color: #ececf1;
            text-decoration: none;
        }
        .topic-title {
            font-size: 1.3em;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .topic-subtitle {
            font-size: 0.9em;
            color: #a0a2b0;
        }
        .no-topics {
            text-align: center;
            padding: 60px 20px;
            color: #a0a2b0;
            font-size: 1.1em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="breadcrumb">
            <a href="../index.html">← Back to all dates</a>
        </div>
        <h1>📚 Mind Maps</h1>
        <p class="subtitle">$date_display</p>
        <ul class="topic-grid" id="topicList">
            <!-- Topics will be listed here -->
        </ul>
        <div class="no-topics" id="noTopics" style="display: none;">
            No topics yet for this date.
        </div>
    </div>
    <script>
        const topicList = document.getElementById('topicList');
        const noTopics = document.getElementById('noTopics');
        
        // Topics list
        const topics = [
EOF

    # Add topic entries (list all topic directories)
    local first=true
    for topic_dir in "$date_path"/*/; do
        if [ -d "$topic_dir" ]; then
            local topic_name=$(basename "$topic_dir")
            # Skip the current directory
            if [ "$topic_name" != "*" ]; then
                if [ "$first" = true ]; then
                    first=false
                else
                    echo "," >> "$index_file"
                fi
                echo -n "            {\"id\": \"$topic_name\", \"title\": \"$topic_name\"}" >> "$index_file"
            fi
        fi
    done
    
    cat >> "$index_file" << 'EOF'

        ];
        
        if (topics.length === 0) {
            noTopics.style.display = 'block';
        } else {
            topics.forEach(topic => {
                const li = document.createElement('li');
                li.className = 'topic-card';
                
                // Format title (replace underscores with spaces)
                const displayTitle = topic.title.replace(/_/g, ' ');
                
                li.innerHTML = `
                    <a href="${topic.id}/index.html" class="topic-link">
                        <div class="topic-title">🗺️ ${displayTitle}</div>
                        <div class="topic-subtitle">View mind map & notes</div>
                    </a>
                `;
                topicList.appendChild(li);
            });
        }
    </script>
</body>
</html>
EOF
    
    echo "✅ Updated date index.html"
}

# Update index files
echo ""
echo "📄 Updating index files..."
create_root_index
create_date_index

echo ""
echo "================================================"
echo "✅ Files saved to: $target_path"
echo "================================================"
echo ""

# Git operations
echo ""
echo "📦 Git operations..."
cd "$MINDMAP_REPO_PATH"

# Check if it's a git repository
if [ ! -d ".git" ]; then
    echo "⚠️  Not a git repository. Initializing..."
    git init
    echo "✅ Git repository initialized"
fi

# Add all changes
echo "Adding changes..."
git add .

# Create commit message
commit_message="Add mindmap: $root_filename ($date_display)"

# Commit changes
echo "Committing changes..."
if git commit -m "$commit_message"; then
    echo "✅ Changes committed: $commit_message"
    
    # Push to remote (if configured)
    echo "Pushing to remote..."
    if git push 2>/dev/null; then
        echo "✅ Changes pushed to remote"
    else
        echo "⚠️  Push failed. You may need to configure remote or push manually."
        echo "💡 Run: cd $MINDMAP_REPO_PATH && git remote add origin <your-repo-url>"
    fi
else
    echo "ℹ️  No changes to commit"
fi

echo ""
echo "================================================"
echo "✅ All operations complete!"
echo "================================================"
echo ""

# Open the mindmap HTML from the new location
open "$target_path/index.html"
