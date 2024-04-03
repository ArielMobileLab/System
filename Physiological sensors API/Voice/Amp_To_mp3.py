import json
import numpy as np
import soundfile as sf

# Load the JSON file containing the recorded voice data
json_file = "recorded_audio_data.json"

try:
    with open(json_file, "r") as f:
        voice_data = json.load(f)
    print("JSON file loaded successfully.")
    
    # Extract the voice values from the JSON data
    voice_values = [sample["audio_amplitude"] for sample in voice_data]

    # Convert the voice data back into an audio signal
    audio_signal = np.array(voice_values)

    # Sample rate in Hz (e.g., 44100 Hz)
    sample_rate = 16000

    # Save the audio signal as a WAV file
    output_wav_file = "recorded_voice.mp3"
    sf.write(output_wav_file, audio_signal, sample_rate)
    print("WAV file saved:", output_wav_file)

except json.JSONDecodeError as e:
    print("Error decoding JSON:", e)
except FileNotFoundError:
    print("JSON file not found.")
except Exception as e:
    print("An error occurred:", e)

