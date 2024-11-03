import pyaudio
import numpy as np
import time
import rospy
import json
from sensor_msgs.msg import NavSatFix
from datetime import datetime

# Global variable to store simulation time
simulation_time = 0.0

# List to store audio amplitude and simulation time data
audio_data_list = []

# Callback function to update simulation time
def gnss_callback(data):
    global simulation_time
    simulation_time = data.header.seq * 0.033333335071821  # Assuming header.stamp provides simulation time

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
duration = 10  # Record for n seconds
sample_rate = 16000  # Sample rate (samples per second)
channels = 1  # Mono audio

# Initialize ROS node
rospy.init_node('voice_recorder')

# Subscribe to the ROS topic that publishes simulation time
rospy.Subscriber("/carla/ego_vehicle/gnss", NavSatFix, gnss_callback)

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

# Wait for the specified duration
time.sleep(duration)

# Stop recording
print("Recording complete.")
print("simulation_time:")
print(simulation_time)
# Close the stream and terminate PyAudio
stream.stop_stream()
stream.close()
audio.terminate()

# Save recorded data to a JSON file
output_json_file = "recorded_audio_data.json"
with open(output_json_file, "w") as file:
    json.dump(audio_data_list, file, indent=4)

print("Recorded audio data saved to JSON file:", output_json_file)

