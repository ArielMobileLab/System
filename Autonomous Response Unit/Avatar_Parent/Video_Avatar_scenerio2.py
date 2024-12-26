import rospy
from nav_msgs.msg import Odometry
import vlc
import time
import tkinter as tk
import json
from datetime import datetime
import os
from collections import OrderedDict
from carla import TrafficLightState
import carla
import sys


# Global flags to track if the videos have been played
video_flags = {
    'video1': False,
    'video2': False,
    # 'video3': False,
    'video4': False,
    'video5': False,
    'video6': False
}

Agent_type = "_Avatar"
Folder_Name = sys.argv[2]

folder_path = "/home/omer/Desktop/Carla_Logs/Logs/{}".format(Folder_Name)
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
file_name = os.path.join(folder_path, 'Video_Status{}_{}.json'.format(Agent_type, current_time))


client = carla.Client('localhost', 2000)
client.set_timeout(2.0)
world = client.get_world()


def get_traffic_light_state_by_id(world, traffic_light_id):
    traffic_light = world.get_actor(traffic_light_id)
    if traffic_light is not None:
        return traffic_light.get_state()
    return None


def write_to_json(data_dict):
   
    # Open the JSON file in append mode and write the data
    with open(file_name, 'a') as json_file:
        json.dump(data_dict, json_file)
        json_file.write('\n')  # Add a newline for readability



def play_video(video_path, window_x, window_y, window_width, window_height):
    # Create a Tkinter window
    root = tk.Tk()
    root.geometry("{0}x{1}+{2}+{3}".format(window_width, window_height, window_x, window_y))
    root.title("Video Player")
    root.attributes('-topmost', True)
    root.wm_attributes('-topmost', 1)
    root.focus_force()

    # Initialize VLC player
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(video_path)
    player.set_media(media)



    # Embed VLC player in Tkinter window
    root.update()
    player.set_xwindow(root.winfo_id())

    # Play the video
    player.play()

    # Wait for a short time to let the player start
    time.sleep(1)

    # Check if the video is still playing
    def check_video():
        if player.get_state() not in (vlc.State.Ended, vlc.State.Error):
            root.after(100, check_video)
        else:
            root.destroy()

    root.after(100, check_video)
    root.mainloop()



