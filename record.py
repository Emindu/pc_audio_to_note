import sounddevice as sd
import soundfile as sf
import numpy as np
import time
import sys
import queue

# --- Configuration ---
OUTPUT_FILENAME = "system_audio_recording.wav"
SAMPLE_RATE = 44100  # Sample rate (Hz). Needs to match BlackHole's setting in Audio MIDI Setup
DEVICE_NAME_QUERY = "BlackHole" # Part of the name of the BlackHole device to search for
CHANNELS = 2  # Number of channels (stereo)
DTYPE = 'float32'  # Data type for recording

# --- Find BlackHole Device ---
def find_blackhole_device_index():
    """Finds the input device index for BlackHole."""
    devices = sd.query_devices()
    print("\nAvailable Devices:")
    print(devices)
    for index, device in enumerate(devices):
        if DEVICE_NAME_QUERY in device['name'] and device['max_input_channels'] > 0:
            print(f"\nFound BlackHole input device: '{device['name']}' with index {index}")
            print(f"Device default sample rate: {device['default_samplerate']} Hz")
            global SAMPLE_RATE
            return index
    return None

blackhole_index = find_blackhole_device_index()

if blackhole_index is None:
    print(f"\nError: Could not find an input device matching '{DEVICE_NAME_QUERY}'.")
    print("Please ensure BlackHole is installed and check the DEVICE_NAME_QUERY.")
    print("Run this script again after uncommenting the 'Available Devices' print statements to see device names.")
    sys.exit(1)

# --- Recording ---
try:
    print(f"\nRecording system audio via '{sd.query_devices(blackhole_index)['name']}'...")
    print(f"Sample Rate: {SAMPLE_RATE} Hz")
    print("Press Ctrl+C to stop recording.")

    # Create a queue to store the recorded data
    q = queue.Queue()
    
    def callback(indata, frames, time, status):
        """This is called for each audio block."""
        if status:
            print(status)
        q.put(indata.copy())

    # Start the recording stream
    with sd.InputStream(samplerate=SAMPLE_RATE,
                       channels=CHANNELS,
                       dtype=DTYPE,
                       device=blackhole_index,
                       callback=callback):
        print("Recording started...")
        # Keep recording until Ctrl+C
        while True:
            time.sleep(0.1)  # Small sleep to prevent CPU overuse

except KeyboardInterrupt:
    print("\nRecording stopped by user.")
    # Get all recorded data from the queue
    recording = []
    while not q.empty():
        recording.append(q.get())
    
    if recording:
        # Convert list of arrays to a single array
        recording = np.concatenate(recording, axis=0)
        
        # Save the recording
        try:
            print(f"Saving audio to {OUTPUT_FILENAME}...")
            sf.write(OUTPUT_FILENAME, recording, SAMPLE_RATE)
            print("Audio saved successfully.")
        except Exception as e:
            print(f"\nAn error occurred while saving the file: {e}")
    else:
        print("No audio data was recorded.")

except Exception as e:
    print(f"\nAn error occurred during recording: {e}")
    sys.exit(1)
