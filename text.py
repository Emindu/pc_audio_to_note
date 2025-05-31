import whisper
import subprocess
import os

# Step 1: Split the audio using ffmpeg (30-second chunks)
input_file = "system_audio_recording.wav"
chunk_dir = "chunks"
os.makedirs(chunk_dir, exist_ok=True)

# Get duration
duration_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", input_file]
duration = float(subprocess.check_output(duration_cmd).decode().strip())

chunk_length = 30  # seconds
chunk_files = []

for i in range(0, int(duration), chunk_length):
    output_chunk = os.path.join(chunk_dir, f"chunk_{i}.wav")
    subprocess.run([
        "ffmpeg", "-y", "-i", input_file, "-ss", str(i), "-t", str(chunk_length),
        output_chunk
    ])
    chunk_files.append(output_chunk)

# Step 2: Transcribe each chunk
model = whisper.load_model("base")
full_transcription = ""

for chunk in chunk_files:
    result = model.transcribe(chunk)
    full_transcription += result["text"] + " "

# Step 3: Print the result and save to file
stripped_transcript = full_transcription.strip()
print(stripped_transcript)

# Save to text file
with open("transcript.txt", "w", encoding="utf-8") as f:
    f.write(stripped_transcript)


