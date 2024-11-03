import pyaudio
import numpy as np
import time
import rospy
import json
from sensor_msgs.msg import NavSatFix
from datetime import datetime
import signal
import sys
from datetime import datetime
import os

# Global variable to store simulation time
simulation_time = 0.0

# List to store audio amplitude and simulation time data
audio_data_list = []

# Callback function to update simulation time
def gnss_callback(data):
    global simulation_time
    #simulation_time = data.header.seq * 0.033333335071821  # Assuming header.stamp provides simulation time
    header = data.header
    secs = header.stamp.secs
    nsecs = header.stamp.nsecs

# Combine secs and nsecs into a float
    simulation_time = secs + nsecs * 1e-9

# Define callback function to process incoming audio data
def callback(in_data, frame_count, time_info, status):
    global simulation_time, audio_data_list
    # Convert input data to numpy array
    audio_data = np.frombuffer(in_data, dtype=np.float32)
    world_time = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    # Append audio amplitude and simulation time data to the list
    audio_data_list.append({"World_time": world_time, "simulation_time": simulation_time, "audio_amplitude": audio_data.tolist()})
    return (in_data, pyaudio.paContinue)

# Function to handle interrupt signal
def signal_handler(sig, frame):
    print("Interrupt received, stopping recording...")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    save_recorded_data()
    print("Recording stopped and saved.")
    sys.exit(0)

# Function to save recorded data to a JSON file
def save_recorded_data():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    directory = "/home/omer/Desktop/Carla_Logs/Logs"
    os.makedirs(directory, exist_ok=True)
    output_json_file = os.path.join(directory, f"recorded_audio_data_{timestamp}.json")
    with open(output_json_file, "w") as file:
        json.dump(audio_data_list, file, indent=4)
    print("Recorded audio data saved to JSON file:", output_json_file)

# Register the signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# Define parameters for recording
duration = 10  # Record for n seconds (not used in this script)
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
print("Recording live audio..~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.")
stream.start_stream()

# Keep the script running
rospy.spin()
