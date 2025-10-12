import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def read_transcript(file_path):
    """Read the transcript from the text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None

def format_mindmap_prompt(transcript):
    """
    Format the detailed prompt for generating mind map JSON from the transcript.
    This powerful prompt engineering is the key to getting reliable JSON output.
    """
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

### CORRECT Output Example:
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
  }}
]

## Analysis Guidelines
- **Identify Hierarchy**: Focus on high-level concepts. Root -> 3-6 Major Themes -> 2-4 Key Sub-concepts per theme.
- **Content Organization**: Prioritize breadth over depth. Use professional terminology. Aim for 20-40 nodes total.
- **What to Avoid**: Don't create nodes for minor examples, simple definitions, or implementation details. Do not go beyond 3-4 levels deep.

## Output Format
Return ONLY a valid JSON array. Do not include markdown code blocks, explanations, or any text outside of the JSON. Your entire response must start with '[' and end with ']'.

Now, analyze the following transcript and generate the mind map JSON:

Transcript:
{transcript}

Remember: Return ONLY the JSON array, nothing else."""

def generate_mindmap_with_perplexity(prompt):
    """Send the prompt to the Perplexity API and get the response."""
    # --- Configuration from .env with sensible defaults ---
    api_key = os.getenv('PERPLEXITY_API_KEY')
    api_url = os.getenv('PERPLEXITY_API_URL', "https://api.perplexity.ai/chat/completions")
    model = os.getenv('PERPLEXITY_MODEL', "llama-3-sonar-large-32k-online")

    if not api_key:
        print("❌ Error: PERPLEXITY_API_KEY not found. Please add it to your .env file.")
        return None

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a precise JSON generator. You must output only valid JSON, strictly following the user's requested format. Do not include any explanations or markdown. Your response must begin with '[' and end with ']'."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.1,  # Low temperature for deterministic, structured JSON output
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        response_json = response.json()

        # Extract the content from the response
        if response_json and 'choices' in response_json and len(response_json['choices']) > 0:
            return response_json['choices'][0]['message']['content']
        else:
            print(f"⚠️ Warning: API returned an unexpected response format: {response_json}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error communicating with Perplexity API: {e}")
        return None

def clean_json_response(response_text):
    """Clean the raw API response to extract a valid JSON string."""
    # Find the start of the JSON array and its corresponding end
    start_index = response_text.find('[')
    end_index = response_text.rfind(']')

    if start_index != -1 and end_index != -1 and end_index > start_index:
        return response_text[start_index : end_index + 1]
    
    print("⚠️ Warning: Could not find a JSON array '[...]' in the API response.")
    return response_text # Return original text if no array is found, for debugging

def validate_mindmap_json(json_string):
    """Validate the mind map JSON string against the required structure."""
    try:
        data = json.loads(json_string)
        if not isinstance(data, list) or not data:
            print("❌ Validation Error: JSON is not a non-empty array.")
            return False

        required_fields = ['id', 'text', 'parent', 'level', 'position']
        for i, node in enumerate(data):
            if not isinstance(node, dict):
                print(f"❌ Validation Error: Item {i} is not an object.")
                return False
            for field in required_fields:
                if field not in node:
                    print(f"❌ Validation Error: Node {i} is missing required field '{field}'.")
                    return False
            if not isinstance(node.get('position'), dict) or 'x' not in node['position'] or 'y' not in node['position']:
                print(f"❌ Validation Error: Node {i} has an invalid 'position' structure.")
                return False

        if sum(1 for node in data if node.get('parent') is None) != 1:
            print("❌ Validation Error: There must be exactly one root node (parent: null).")
            return False

        print("✅ Mind map JSON structure is valid.")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ Validation Error: Invalid JSON format. {e}")
        return False

def save_file(content, filename):
    """Save content to a file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except IOError as e:
        print(f"❌ Error saving file {filename}: {e}")
        return False

def main():
    """Main function to run the transcript-to-mindmap process."""
    transcript_file = "transcript.txt"
    transcript = read_transcript(transcript_file)
    if not transcript:
        return

    formatted_prompt = format_mindmap_prompt(transcript)
    
    model_name = os.getenv('PERPLEXITY_MODEL', "default model")
    print(f"\n🔄 Processing transcript with Perplexity model: {model_name}...")
    
    raw_response = generate_mindmap_with_perplexity(formatted_prompt)
    if not raw_response:
        print("\n❌ Failed to get a response from the Perplexity API.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    debug_filename = f"mindmap_raw_{timestamp}.txt"
    save_file(raw_response, debug_filename)
    print(f"📄 Raw response saved to '{debug_filename}' for debugging.")

    json_content = clean_json_response(raw_response)
    if not validate_mindmap_json(json_content):
        print("\n❌ Generated content failed validation.")
        print("💡 Check the raw response file and adjust the prompt or model if needed.")
        return

    # Save the final valid JSON
    output_filename = f"mindmap_{timestamp}.json"
    parsed_json = json.loads(json_content)
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(parsed_json, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Mind map JSON successfully saved to '{output_filename}'")
    except IOError as e:
        print(f"\n❌ Failed to save final JSON file: {e}")
        return
        
    # Display summary
    print("\n📊 Mind Map Summary:")
    print(f"   - Total nodes: {len(parsed_json)}")
    levels = sorted(list(set(node['level'] for node in parsed_json)))
    print(f"   - Levels found: {levels}")
    root_node = next((node for node in parsed_json if node['parent'] is None), None)
    if root_node:
        print(f"   - Root topic: '{root_node['text']}'")

if __name__ == "__main__":
    main()