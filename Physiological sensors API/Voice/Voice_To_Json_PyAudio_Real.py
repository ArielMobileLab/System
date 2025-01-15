import pyaudio
import numpy as np
import time
import rospy
import json
from geometry_msgs.msg import TwistStamped
from std_msgs.msg import Float64  # Updated to handle numeric messages
from datetime import datetime
import signal
import sys
import os

Senario_type = sys.argv[1]
#Senario_type = "Real"

# Global variable to store simulation time
simulation_time = 0.0

# List to store audio amplitude and simulation time data
audio_data_list = []

# Flag to control recording
is_recording = False

# Variable to track last message time
last_msg_time = 0.0

# Callback function to update simulation time
def gnss_callback(data):
    #print(data)
    global simulation_time
    simulation_time = data.twist.angular.y

# Callback function for /X topic
def Record_Flag_callback(msg):
    global is_recording, last_msg_time
    if msg.data != 0:  # Start recording if the number is not zero
        is_recording = True
        last_msg_time = rospy.get_time()

def check_inactivity():
    global is_recording, last_msg_time
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        if rospy.get_time() - last_msg_time > 2:  # 2 seconds without messages
            if is_recording:
                print("No messages on /X. Stopping recording...")
                save_recorded_data()
                audio_data_list.clear()
                is_recording = False
        rate.sleep()

# Define callback function to process incoming audio data
def callback(in_data, frame_count, time_info, status):
    global simulation_time, audio_data_list, is_recording
    if is_recording:
        audio_data = np.frombuffer(in_data, dtype=np.float32)
        world_time = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        audio_data_list.append({"World_time": world_time, "simulation_time": simulation_time, "audio_amplitude": audio_data.tolist()})
    return (in_data, pyaudio.paContinue)

# Function to handle interrupt signal
def signal_handler(sig, frame):
    print("Interrupt received, stopping recording...")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    if is_recording:
        save_recorded_data()
    print("Recording stopped and saved.")
    sys.exit(0)

# Function to save recorded data to a JSON file
def save_recorded_data():
    if audio_data_list:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_json_file = f"/home/omer/Desktop/Parent_experement/Logs_Parent/{Senario_type}/Parent_{Senario_type}_recorded_audio_data_Physiological_{timestamp}.json"
        with open(output_json_file, "w") as file:
            json.dump(audio_data_list, file, indent=4)
        print("Recorded audio data saved to JSON file:", output_json_file)

signal.signal(signal.SIGINT, signal_handler)

duration = 5000
sample_rate = 16000
channels = 1

rospy.init_node('voice_recorder_parent_side')

rospy.Subscriber("/gps_time", TwistStamped, gnss_callback)
rospy.Subscriber("/Record_Flag", Float64, Record_Flag_callback)  # Updated subscriber for numeric data

audio = pyaudio.PyAudio()

stream = audio.open(format=pyaudio.paFloat32,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=1,
                    stream_callback=callback)

stream.start_stream()

import threading
threading.Thread(target=check_inactivity, daemon=True).start()

rospy.spin()

