import ollama
import json
from datetime import datetime

def read_transcript(file_path):
    """Read the transcript from the text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None

def format_mindmap_prompt(transcript):
    """Format the prompt for generating mind map JSON from transcript."""
    return f"""# Transcript to Mind Map JSON Converter

You are an expert at analyzing educational transcripts and converting them into hierarchical mind map structures. Your task is to transform the given transcript into a JSON format suitable for mind map visualization.

## CRITICAL: You MUST use this EXACT structure for each node

DO NOT create objects with "id" as numbers or with "content" fields!
DO NOT create a simple list of transcript segments!

Each object MUST have EXACTLY these fields (no more, no less):
- "id": string (unique identifier like "root", "topic1", "subtopic1")
- "text": string (short label, 3-8 words)
- "parent": null OR string (parent's id, null ONLY for root node)
- "level": number (0 for root, 1 for main topics, 2+ for subtopics)
- "position": object {{ "x": number, "y": number }}
- "isCollapsed": boolean (always false)

### Example showing CORRECT transformation:

Input transcript: "SVG paths. There are curves. Quadratic Bezier uses one control point. Cubic Bezier uses two control points."

CORRECT output:
[
  {{
    "id": "root",
    "text": "SVG Paths",
    "parent": null,
    "level": 0,
    "position": {{ "x": 100, "y": 300 }},
    "isCollapsed": false
  }},
  {{
    "id": "curves",
    "text": "Curves",
    "parent": "root",
    "level": 1,
    "position": {{ "x": 400, "y": 250 }},
    "isCollapsed": false
  }},
  {{
    "id": "quadratic",
    "text": "Quadratic Bezier",
    "parent": "curves",
    "level": 2,
    "position": {{ "x": 700, "y": 200 }},
    "isCollapsed": false
  }},
  {{
    "id": "cubic",
    "text": "Cubic Bezier",
    "parent": "curves",
    "level": 2,
    "position": {{ "x": 700, "y": 300 }},
    "isCollapsed": false
  }}
]

WRONG output (DO NOT DO THIS):
[
  {{"id": 1, "content": "long text..."}}  ❌ WRONG!
]

### Node Object Schema (MANDATORY FIELDS)
{{
  "id": "unique_identifier",
  "text": "Node label/title",
  "parent": "parent_node_id or null",
  "level": 0-5,
  "position": {{ "x": number, "y": number }},
  "isCollapsed": false
}}

### Field Specifications

1. **id**: 
   - Use short, descriptive, lowercase identifiers
   - Use underscores or camelCase for multi-word IDs
   - Examples: 'root', 'def', 'markov_chain', 'properties'

2. **text**: 
   - Clear, concise labels (3-8 words maximum)
   - Capture the essence of the concept
   - Use proper capitalization and terminology from the transcript

3. **parent**: 
   - 'null' for root node only
   - Reference the parent node's id for all other nodes
   - Ensure hierarchical relationships are logical

4. **level**: 
   - 0: Root node (main topic)
   - 1: Primary subtopics/major concepts
   - 2: Secondary concepts/details
   - 3: Tertiary details/examples
   - 4-5: Fine-grained details (use sparingly)

5. **position**: 
   - Root (level 0): Start at approximately {{ x: 100, y: 300 }}
   - Level 1: x: 400, distribute y values with ~75-100px spacing
   - Each subsequent level: increase x by ~300px
   - Distribute y coordinates to prevent overlap
   - Group related concepts vertically

6. **isCollapsed**: 
   - Set to false by default

## Analysis Guidelines

### 1. Identify Hierarchy (Keep it Simple and High-Level)
- **Root**: The main subject/topic (short, clear title)
- **Level 1**: 3-6 major conceptual themes ONLY (not every detail)
  - Focus on the BIG IDEAS that organize the content
  - Use clear, professional terminology
  - Avoid verbose descriptions
- **Level 2**: 2-4 key sub-concepts per Level 1 node
  - Only the most important subtopics
  - Keep labels concise (3-6 words max)
- **Level 3+**: Use sparingly, only for critical breakdowns

### 2. Content Organization Principles (NotebookLM Style)
- **Prioritize breadth over depth**: Fewer levels, more horizontal organization
- **Use professional terminology**: Match academic/technical naming conventions
- **Consolidate related ideas**: Don't create separate nodes for closely related concepts
- **Think in categories**: Group similar concepts under umbrella terms
- **Quality over quantity**: 20-40 nodes total is ideal (not 60+)
- **Avoid redundancy**: Each node should represent a distinct concept

### 3. What to Include (High-Level Focus)
- Major conceptual frameworks
- Key methodologies or approaches
- Important mathematical/theoretical constructs
- Main categories of ideas
- Core principles and relationships
- Essential technical terms (as category labels)

### 4. What to Avoid (Critical for Clean Mind Maps)
- ❌ Don't create nodes for examples unless they're major case studies
- ❌ Don't separate "definition" from the concept itself
- ❌ Don't include implementation details or step-by-step procedures
- ❌ Don't add nodes for every formula or equation mentioned
- ❌ Don't create "Properties" or "Characteristics" as separate nodes
- ❌ Don't go beyond 3-4 levels deep
- ❌ Don't include filler words like "Understanding", "Overview", "Introduction"
- ❌ Avoid nodes that just restate the parent with more words

## Positioning Strategy

### Horizontal (x-axis)
- Level 0: x = 100
- Level 1: x = 400 (300px offset)
- Level 2: x = 700 (600px offset)
- Level 3: x = 1000 (900px offset)
- Level 4+: x = 1300+ (continue pattern)

### Vertical (y-axis)
- Calculate center point based on number of siblings
- Space siblings 75-100px apart vertically
- Start first sibling group at y = 100-150
- Adjust y values to prevent overlap between branches
- Keep related concepts close vertically

## Output Format
Return ONLY a valid JSON array, no markdown code blocks, no explanations. Just the raw JSON array starting with [ and ending with ].

## Quality Checklist
- Root node exists with parent: null and level: 0
- All parent references exist as node IDs
- No orphaned nodes (except root)
- Levels increment logically (no skipping levels)
- Positions don't overlap significantly
- Text labels are clear and concise
- Hierarchy represents logical relationships
- All important concepts from transcript are included
- Structure is balanced and readable

Now, analyze the following transcript and generate the mind map JSON:

Transcript:
{transcript}

Remember: Return ONLY the JSON array, nothing else."""

def generate_mindmap_with_ollama(prompt):
    """Send the prompt to the local Ollama model and get the response."""
    try:
        response = ollama.chat(
            model='qwen2.5:3b',
            messages=[
                {
                    'role': 'system',
                    'content': '''You are a JSON generator for mind maps. You MUST output ONLY valid JSON with this EXACT structure:

REQUIRED fields for EVERY object:
- "id": string (e.g., "root", "topic1")  
- "text": string (the label)
- "parent": null for root, or parent's id string for others
- "level": number (0 for root, 1 for children, etc.)
- "position": object with "x" and "y" numbers
- "isCollapsed": boolean (always false)

Return ONLY the JSON array. No explanations. No markdown. Start with [ and end with ].'''
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            options={
                'temperature': 0.2,  # Lower temperature for more consistent JSON
                'num_predict': 3000,  # Increased limit for larger mindmaps
            }
        )
        return response['message']['content']
    except Exception as e:
        print(f"Error communicating with Ollama: {e}")
        return None

def clean_json_response(response):
    """Clean the response to extract valid JSON."""
    import re
    
    # Remove markdown code blocks if present
    response = response.strip()
    if response.startswith('```'):
        # Find the actual JSON content
        lines = response.split('\n')
        json_lines = []
        in_code_block = False
        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            if in_code_block or (not line.strip().startswith('```')):
                json_lines.append(line)
        response = '\n'.join(json_lines)
    
    # Find the JSON array
    start = response.find('[')
    end = response.rfind(']') + 1
    if start != -1 and end > start:
        response = response[start:end]
    
    # Remove control characters
    response = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', response)
    
    # Fix common JSON issues
    response = response.replace('\n', ' ').replace('\r', '')
    response = re.sub(r'\s+', ' ', response)
    
    return response.strip()

def attempt_fix_string_array(json_str):
    """Attempt to fix JSON arrays that contain stringified objects."""
    try:
        data = json.loads(json_str)
        
        # Check if we have an array of strings
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], str):
            print("⚠️  Detected array of strings. Attempting to parse each string as JSON...")
            fixed_data = []
            
            for i, item in enumerate(data):
                try:
                    # Try to parse each string as JSON
                    parsed_item = json.loads(item)
                    fixed_data.append(parsed_item)
                except json.JSONDecodeError:
                    print(f"   Failed to parse item {i}: {item[:50]}...")
                    return None
            
            if fixed_data:
                print(f"✅ Successfully parsed {len(fixed_data)} objects from strings")
                return json.dumps(fixed_data)
        
        return json_str
        
    except json.JSONDecodeError:
        return json_str
    except Exception as e:
        print(f"⚠️  Error during fix attempt: {e}")
        return json_str

def validate_mindmap_json(json_data):
    """Validate the mind map JSON structure."""
    try:
        data = json.loads(json_data) if isinstance(json_data, str) else json_data
        
        if not isinstance(data, list):
            print("❌ Error: JSON must be an array")
            return False
        
        if len(data) == 0:
            print("❌ Error: JSON array is empty")
            return False
        
        # Check if elements are strings instead of objects
        if isinstance(data[0], str):
            print("❌ Error: Array contains strings instead of objects")
            print("   The model generated string representations instead of JSON objects")
            return False
        
        # Check if elements are objects
        if not isinstance(data[0], dict):
            print(f"❌ Error: Array elements must be objects, got {type(data[0]).__name__}")
            return False
        
        # Check if wrong format (common mistake: id as number, content field)
        first_node = data[0]
        if 'content' in first_node or (isinstance(first_node.get('id'), (int, float))):
            print(f"❌ Error: Wrong JSON format detected!")
            print(f"   Found fields: {list(first_node.keys())}")
            print(f"   ❌ The model created the wrong structure!")
            print(f"\n   Expected: {{'id': 'string', 'text': 'label', 'parent': null, 'level': 0, 'position': {{'x': 100, 'y': 300}}, 'isCollapsed': false}}")
            print(f"   Got:      {first_node}")
            return False
        
        # Check for required fields
        required_fields = ['id', 'text', 'parent', 'level', 'position']
        missing_fields = [f for f in required_fields if f not in first_node]
        if missing_fields:
            print(f"❌ Error: First node is missing required fields: {missing_fields}")
            print(f"   Found fields: {list(first_node.keys())}")
            print(f"   This is not a valid mindmap structure!")
            return False
        
        # Check for root node
        root_nodes = [node for node in data if node.get('parent') is None]
        if len(root_nodes) != 1:
            print(f"❌ Error: Must have exactly one root node, found {len(root_nodes)}")
            return False
        
        # Check required fields
        required_fields = ['id', 'text', 'parent', 'level', 'position']
        for i, node in enumerate(data):
            if not isinstance(node, dict):
                print(f"❌ Error: Node {i} is not an object")
                return False
                
            for field in required_fields:
                if field not in node:
                    print(f"❌ Error: Node {i} missing required field '{field}'")
                    return False
            
            # Validate position structure
            if not isinstance(node['position'], dict) or 'x' not in node['position'] or 'y' not in node['position']:
                print(f"❌ Error: Node {i} has invalid position structure")
                return False
        
        print("✅ Mind map JSON structure is valid")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON - {e}")
        return False
    except Exception as e:
        print(f"❌ Error during validation: {e}")
        return False

def save_json(json_content, output_file):
    """Save the JSON content to a file."""
    try:
        # Parse and pretty-print the JSON
        parsed_json = json.loads(json_content)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(parsed_json, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON: {e}")
        return False

def save_as_js(json_content, json_filename):
    """Save the JSON content as a JavaScript file."""
    try:
        # Parse and pretty-print the JSON
        parsed_json = json.loads(json_content)
        
        # Create the JavaScript file content
        js_content = f"// Auto-generated from {json_filename}\n"
        js_content += "const mindmapData = "
        js_content += json.dumps(parsed_json, indent=2, ensure_ascii=False)
        js_content += ";\n"
        
        # Save to mindmap_data.js
        js_filename = "mindmap_data.js"
        with open(js_filename, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        return True, js_filename
    except Exception as e:
        print(f"Error saving JavaScript file: {e}")
        return False, None

def main():
    # Define the input transcript file
    transcript_file = "transcript.txt"
    
    # Read the transcript
    transcript = read_transcript(transcript_file)
    if transcript is None:
        return
    
    # Format the prompt
    formatted_prompt = format_mindmap_prompt(transcript)
    print("\n🔄 Processing transcript with local Ollama qwen2.5:3b model...")
    print("Generating mind map JSON structure...\n")
    
    # Generate the mind map JSON using Ollama
    raw_response = generate_mindmap_with_ollama(formatted_prompt)
    
    if raw_response:
        print("📄 Raw response received. Cleaning and validating...\n")
        
        # Save raw response for debugging
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        debug_file = f"mindmap_raw_{timestamp}.txt"
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(raw_response)
        print(f"💾 Raw response saved to '{debug_file}' for debugging\n")
        
        # Clean the response
        json_content = clean_json_response(raw_response)
        
        # Validate the JSON
        if validate_mindmap_json(json_content):
            # Create output filename with timestamp
            output_filename = f"mindmap_{timestamp}.json"
            
            # Save the JSON file
            if save_json(json_content, output_filename):
                print(f"\n✅ Mind map JSON has been created and saved to '{output_filename}'")
                
                # Save as JavaScript file
                success, js_filename = save_as_js(json_content, output_filename)
                if success:
                    print(f"✅ JavaScript version saved to '{js_filename}'")
                else:
                    print(f"⚠️  Warning: Failed to save JavaScript version")
                
                # Display summary
                parsed_data = json.loads(json_content)
                print(f"\n📊 Mind Map Summary:")
                print(f"   Total nodes: {len(parsed_data)}")
                levels = set(node['level'] for node in parsed_data)
                print(f"   Levels: {sorted(levels)}")
                print(f"   Root topic: {parsed_data[0]['text']}")
            else:
                print("\n❌ Failed to save mind map JSON.")
        else:
            print("\n❌ Generated JSON is invalid.")
            print("\n💡 Suggestions:")
            print("   1. The model 'qwen2.5:3b' is not following the instructions properly")
            print("   2. Try a different model:")
            print("      • llama3.2:3b (good balance)")
            print("      • llama3.1:8b (most reliable)")
            print("      • qwen2.5:7b (larger version)")
            print("   3. Check the raw response file to see what the model generated")
            print("   4. If the model keeps generating wrong format, try a larger/better model")
            print(f"\n📝 First 500 characters of cleaned response:")
            print(json_content[:500] + "..." if len(json_content) > 500 else json_content)
    else:
        print("\n❌ Failed to generate mind map JSON.")

if __name__ == "__main__":
    main()