def odometry_callback(data):
    global video_flags

    x = data.pose.pose.position.x
    y = data.pose.pose.position.y

    # Screen dimensions
    single_screen_width = 2150  # Width of a single screen (adjust as necessary)
    screen_height = 1080  # Height of the screens

    # Desired video window size
    window_width = 250
    window_height = 250

    # Calculate position to center the window at the bottom of the middle screen
    middle_screen_x_start = single_screen_width  # Start of the middle screen
    window_x = middle_screen_x_start + (single_screen_width - window_width) // 2
    window_y = screen_height - window_height - 50  # Adjust to place it slightly above the bottom edge

    # Video 1 condition
    if 200 < x < 230 and -65 < y < -50 and not video_flags['video1']:

        timestamp = datetime.now().strftime('%H:%M:%S.%f')
        simulation_time = data.header.seq*0.033333335071821

        header = data.header
        secs = header.stamp.secs
        nsecs = header.stamp.nsecs

        # Combine secs and nsecs into a float
        simulation_Time = secs + nsecs * 1e-9

        Egocar_data = OrderedDict()
        Egocar_data["Type"] = "Video_Status:"
        Egocar_data["Timestamp"] = timestamp
        Egocar_data["Simulation_time_ROS"] = simulation_time
        Egocar_data["Simulation_time"] = simulation_Time
        Egocar_data["Video"] = "person_cross"
        write_to_json(Egocar_data) # for json

        video_path1 = '/home/omer/Desktop/Autonomous Resope Unit/Avatar_Parent/Avatar_video/person_cross.mp4'
        play_video(video_path1, window_x, window_y, window_width, window_height)
        video_flags['video1'] = True

    # Video 2 condition
    elif 165 < x < 195 and -8 < y < 8 and not video_flags['video2']:

        timestamp = datetime.now().strftime('%H:%M:%S.%f')
        simulation_time = data.header.seq*0.033333335071821

        header = data.header
        secs = header.stamp.secs
        nsecs = header.stamp.nsecs

        # Combine secs and nsecs into a float
        simulation_Time = secs + nsecs * 1e-9

        Egocar_data = OrderedDict()
        Egocar_data["Type"] = "Video_Status:"
        Egocar_data["Timestamp"] = timestamp
        Egocar_data["Simulation_time_ROS"] = simulation_time
        Egocar_data["Simulation_time"] = simulation_Time
        Egocar_data["Video"] = "car_stop"
        write_to_json(Egocar_data) # for json

        video_path2 = '/home/omer/Desktop/Autonomous Resope Unit/Avatar_Parent/Avatar_video/car_stop.mp4'
        play_video(video_path2, window_x, window_y, window_width, window_height)
        video_flags['video2'] = True

    # # Video 3 condition
    # elif 330.00 < x < 345.00 and -33 < y < -13 and not video_flags['video3']:
    #     video_path3 = '/home/omer/Desktop/CARLA_0.9.13/PythonAPI/examples/Map_objects/Parent/Mordechai/Avatar video/person_cross.mp4'
    #     play_video(video_path3, window_x, window_y, window_width, window_height)
    #     video_flags['video3'] = True

    # Video 4 condition
    elif 328 < x < 345 and  -186 < y < -140 and not video_flags['video4']:

        traffic_light_id = 80  # Traffic light ID
        traffic_light_state = get_traffic_light_state_by_id(world, traffic_light_id)

        if traffic_light_state == TrafficLightState.Yellow or traffic_light_state == TrafficLightState.Red:

            timestamp = datetime.now().strftime('%H:%M:%S.%f')
            simulation_time = data.header.seq*0.033333335071821

            header = data.header
            secs = header.stamp.secs
            nsecs = header.stamp.nsecs

            # Combine secs and nsecs into a float
            simulation_Time = secs + nsecs * 1e-9

            Egocar_data = OrderedDict()
            Egocar_data["Type"] = "Video_Status:"
            Egocar_data["Timestamp"] = timestamp
            Egocar_data["Simulation_time_ROS"] = simulation_time
            Egocar_data["Simulation_time"] = simulation_Time
            Egocar_data["Video"] = "red_light"
            write_to_json(Egocar_data) # for json


            video_path4 = '/home/omer/Desktop/Autonomous Resope Unit/Avatar_Parent/Avatar_video/red_light.mp4'
            play_video(video_path4, window_x, window_y, window_width, window_height)
            video_flags['video4'] = True

    # Video 5 condition
    elif 260.00 < x < 290.00 and -332.00 < y < -323.00 and not video_flags['video5']:

        timestamp = datetime.now().strftime('%H:%M:%S.%f')
        simulation_time = data.header.seq*0.033333335071821

        header = data.header
        secs = header.stamp.secs
        nsecs = header.stamp.nsecs

        # Combine secs and nsecs into a float
        simulation_Time = secs + nsecs * 1e-9

        Egocar_data = OrderedDict()
        Egocar_data["Type"] = "Video_Status:"
        Egocar_data["Timestamp"] = timestamp
        Egocar_data["Simulation_time_ROS"] = simulation_time
        Egocar_data["Simulation_time"] = simulation_Time
        Egocar_data["Video"] = "barrier"
        write_to_json(Egocar_data) # for json

        video_path5 = '/home/omer/Desktop/Autonomous Resope Unit/Avatar_Parent/Avatar_video/barrier.mp4'
        play_video(video_path5, window_x, window_y, window_width, window_height)
        video_flags['video5'] = True
    
    # Video 6 condition
    elif 82 < x < 98 and -280.0 < y < -210.0 and not video_flags['video6']:

        traffic_light_id = 60  # Traffic light ID

        traffic_light_state = get_traffic_light_state_by_id(world, traffic_light_id)

        if traffic_light_state == TrafficLightState.Yellow:


            timestamp = datetime.now().strftime('%H:%M:%S.%f')
            simulation_time = data.header.seq*0.033333335071821

            header = data.header
            secs = header.stamp.secs
            nsecs = header.stamp.nsecs

            # Combine secs and nsecs into a float
            simulation_Time = secs + nsecs * 1e-9

            Egocar_data = OrderedDict()
            Egocar_data["Type"] = "Video_Status:"
            Egocar_data["Timestamp"] = timestamp
            Egocar_data["Simulation_time_ROS"] = simulation_time
            Egocar_data["Simulation_time"] = simulation_Time
            Egocar_data["Video"] = "red_light"
            write_to_json(Egocar_data) # for json

            video_path6 = '/home/omer/Desktop/Autonomous Resope Unit/Avatar_Parent/Avatar_video/red_light.mp4'
            play_video(video_path6, window_x, window_y, window_width, window_height)
            video_flags['video6'] = True    


# Initialize ROS node
rospy.init_node('Video_Agent')

# Subscribe to the odometry topic
rospy.Subscriber("/carla/ego_vehicle/odometry", Odometry, odometry_callback)

# Set the desired loop frequency (1 Hz in this example)
rate = rospy.Rate(1)

# Continue running the code
while not rospy.is_shutdown():
    rate.sleep()
