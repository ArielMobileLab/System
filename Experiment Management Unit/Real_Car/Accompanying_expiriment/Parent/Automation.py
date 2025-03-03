#!/usr/bin/env python

import subprocess
import os
import signal
import rospy
import time
import psutil
from std_msgs.msg import Float64  # Adjust message type if necessary
from nav_msgs.msg import Odometry
import multiprocessing

# Function to check and start roscore if not running
def start_roscore():
        # Set ROS environment variables
        os.environ['ROS_IP'] = '10.20.0.1'
        os.environ['ROS_MASTER_URI'] = 'http://10.20.0.180:11311'
        rospy.loginfo("ROS environment variables set.")

# Flags to control scenario execution and inactivity timeout
scenario_executed = False
last_message_time = time.time()
TIMEOUT_DURATION = 5  # Seconds before shutting down due to inactivity
scenario_process = None  # Track the scenario process
terminal_opened = True
Flag = True
voice_flag = True
ffmpeg_flag = True
Flag2 = True

# Function to launch the scenario
def launch_scenario(scenarioslist, Town, Face, Objects, Arrow_Guilde):
    global scenario_process

    for scenario in scenarioslist:
        try:
            # Use Popen to track the running process
            scenario_process = subprocess.Popen(["bash", scenario, Town, Face, Objects, Arrow_Guilde])
            scenario_process.wait()
        except subprocess.CalledProcessError as e:
            rospy.logerr(f"Failed to run scenario: {e}")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`need to fix so the data will be saved!!
# def stop_scenario():
#     global scenario_process, Flag
#     if scenario_process and scenario_process.poll() is None and Flag == True:
#         rospy.loginfo("Sending SIGINT to stop scenario gracefully (Ctrl+C)...")

#                 # Handle 'Voice_To_Json_PyAudio.py' gracefully
#         for proc in psutil.process_iter(attrs=['pid', 'name', 'username', 'cmdline']):
#                 # Filter for Python-related processes running the specific script
#                 if 'python' in proc.info['name'].lower() and 'Voice_To_Json_PyAudio.py' in ' '.join(proc.info['cmdline']):
#                     rospy.loginfo(f"Sending SIGINT to process PID: {proc.info['pid']} | Command: {' '.join(proc.info['cmdline'])}")
#                     proc.send_signal(signal.SIGINT)  
#                     Flag = False

#         # Send SIGINT (equivalent to pressing Ctrl+C)
#         #os.kill(scenario_process.pid, signal.SIGINT)

#         # Wait for the process to exit (gracefully), allowing time for log saving
#         try:
#             rospy.loginfo("Waiting for the process to exit gracefully...")
#             #scenario_process.wait(timeout=20)  # Wait up to 60 seconds
#         except subprocess.TimeoutExpired:
#             rospy.logwarn("Process did not exit gracefully in time. Force killing process...")
#             #os.kill(scenario_process.pid, signal.SIGTERM)  # Force termination (if still running)



def stop_scenario():
    global ffmpeg_flag, voice_flag  # Ensure we update both flags

    # Define process order: First stop "Voice_To_Json_PyAudio.py", then "ffmpeg"
    process_order = ["Voice_To_Json_PyAudio.py", "ffmpeg"]
    process_flags = {"Voice_To_Json_PyAudio.py": "voice_flag", "ffmpeg": "ffmpeg_flag"}
    process_found = {"Voice_To_Json_PyAudio.py": False, "ffmpeg": False}

    for process_name in process_order:  # Process in order: Voice_To_Json_PyAudio.py -> ffmpeg
        for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
            try:
                process_cmd = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ""

                if process_name in process_cmd:
                    rospy.loginfo(f"Sending SIGINT to {process_name} (PID: {proc.info['pid']}) | Command: {process_cmd}")
                    proc.send_signal(signal.SIGINT)  # Graceful termination
                    process_found[process_name] = True
                    proc.wait(timeout=10000)  # Wait up to 15 sec for graceful shutdown
                    rospy.loginfo(f"{process_name} has stopped successfully.")

                    if process_name == "Voice_To_Json_PyAudio.py":
                        voice_flag = False
                        rospy.loginfo("Voice_To_Json_PyAudio.py stopped. voice_flag set to False.")
                        time.sleep(1)  # Short delay to ensure clean shutdown before handling FFmpeg

                    if process_name == "ffmpeg":
                        ffmpeg_flag = False
                        rospy.loginfo("FFmpeg stopped. ffmpeg_flag set to False.")
           
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue  # Ignore errors from terminated processes

    if not any(process_found.values()):
        if Flag2 == True:
            proc.wait(timeout=5)  # Wait up to 5 sec for graceful shutdown
            Flag2 = False
        rospy.loginfo("No matching processes found. Nothing to stop.")


scenarios = [
    {
        "name": "Parent_side_Far",

        "code": ["/home/omer/Desktop/Experiment Management Unit/Simulations/Carla/Parent/Senarios/Parent_Close.sh","Town04","Close","Nah","Guide_Parent"],
        "code2": ["/home/omer/Desktop/Experiment Management Unit/Simulations/Carla/Parent/Senarios/Parent.sh","Town04","Far","Nah","Guide_Parent"],
        "code3": ["/home/omer/Desktop/Experiment Management Unit/Simulations/Carla/Parent/Senarios/Parent.sh","Town04","Far","Nah","Guide_Parent"],
        "code4": ["/home/omer/Desktop/Experiment Management Unit/Simulations/Carla/Parent/Senarios/Parent.sh","Town04","Far","Nah","Guide_Parent_C"],
        "code5": ["/home/omer/Desktop/Experiment Management Unit/Simulations/Carla/Parent/Senarios/Parent_Close.sh","Town04","Close","Nah","Guide_Parent"],
        "code6": ["/home/omer/Desktop/Experiment Management Unit/Simulations/Carla/Parent/Senarios/Parent_Close.sh","Town04","Close","Nah","Guide_Parent"],
        "code7": ["/home/omer/Desktop/Experiment Management Unit/Simulations/Carla/Parent/Senarios/Parent_Close.sh","Town04","Close","Nah","Guide_Parent_C"],
        "code8": ["/home/omer/Desktop/Experiment Management Unit/Simulations/Carla/Parent/Senarios/Parent_avatar.sh","Town04","Avatar","Nah","Guide_Parent"],
        "code9": ["/home/omer/Desktop/Experiment Management Unit/Simulations/Carla/Parent/Senarios/Parent_avatar.sh","Town04","Avatar","Nah","Guide_Parent"],
        "code10":["/home/omer/Desktop/Experiment Management Unit/Simulations/Carla/Parent/Senarios/Parent_avatar.sh","Town04","Avatar","Nah","Guide_Parent_C"]

    }
]
def callback2(msg):
        global  last_message_time
        last_message_time = time.time()


# Callback function for ROS subscriber
def callback(msg):
    time.sleep(5)

    global scenario_executed, last_message_time
    
    # Convert the message into an integer (assuming it's a number)
    try:
        scenario_id = int(msg.data)  # If msg is a Float64, convert it to an int
    except ValueError:
        rospy.logwarn(f"Received invalid message: {msg.data}")
        return
    
    scenario = scenarios[0]  # The first scenario in the list (you can change this if needed)
    
    # Check which scenario to execute based on the message value
    if not scenario_executed:
        #if scenario_id == 1:
        #    rospy.loginfo("Received message '1', launching 'code' scenario...")
        #    launch_scenario(scenario["code"], scenario["code"][1], scenario["code"][2], scenario["code"][3], scenario["code"][4])
        if scenario_id == 2:
            rospy.loginfo("Received message '2', launching 'code1' scenario...")
            launch_scenario(scenario["code2"], scenario["code2"][1], scenario["code2"][2], scenario["code2"][3], scenario["code2"][4])
        elif scenario_id == 3:
            rospy.loginfo("Received message '3', launching 'code2' scenario...")
            launch_scenario(scenario["code3"], scenario["code3"][1], scenario["code3"][2], scenario["code3"][3], scenario["code3"][4])
        elif scenario_id == 4:
            rospy.loginfo("Received message '4', launching 'code3' scenario...")
            launch_scenario(scenario["code4"], scenario["code4"][1], scenario["code4"][2], scenario["code4"][3], scenario["code4"][4])
        elif scenario_id == 5:
            rospy.loginfo("Received message '5', launching 'code4' scenario...")
            launch_scenario(scenario["code5"], scenario["code5"][1], scenario["code5"][2], scenario["code5"][3], scenario["code5"][4])
        elif scenario_id == 6:
            rospy.loginfo("Received message '6', launching 'code5' scenario...")
            launch_scenario(scenario["code6"], scenario["code6"][1], scenario["code6"][2], scenario["code6"][3], scenario["code6"][4])
        elif scenario_id == 7:
            rospy.loginfo("Received message '7', launching 'code5' scenario...")
            launch_scenario(scenario["code7"], scenario["code7"][1], scenario["code7"][2], scenario["code7"][3], scenario["code7"][4])
        elif scenario_id == 8:
            rospy.loginfo("Received message '5', launching 'code4' scenario...")
            launch_scenario(scenario["code8"], scenario["code8"][1], scenario["code8"][2], scenario["code8"][3], scenario["code8"][4])
        elif scenario_id == 9:
            rospy.loginfo("Received message '6', launching 'code5' scenario...")
            launch_scenario(scenario["code9"], scenario["code9"][1], scenario["code9"][2], scenario["code9"][3], scenario["code9"][4])
        elif scenario_id == 10:
            rospy.loginfo("Received message '6', launching 'code5' scenario...")
            launch_scenario(scenario["code10"], scenario["code10"][1], scenario["code10"][2], scenario["code10"][3], scenario["code10"][4])
        else:
            rospy.loginfo(f"Invalid scenario_id '{scenario_id}', no scenario executed.")

        
        # Mark scenario as executed to prevent repeated execution
        scenario_executed = True
    else:
        
        rospy.loginfo("Scenario has already been executed or invalid message.")


# Function to monitor inactivity and shut down
def monitor_inactivity():
    global last_message_time
    while True:
        #print(time.time() - last_message_time)  # Print time difference
        # Check if the timeout duration has passed since the last message
        if time.time() - last_message_time > TIMEOUT_DURATION:
            #print("No messages received for a while. Resetting terminal_opened flag.")
            stop_scenario()
        
        time.sleep(1)  # Sleep for a second before checking again


# ROS Node initialization
def listener():
    rospy.init_node('scenario_runner', anonymous=True)
    #rospy.Subscriber('/start_senario', Float64, callback)
    rospy.Subscriber('senario_type', Float64, callback)
    rospy.Subscriber('/carla/ego_vehicle/odometry', Odometry, callback2, queue_size=1)
    monitor_inactivity()
    rospy.spin()

if __name__ == '__main__':
    start_roscore()  # Ensure roscore is running
    listener()


