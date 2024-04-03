import socket
import struct
import pyaudio
import numpy as np
import time
import json
from sensor_msgs.msg import NavSatFix
from datetime import datetime

MatLabPort = 12355
bufferSize = 2048
receiverIP = "10.20.0.133"

# Create a UDP socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind the socket to the address and port
UDPServerSocket.bind((receiverIP, MatLabPort))

print("UDP server up and listening...")

# Global variable to store simulation time
simulation_time = 0.0

# List to store audio amplitude and simulation time data
audio_data_list = []

# Callback function to update simulation time
# Define callback function to process incoming audio data
def callback(in_data, frame_count, time_info, status):
    global simulation_time, audio_data_list
    # Convert input data to numpy array
    audio_data = np.frombuffer(in_data, dtype=np.float32)
    world_time = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    # Append audio amplitude and simulation time data to the list
    audio_data_list.append({"World_time": world_time, "simulation_time": simulation_time, "audio_amplitude": audio_data.tolist()})
    return (in_data, pyaudio.paContinue)

# Define parameters for recording
duration = 5  # Record for 15 seconds
sample_rate = 16000  # Sample rate (samples per second)
channels = 1  # Mono audio

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open audio stream with callback function
stream = audio.open(format=pyaudio.paFloat32,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=1,
                    stream_callback=callback)

# Start recording
print("Recording live audio...")
stream.start_stream()

# Start time for tracking 16K lines per second
start_time = time.time()

# Receive simulation time from UDP and record audio
while True:
    # Receive data from the client
    data, address = UDPServerSocket.recvfrom(bufferSize)
    
    # Unpack the received data to get simulation time
    unpacked_data = struct.unpack(f"{len(data)//struct.calcsize('d')}d", data)
    simulation_time = unpacked_data[0]
    
    # Check if it's time to stop
    if time.time() - start_time > duration:
        print(simulation_time)
	
        break

# Stop recording
print("Recording complete.")

# Close the stream and terminate PyAudio
stream.stop_stream()
stream.close()
audio.terminate()

# Save recorded data to a JSON file
output_json_file = "recorded_audio_data.json"
with open(output_json_file, "w") as file:
    json.dump(audio_data_list, file, indent=4)

print("Recorded audio data saved to JSON file:", output_json_file)

