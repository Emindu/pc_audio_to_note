import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def read_transcript(file_path):
    """Read the transcript from the text file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def format_prompt(transcript):
    """Format the prompt for the Perplexity API."""
    return f"""Create a concise markdown note from this transcript. Include only key points and main ideas.

    Requirements:
    - Use headers and bullet points
    - Be brief and direct
    - Use only information from the transcript

    Transcript:
    {transcript}"""

def send_to_perplexity(prompt):
    """Send request to Perplexity API."""
    api_key = os.getenv('PERPLEXITY_API_KEY')
    api_url = os.getenv('PERPLEXITY_API_URL')
    model = os.getenv('PERPLEXITY_MODEL', 'sonar')
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that creates well-structured markdown notes."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error sending to Perplexity API: {e}")
        return None

def extract_answer(response):
    """Extract the answer from the API response."""
    if response and 'choices' in response and len(response['choices']) > 0:
        return response['choices'][0]['message']['content']
    return "No response received from API"

def save_markdown(markdown_content, output_file):
    """Save the markdown content to a file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

def save_as_js(markdown_content, js_filename="note_data.js"):
    """Save markdown content as a JavaScript file for direct embedding."""
    # Escape special characters for JavaScript string
    escaped_content = (markdown_content
                      .replace('\\', '\\\\')
                      .replace('`', '\\`')
                      .replace('${', '\\${'))
    
    js_content = f"const noteMarkdown = `{escaped_content}`;\n"
    
    with open(js_filename, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"✅ Saved JavaScript version: {js_filename}")

def main():
    # Output filename
    output_filename = "note.md"
    
    # Read the transcript
    transcript = read_transcript("transcript.txt")
    
    # Format the prompt
    formatted_prompt = format_prompt(transcript)
    print("\nProcessing transcript...")
    
    # Send to Perplexity API
    response = send_to_perplexity(formatted_prompt)
    markdown_content = extract_answer(response)
    
    source_input = input("Add source (optional): ")
    if source_input.strip():
        markdown_content += f"\n\n### Source: {source_input}"
    else:
        # If the input is empty or just whitespace, add a newline for spacing
        markdown_content += "### Source:  \n"

    
    if markdown_content != "No response received from API":
        # Save the markdown file
        save_markdown(markdown_content, output_filename)
        print(f"\n✅ Markdown notes have been created and saved to '{output_filename}'")
        
        # Save as JavaScript file for direct embedding
        save_as_js(markdown_content)
    else:
        print("\n❌ Failed to create markdown notes due to API error")

if __name__ == "__main__":
    main() 