import json
import numpy as np
import soundfile as sf

# Load the JSON file containing the recorded voice data
json_file = "recorded_audio_data.json"
with open(json_file, "r") as f:
    voice_data = json.load(f)

# Filter voice data based on simulation time
filtered_data = [sample["audio_amplitude"] for sample in voice_data if 208.5 <= sample["simulation_time"] <= 210]

# Extract the voice values from the filtered data
voice_values = [sample[0] for sample in filtered_data]

# Convert the voice data back into an audio signal
audio_signal = np.array(voice_values)

# Sample rate in Hz (e.g., 44100 Hz)
sample_rate = 16000

# Save the audio signal as a WAV file
output_wav_file = "recorded_voice.wav"
sf.write(output_wav_file, audio_signal, sample_rate)
print("WAV file saved:", output_wav_file)

